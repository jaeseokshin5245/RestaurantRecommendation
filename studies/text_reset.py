import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.label = QLabel(self)
        self.label.setText("Press Enter to Reset Text")

        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

        self.setGeometry(300, 300, 300, 100)
        self.setWindowTitle('Text Reset on Enter Key Press')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.label.clear()
            self.load_new_text()


    def load_new_text(self):
        self.label.setText("This is new text!")
        # self.layout.addWidget(self.label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
