# create a window to edit text and a button copy text to clipboard using pyqt5 and can auto adapt to the size of the text

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QTextEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QSize
from subprocess import check_output

def getText() -> str:
    return check_output(["xsel"]).decode("utf-8")

def trans(text) -> str:
    return check_output(["crow", "-b", "-t", "vi", text]).decode("utf-8")

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # set the window size and title
        self.setGeometry(1200, 300, 800, 400)
        self.setWindowTitle('Copy Text to Clipboard')

        # create textbox to edit text with default text
        self.text_edit = QTextEdit(self)
        self.text_edit.setFont(QFont('Arial', 12))
        self.text_edit.setText(trans(getText()))


        # create a button in green color
        self.button = QPushButton('Copy', self)
        self.button.setFont(QFont('Arial', 20))
        self.button.clicked.connect(self.copy_text)
        self.button.setFixedSize(QSize(150, 80))
        self.button.setStyleSheet("background-color: green")

        # create a grid layout
        self.grid = QGridLayout(self)
        self.grid.setSpacing(10)
        self.grid.addWidget(self.text_edit, 1, 0, 1, 2)
        self.grid.addWidget(self.button, 2, 0, 1, 2)

        # set the window layout
        self.setLayout(self.grid)

        # show the window
        self.show()

    def copy_text(self):
        # copy the text to clipboard the close the app
        self.clipboard = QApplication.clipboard()
        self.clipboard.setText(self.text_edit.toPlainText())
        self.close()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())


