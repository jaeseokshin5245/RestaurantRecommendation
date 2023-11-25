from PyQt5.QtWidgets import QSplashScreen, QVBoxLayout, QProgressBar
from PyQt5.QtGui import QPixmap

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet("QProgressBar {"
                                        "border: 2px solid grey;"
                                        "border-radius: 5px;"
                                        "text-align: center;"
                                        "}"
                                        "QProgressBar::chunk {"
                                        "background-color: #53EA53;"  
                                        "}")
        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def set_progress(self, value):
        self.progress_bar.setValue(value)

    def hide_splash(self):
        self.hide()
