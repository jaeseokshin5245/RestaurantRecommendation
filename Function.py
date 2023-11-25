import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RestaurantRecommender:
    def __init__(self):
        self.data = pd.read_csv('./source.csv', encoding='cp949')

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
        self.data["유사도"] = self.menu_sim[rest_index, :].reshape(-1, 1) * 100
        temp = self.data.sort_values(by=["유사도", "가중 별점"], ascending=False)
        temp = temp[temp.index.values != rest_index]
        final_index = temp.index.values[:top_n]
        final_index = self.data.iloc[final_index]
        return final_index

    def display_recommendations(self, recommendations):
        sim_title = recommendations[['업소명']]
        sim_point = recommendations[['별점']]
        sim_pointnum = recommendations[['유사도']]
        sim_menu = recommendations[['메뉴']]
        sim_num = recommendations[['별점 수']]
        
        info_list = [sim_title, sim_point, sim_pointnum, sim_menu, sim_num]
        list_count = 0
        result_array = []

        for ls in info_list:
            temp_array = ls.to_string(index=False)
            temp_array = temp_array.split('\n')
            temp_array = temp_array[1:]
            temp_array = [s.lstrip() for s in temp_array]
            if list_count == 2:
                temp_array = [t[:-7] for t in temp_array]
            elif list_count == 3:
                temp_array[0].split(',')
            list_count += 1
            result_array.append(temp_array)
        return result_array[0], result_array[1], result_array[2], result_array[3], result_array[4]    

if __name__ == '__main__':
    recommender = RestaurantRecommender()
    recommender.preprocess_data()
    recommender.calculate_similarity()
    recommender.calculate_weighted_ratings(0.6)
    similar_restaurants = recommender.find_similar_restaurant('쌍둥이네 떡볶이', 10)
    result = recommender.display_recommendations(similar_restaurants)
