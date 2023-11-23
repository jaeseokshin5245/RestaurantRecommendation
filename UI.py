import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,  QGridLayout
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from Function import RestaurantRecommender

recommender = RestaurantRecommender()
recommender.preprocess_data()
recommender.calculate_similarity()
recommender.calculate_weighted_ratings(0.6)
similar_restaurants = recommender.find_similar_restaurant('쌍둥이네 떡볶이', 10)
result = recommender.display_recommendations(similar_restaurants)

result_title, result_point, result_pointnum = result

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
        self.setWindowIcon(QIcon("./resources/Ficon.png"))
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
        main_grid.addLayout(self.LikesSubLayout(result_pointnum[0]), 3, 0)
        main_grid.addLayout(self.CommentSubLayout(result_title[0]), 4, 0)
        main_grid.addLayout(self.AddCommentSubLayout(), 5, 0)
        main_grid.addLayout(self.HashtagSubLayout(), 6, 0)
        main_grid.addLayout(self.RecentSubLayout(), 7, 0)
        
        self.setLayout(main_grid)
    
    def TitleSubLayout(self):
        
        dots_label = QLabel()
        dots_icon = QIcon("./resources/dots.png")  
        dots_label.setPixmap(dots_icon.pixmap(64, 64))
        
        profile_label = QLabel()
        profile_icon = QIcon("./resources/profile.png")  
        profile_label.setPixmap(profile_icon.pixmap(64, 64))
        
        blank_label = QLabel()
        blank_icon = QIcon("./resources/blank.png")  
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
        self.image_layout = QGridLayout()
        self.image_label = QLabel()
        
        self.pixmap = QPixmap("./studies/image1.jpg")
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setGeometry(0, 0, 512, 512)
        self.image_layout.addWidget(self.image_label, 0, 0)
        
        return self.image_layout
    
    def keyPressEvent(self, event):
        # Handle left arrow key press for switching to the previous image
        if event.key() == Qt.Key_Left:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_paths)
            self.load_image()

        # Handle right arrow key press for switching to the next image
        if event.key() == Qt.Key_Right:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
            self.load_image()

    
    def load_image(self):
        self.pixmap = QPixmap(self.image_path[self.current_image_index])
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setScaledContents(True)

    
    def ShareSubLayout(self):
        
        blank_label = QLabel()
        blank_icon = QIcon("./resources/blank.png")  
        blank_label.setPixmap(blank_icon.pixmap(64, 64))
        
        heart_label = QLabel()
        heart_icon = QIcon("./resources/heart.png")  
        heart_label.setPixmap(heart_icon.pixmap(64, 64))
        
        send_label = QLabel()
        send_icon = QIcon("./resources/send.png")  
        send_label.setPixmap(send_icon.pixmap(64, 64))
        
        comment_label = QLabel()
        comment_icon = QIcon('./resources/comment.png')  
        comment_label.setPixmap(comment_icon.pixmap(64, 64))
        
        bm_label = QLabel()
        bm_icon = QIcon("./resources/bm.png")  
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
    
    def LikesSubLayout(self, sim):
        likes_layout = QGridLayout() 
        likes_label = QLabel("{} % similiar with your previous restaurant".format(sim))
        likes_label.setFont(self.bold_font)
        likes_layout.addWidget(likes_label, 0, 0)
        
        return likes_layout
        
    def CommentSubLayout(self, rest_title):
        blank_label = QLabel()
        blank_icon = QIcon("./resources/blank.png")  
        blank_label.setPixmap(blank_icon.pixmap(64, 64))
        
        comment_layout = QGridLayout()
        comment_label = QLabel("Content Based Recommendation")
        comment_label.setFont(self.bold_font)
        comment_layout.addWidget(comment_label, 0, 0)
        
        comment_content_label = QLabel("{}".format(rest_title))
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
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())