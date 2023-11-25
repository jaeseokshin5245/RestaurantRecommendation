import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

class ImageSwipeInstant(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Image Swipe Instant')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Set up the layout
        layout = QVBoxLayout(central_widget)

        # Create a QLabel instance for displaying the images
        self.image_label = QLabel(self)
        layout.addWidget(self.image_label)

        # Load two sample images
        self.image_paths = ['image1.jpg', 'image2.jpg']
        self.current_image_index = 0
        self.load_image()

        self.show()

    def load_image(self):
        # Load the current image into the QLabel
        pixmap = QPixmap(self.image_paths[self.current_image_index])
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def keyPressEvent(self, event):
        # Handle left arrow key press for switching to the previous image
        if event.key() == Qt.Key_Left:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_paths)
            self.load_image()

        # Handle right arrow key press for switching to the next image
        if event.key() == Qt.Key_Right:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
            self.load_image()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageSwipeInstant()
    sys.exit(app.exec_())
