import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,  QGridLayout
from PyQt5.QtGui import QIcon, QPixmap, QFont
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

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowProperties()
        self.main_grid()
        self.show()
        
    def setWindowProperties(self):
        self.setWindowTitle('Foodstagram')
        self.setWindowIcon(QIcon("./sources/Ficon.png"))
        self.setStyleSheet("background-color: white;")
        self.setGeometyAndSize()
        self.setFonts()
        
    def setGeometyAndSize(self):
        self.screen_geometry = app.desktop().screenGeometry()
        x = int(self.screen_geometry.width() * 0.4)
        y = int(self.screen_geometry.height() * 0.2)
        self.move(x, y)
        self.setFixedSize(523, 750)   
        
    def setFonts(self):
        self.gen_font = QFont("Instagram Sans", 12)
        self.gen_font.setBold(False)
        
        self.bold_font = QFont("Instagram Sans", 12)
        self.bold_font.setBold(True)
        
    def main_grid(self):
        main_grid = QGridLayout()
        main_grid.setSpacing(3)   

        main_grid.addLayout(self.TitleSubLayout(), 0, 0)
        main_grid.addLayout(self.ImageSubLayout(), 1, 0)
        main_grid.addLayout(self.ShareSubLayout(), 2, 0)
        main_grid.addLayout(self.LikesSubLayout(), 3, 0)
        main_grid.addLayout(self.CommentSubLayout(), 4, 0)
        main_grid.addLayout(self.AddCommentSubLayout(), 5, 0)
        main_grid.addLayout(self.HashtagSubLayout(), 6, 0)
        main_grid.addLayout(self.RecentSubLayout(), 7, 0)
        
        self.setLayout(main_grid)
    
    def TitleSubLayout(self):
        
        dots_label = QLabel()
        dots_icon = QIcon("./sources/dots.png")  
        dots_label.setPixmap(dots_icon.pixmap(64, 64))
        
        profile_label = QLabel()
        profile_icon = QIcon("./sources/profile.png")  
        profile_label.setPixmap(profile_icon.pixmap(64, 64))
        
        blank_label = QLabel()
        blank_icon = QIcon("./sources/blank.png")  
        blank_label.setPixmap(blank_icon.pixmap(64, 64))

        profile_name = QLabel("Content Based Recommendation")
        profile_name.setFont(self.bold_font)
        
        Title_layout = QGridLayout()
        Title_layout.addWidget(profile_label, 0, 0)
        Title_layout.addWidget(profile_name, 0, 1)
        Title_layout.addWidget(blank_label, 0, 2)
        Title_layout.addWidget(blank_label, 0, 3)
        Title_layout.addWidget(blank_label, 0, 4)
        Title_layout.addWidget(blank_label, 0, 5)
        Title_layout.addWidget(dots_label, 0, 6)
        
        return Title_layout
    
    def ImageSubLayout(self):
        Image_layout = QGridLayout()
        image_label = QLabel()
        
        pixmap = QPixmap("./sources/sample.png")
        image_label.setPixmap(pixmap)
        image_label.setGeometry(0, 0, 512, 512)
        Image_layout.addWidget(image_label, 0, 0)
        
        return Image_layout
    
    def ShareSubLayout(self):
        
        blank_label = QLabel()
        blank_icon = QIcon("./sources/blank.png")  
        blank_label.setPixmap(blank_icon.pixmap(64, 64))
        
        heart_label = QLabel()
        heart_icon = QIcon("./sources/heart.png")  
        heart_label.setPixmap(heart_icon.pixmap(64, 64))
        
        send_label = QLabel()
        send_icon = QIcon("./sources/send.png")  
        send_label.setPixmap(send_icon.pixmap(64, 64))
        
        comment_label = QLabel()
        comment_icon = QIcon('./sources/comment.png')  
        comment_label.setPixmap(comment_icon.pixmap(64, 64))
        
        bm_label = QLabel()
        bm_icon = QIcon("./sources/bm.png")  
        bm_label.setPixmap(bm_icon.pixmap(64, 64))
        
        share_layout = QGridLayout()
        share_layout.addWidget(heart_label, 0, 0)
        share_layout.addWidget(send_label, 0, 1)
        share_layout.addWidget(comment_label, 0, 2)
        share_layout.addWidget(blank_label, 0, 3)
        share_layout.addWidget(blank_label, 0, 4)
        share_layout.addWidget(blank_label, 0, 5)
        share_layout.addWidget(blank_label, 0, 6)
        share_layout.addWidget(blank_label, 0, 7)
        share_layout.addWidget(blank_label, 0, 8)
        share_layout.addWidget(blank_label, 0, 9)
        share_layout.addWidget(bm_label, 0, 10)
        
        return share_layout
    
    def LikesSubLayout(self):
        likes_layout = QGridLayout() 
        likes_label = QLabel("000 Likes")
        likes_label.setFont(self.bold_font)
        likes_layout.addWidget(likes_label, 0, 0)
        
        return likes_layout
        
    def CommentSubLayout(self):
        blank_label = QLabel()
        blank_icon = QIcon("./sources/blank.png")  
        blank_label.setPixmap(blank_icon.pixmap(64, 64))
        
        comment_layout = QGridLayout()
        comment_label = QLabel("Content Based Recommendation")
        comment_label.setFont(self.bold_font)
        comment_layout.addWidget(comment_label, 0, 0)
        
        comment_content_label = QLabel("Hello world!")
        comment_content_label.setFont(self.gen_font)
        comment_layout.addWidget(comment_content_label, 0, 1)
        comment_layout.addWidget(blank_label, 0, 2)
        
        return comment_layout
        
    def AddCommentSubLayout(self):
        addcomment_layout = QGridLayout()
        addcomment_label = QLabel("See all 1,234 comments")
        addcomment_label.setStyleSheet("color: #868686;")
        addcomment_label.setFont(self.gen_font)
        addcomment_layout.addWidget(addcomment_label, 0, 0)
        
        return addcomment_layout
        
    def HashtagSubLayout(self):
        hashtag_layout = QGridLayout()
        hashtag_label = QLabel("#hashtag1 #hashtag2")
        hashtag_label.setStyleSheet("color: #2F729B;")
        hashtag_label.setFont(self.gen_font)
        hashtag_layout.addWidget(hashtag_label, 0, 0)
        
        return hashtag_layout
        
    def RecentSubLayout(self):
        recent_layout = QGridLayout()
        recent_label = QLabel("Uploaded 0 days ago")
        recent_label.setStyleSheet("color: #868686;")
        recent_label.setFont(QFont("Instagram Sans", 9))
        recent_layout.addWidget(recent_label, 0, 0)
        
        return recent_layout    
    
if __name__ == '__main__':
    recommender = RestaurantRecommender('./data_sources/source.csv')
    recommender.preprocess_data()
    recommender.calculate_similarity()
    recommender.calculate_weighted_ratings(0.6)
    similar_restaurants = recommender.find_similar_restaurant('아키타', 10)
    recommender.display_recommendations(similar_restaurants)
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())