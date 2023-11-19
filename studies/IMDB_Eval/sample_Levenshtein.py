import pandas as pd
import warnings; warnings.filterwarnings('ignore')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tabulate import tabulate

def find_sim_menu(df, sim_martix, rest_name, top_n=5):

    rest_menu = df[df['업소명'] == rest_name]
    rest_index = rest_menu.index.values

    df['유사도'] = sim_martix[rest_index, :].reshape(-1, 1)

    temp = df.sort_values(by='유사도', ascending= False)
    final_index = temp.index.values[ : top_n]

    return df.iloc[final_index]

menus = pd.read_csv('./source.csv')

menus_df = menus[['업소명','대분류', '메뉴', '별점', '별점 수']]

pd.set_option('max_colwidth', 100)

menus_df['메뉴']  = menus_df['메뉴'].apply(lambda x : ('').join(x))

count_vec = CountVectorizer(min_df=0, ngram_range=(1,2))
menu_mat = count_vec.fit_transform(menus_df['메뉴'])

menu_sim = cosine_similarity(menu_mat, menu_mat)

smiliar_rest = find_sim_menu(menus_df, menu_sim, "아키타", 5)

sim_rest_df = pd.DataFrame(smiliar_rest[['업소명', '별점', '유사도']])

print("메뉴 유사도 고려 식당 추천")

print(tabulate(sim_rest_df, headers='keys', tablefmt='fancy_outline'))

# 가중 평점 고려 함수
percentile = 0.6 # 백분위 수 : 오름차순으로 60번 째 
m = menus_df['별점 수'].quantile(percentile)
C = menus_df['별점'].mean()

def weighted_vote_average(record):
    v = record['별점 수']
    R = record['별점']
    
    return ( (v/(v+m)) * R ) + ( (m/(m+v)) * C ) # IMDE 가중 평점 (차후에 디리클레로 변경할 것!)


menus_df['가중 별점'] = menus_df.apply(weighted_vote_average, axis=1)

temp = menus_df[['업소명','별점','별점 수','가중 별점']]

weighted_vote_df = pd.DataFrame(temp.sort_values('가중 별점', ascending=False)[:10])

print("가중 평점 고려 식당 추천")
print(tabulate(weighted_vote_df, headers='keys', tablefmt='fancy_outline'))


# 장르 유사도 및 가중 평점 모두 고려 함수
def find_sim_movie(df, sim_matrix, title_name, top_n=10):
    
    # 입력한 영화의 index
    rest_menu = df[df['업소명'] == title_name]
    rest_index = rest_menu.index.values
    
    # 입력한 영화의 유사도 데이터 프레임 추가
    df["유사도"] = sim_matrix[rest_index, :].reshape(-1,1)
        
    # 유사도와 가중 평점순으로 높은 상위 index 추출 (자기 자신 제거)
    temp = df.sort_values(by=["유사도", "가중 별점"], ascending=False)
    temp = temp[temp.index.values != rest_index]
    
    final_index = temp.index.values[:top_n]
    
    return df.iloc[final_index]

smiliar_rest = find_sim_movie(menus_df, menu_sim, '아키타', 10)

sim_rest_df = pd.DataFrame(smiliar_rest[['업소명', '별점', '유사도']])

print("메뉴 유사도-가중 평점 고려 식당 추천")
print(tabulate(sim_rest_df, headers='keys', tablefmt='fancy_outline'))