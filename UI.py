from PyQt5.QtWidgets import QApplication, QWidget, QLabel,  QGridLayout
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt
import sys

from Function import RestaurantRecommender
from resources.load_main import SplashScreen

class MyApp(QWidget):

    def __init__(self, splash_screen):
        super().__init__()
        self.splash_screen = splash_screen
        self.initUI()

    def initUI(self):
        self.image_paths = ['./studies/image1.jpg', './studies/image2.jpg',
                            './studies/image3.jpg', './studies/image4.jpg',
                            './studies/image5.jpg', './studies/image6.jpg',
                            './studies/image7.jpg', './studies/image8.jpg',
                            './studies/image9.jpg', './studies/image10.jpg',
                            ]
        self.info_image_index = 0
        
        self.setWindowProperties()
        self.simulate_loading()
        self.pro_processing()    
        self.Main_grid()
        self.splash_screen.hide_splash()
        self.current_image_index = 0
        self.load_image()
        
        self.likes_label = self.LikesSubLayout(self.result_pointnum[self.info_image_index])
        self.main_grid.addLayout(self.likes_label, 3, 0)
        
        self.comment_label = self.CommentSubLayout(self.result_title[self.info_image_index])
        self.main_grid.addLayout(self.comment_label, 4, 0)
        
        self.addcomment_label = self.AddCommentSubLayout(self.result_num[self.info_image_index])
        self.main_grid.addLayout(self.addcomment_label, 5, 0)
        
        self.hashtag_label = self.HashtagSubLayout(
            self.menus_list[self.info_image_index][0],
            self.menus_list[self.info_image_index][1],
            self.menus_list[self.info_image_index][2],
            self.menus_list[self.info_image_index][3],
            self.menus_list[self.info_image_index][4],
            )
        
        self.main_grid.addLayout(self.hashtag_label, 6, 0)
        
        self.recent_label = self.RecentSubLayout(self.info_image_index)
        self.main_grid.addLayout(self.recent_label, 7, 0)

        self.show()

    def simulate_loading(self):
        total_steps = 100
        for i in range(total_steps):
            progress_value = int((i / total_steps) * 100)
            self.splash_screen.set_progress(progress_value)
            QApplication.processEvents()
            import time
            time.sleep(0.05)
        
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

    def pro_processing(self):
        recommender = RestaurantRecommender()
        recommender.preprocess_data()
        recommender.calculate_similarity()
        recommender.calculate_weighted_ratings(0.6)
        similar_restaurants = recommender.find_similar_restaurant('아키타', 10)
        result = recommender.display_recommendations(similar_restaurants)
        
        self.result_title, self.result_point, self.result_pointnum, result_menus, self.result_num = result
        self.menus_list = [menu.split(',') for menu in result_menus]
        
        return self.result_title, self.result_point, self.result_pointnum, self.menus_list, self.result_num
        
    def Main_grid(self):
        self.main_grid = QGridLayout()
        self.main_grid.setSpacing(3)   
        self.setLayout(self.main_grid)
        self.main_grid.addLayout(self.TitleSubLayout(), 0, 0)
        self.main_grid.addLayout(self.ImageSubLayout(), 1, 0)
        self.main_grid.addLayout(self.ShareSubLayout(), 2, 0)

        likes_layout = self.LikesSubLayout(self.result_pointnum[self.info_image_index])
        self.main_grid.addLayout(likes_layout, 3, 0)
        
        comment_layout = self.CommentSubLayout(self.result_title[self.info_image_index])
        self.main_grid.addLayout(comment_layout, 4, 0)
        
        addcomment_layout = self.AddCommentSubLayout(self.result_num[self.info_image_index])
        self.main_grid.addLayout(addcomment_layout, 5, 0)

        hashtag_layout = self.HashtagSubLayout(
            self.menus_list[self.info_image_index][0],
            self.menus_list[self.info_image_index][1],
            self.menus_list[self.info_image_index][2],
            self.menus_list[self.info_image_index][3],
            self.menus_list[self.info_image_index][4]
        )
        
        self.main_grid.addLayout(hashtag_layout, 6, 0)
        
        recent_layout = self.RecentSubLayout(self.info_image_index)
        self.main_grid.addLayout(recent_layout, 7, 0)

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
        
        self.pixmap = QPixmap()
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setGeometry(0, 0, 600, 800)
        self.image_layout.addWidget(self.image_label, 0, 0)
        
        return self.image_layout
    
    def load_image(self):
        self.pixmap = QPixmap(self.image_paths[self.info_image_index])
        self.image_label.setPixmap(self.pixmap)

    def update_info(self, increment=True):
        if increment and self.info_image_index < 9:
            self.info_image_index += 1
        elif not increment and self.info_image_index > 0:
            self.info_image_index -= 1
        
        likes_layout = self.LikesSubLayout(self.result_pointnum[self.info_image_index])
        comment_layout = self.CommentSubLayout(self.result_title[self.info_image_index])
        addcomment_layout = self.AddCommentSubLayout(self.result_num[self.info_image_index])
        hashtag_layout = self.HashtagSubLayout(
            self.menus_list[self.info_image_index][0],
            self.menus_list[self.info_image_index][1],
            self.menus_list[self.info_image_index][2],
            self.menus_list[self.info_image_index][3],
            self.menus_list[self.info_image_index][4]
        )
        recent_layout = self.RecentSubLayout(self.info_image_index)
        
        layout_item = self.main_grid.itemAtPosition(3, 0)
        if layout_item:
            existing_layout = layout_item.layout()
            if existing_layout:
                self.main_grid.removeItem(existing_layout)

        self.main_grid.addLayout(likes_layout, 3, 0)
        self.main_grid.addLayout(comment_layout, 4, 0)
        self.main_grid.addLayout(addcomment_layout, 5, 0)
        self.main_grid.addLayout(hashtag_layout, 6, 0)
        self.main_grid.addLayout(recent_layout, 7, 0)
        
        likes_label = likes_layout.itemAtPosition(0, 0).widget()
        likes_value = self.result_pointnum[self.info_image_index]
        self.updateLikesText(likes_label, likes_value)   
        
        comment_content_label = comment_layout.itemAtPosition(0, 1).widget()
        comment_value = self.result_title[self.info_image_index]
        self.updateCommentText(comment_content_label, comment_value)

        addcomment_label = addcomment_layout.itemAtPosition(0, 0).widget()
        addcomment_value = self.result_num[self.info_image_index]
        self.updateAddCommText(addcomment_label, addcomment_value)
        
        hashtag_label = hashtag_layout.itemAtPosition(0, 0).widget()
        hashtag_value = [self.menus_list[self.info_image_index][0],
                         self.menus_list[self.info_image_index][1],
                         self.menus_list[self.info_image_index][2],
                         self.menus_list[self.info_image_index][3],
                         self.menus_list[self.info_image_index][4]
                         ]
        self.updateHashtagText(hashtag_label, hashtag_value[0], 
                               hashtag_value[1],
                               hashtag_value[2],
                               hashtag_value[3],
                               hashtag_value[4])
        
        recent_label = recent_layout.itemAtPosition(0, 0).widget()
        recent_value = self.info_image_index
        self.updateRecentText(recent_label, recent_value)
        
        self.pixmap = QPixmap(self.image_paths[self.info_image_index])
        self.image_label.setPixmap(self.pixmap)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.load_image()
            self.update_info(False)

        if event.key() == Qt.Key_Right:
            self.load_image()
            self.update_info()
        
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
        likes_label = QLabel("{} likes".format(sim))
        likes_label.setFont(self.bold_font)
        likes_layout.addWidget(likes_label, 0, 0)
        
        self.updateLikesText(likes_label, sim)

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
        
        self.updateCommentText(comment_content_label, rest_title)
        
        return comment_layout
        
    def AddCommentSubLayout(self, rate_num):
        addcomment_layout = QGridLayout()
        addcomment_label = QLabel("See all  {} comments".format(rate_num))
        addcomment_label.setStyleSheet("color: #868686;")
        addcomment_label.setFont(self.gen_font)
        addcomment_layout.addWidget(addcomment_label, 0, 0)
        
        self.updateAddCommText(addcomment_label, rate_num)
        
        return addcomment_layout
        
    def HashtagSubLayout(self, menu_1, menu_2, menu_3, menu_4, menu_5):
        hashtag_layout = QGridLayout()
        hashtag_label = QLabel("#{} #{} #{} #{} #{}".format(menu_1, menu_2, menu_3, menu_4, menu_5))
        hashtag_label.setStyleSheet("color: #2F729B;")
        hashtag_label.setFont(self.gen_font)
        hashtag_layout.addWidget(hashtag_label, 0, 0)
        
        self.updateHashtagText(hashtag_label, menu_1, menu_2, menu_3, menu_4, menu_5)
        
        return hashtag_layout
        
    def RecentSubLayout(self, rank):
        recent_layout = QGridLayout()
        recent_label = QLabel("Uploaded {} days ago".format(str(int(rank)+1)))
        recent_label.setStyleSheet("color: #868686;")
        recent_label.setFont(QFont("Instagram Sans", 9))
        recent_layout.addWidget(recent_label, 0, 0)
        
        self.updateRecentText(recent_label, rank)
        
        return recent_layout
    
    def updateLikesText(self, label, sim):
        label.setText("{} likes".format(sim))
        
    def updateCommentText(self, label, rest_title):
        label.setText("{}".format(rest_title))
        
    def updateAddCommText(self, label, rate_num):
        label.setText("See all {} comments".format(rate_num))
        
    def updateHashtagText(self, label, menu_1, menu_2, menu_3, menu_4, menu_5):
        label.setText("#{} #{} #{} #{} #{}".format(menu_1, menu_2, menu_3, menu_4, menu_5))
        
    def updateRecentText(self, label, rank):
        label.setText("Uploaded {} days ago".format(str(int(rank)+1)))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    ex = MyApp(splash)
    sys.exit(app.exec_())