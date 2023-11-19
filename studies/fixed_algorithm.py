import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tabulate import tabulate
import warnings

class RestaurantRecommender:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)

    def preprocess_data(self):
        self.data['메뉴'] = self.data['메뉴'].apply(lambda x: ''.join(x))

    def calculate_similarity(self):
        count_vec = CountVectorizer(min_df=0, ngram_range=(1, 2))
        menu_mat = count_vec.fit_transform(self.data['메뉴'])
        self.menu_sim = cosine_similarity(menu_mat, menu_mat)

    def weighted_vote_average(self, record, m, C):
        v = record['별점 수']
        R = record['별점']
        return ((v / (v + m)) * R) + ((m / (m + v)) * C)

    def calculate_weighted_ratings(self, percentile):
        m = self.data['별점 수'].quantile(percentile)
        C = self.data['별점'].mean()
        self.data['가중 별점'] = self.data.apply(self.weighted_vote_average, axis=1, args=(m, C))

    def find_similar_restaurant(self, title_name, top_n=10):
        rest_menu = self.data[self.data['업소명'] == title_name]
        rest_index = rest_menu.index.values
        self.data["유사도"] = self.menu_sim[rest_index, :].reshape(-1, 1)
        temp = self.data.sort_values(by=["유사도", "가중 별점"], ascending=False)
        temp = temp[temp.index.values != rest_index]
        final_index = temp.index.values[:top_n]
        return self.data.iloc[final_index]

    def display_recommendations(self, recommendations):
        sim_rest_df = pd.DataFrame(recommendations[['업소명', '별점', '유사도']])
        print("메뉴 유사도-가중 평점 고려 식당 추천")
        print(tabulate(sim_rest_df, headers='keys', tablefmt='fancy_outline'))

if __name__ == '__main__':
    recommender = RestaurantRecommender('./source.csv')
    recommender.preprocess_data()
    recommender.calculate_similarity()
    recommender.calculate_weighted_ratings(0.6)
    similar_restaurants = recommender.find_similar_restaurant('아키타', 10)
    recommender.display_recommendations(similar_restaurants)
