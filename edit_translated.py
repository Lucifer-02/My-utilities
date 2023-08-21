# create a window to edit text and a button copy text to clipboard using PySide6 and can auto adapt to the size of the text
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QGridLayout,
    QTextEdit,
    QSlider,
    QLabel,
    QSpinBox,
    QDialog,
    QStatusBar,
    QCheckBox,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import QSize, Qt, Slot
from subprocess import check_output, call
import sys
from multiprocessing import Process
import json
from my_copy import getText
from normalize_str import removeNewline, removeSpace, removeReturn
from myTTS import tts
from myPIDHandle import killed_pid, getPID
from myTranslate import trans


def normalize(text: str) -> str:
    text = removeSpace(removeReturn(removeNewline(text)))
    return text


def get_pid(name: str):
    try:
        return int(
            check_output(["pidof", "-s", name]).decode("utf-8").strip().split(" ")[0]
        )
    except:
        return 0


# create new process to run tts independently from the main process and get return value frome tts function
def tts_process(text, mode, player, speed) -> int:
    p = Process(target=tts, args=(text, mode, player, speed))
    p.start()
    return int(p.pid)


def press_key(key: str):
    call(["xdotool", "key", key])


def focus_window(pid: int):
    call(["xdotool", "windowfocus", str(pid)])


class Window(QDialog):
    speed = 0
    player = ""
    tts_mode = ""
    tts_pid = [0, 0]
    font_size = 0
    editor_window_id = 0

    def __init__(self, config):
        super().__init__()
        self.speed = config["speed"]
        self.player = config["player"]
        self.tts_mode = config["tts_mode"]
        self.font_size = config["font_size"]
        self.editor_window_id = config["editor_window_id"]
        self.initUI()

    def initUI(self):
        # set the window size and title
        self.setGeometry(900, 300, 750, round(750 / 1.618))
        self.setWindowTitle("Edit translation")

        self.text = normalize(getText())
        self.trans = trans(self.text)

        # create textbox to edit text with default text
        self.text_edit = QTextEdit(self)
        self.text_edit.setFont(QFont("Arial", self.font_size))
        # set background color to Solarized dark
        self.text_edit.setStyleSheet(
            "background-color: #002b36; color: #839496; border: 1px solid #586e75"
        )
        self.text_edit.setText(self.trans)

        # create copy button in green color
        self.copy_button = QPushButton("Copy", self)
        self.copy_button.setFont(QFont("Ubuntu", 20))
        self.copy_button.clicked.connect(self.copy_content)
        self.copy_button.setFixedSize(QSize(100, round(100 / 1.618)))
        self.copy_button.setStyleSheet("background-color: green")

        self.speak_button = QPushButton("Speak", self)
        self.speak_button.setFont(QFont("Ubuntu", 14))
        self.speak_button.clicked.connect(self.speak)
        self.speak_button.setFixedSize(QSize(60, round(60 / 1.618)))

        self.close_button = QPushButton("Close", self)
        self.close_button.setFont(QFont("Ubuntu", 20))
        self.close_button.clicked.connect(self.close_window)
        self.close_button.setFixedSize(QSize(100, round(100 / 1.618)))
        self.close_button.setStyleSheet("background-color: red")

        # add reset button to reset the content
        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setFont(QFont("Ubuntu", 20))
        self.reset_button.clicked.connect(self.reset_content)
        self.reset_button.setFixedSize(QSize(100, round(100 / 1.618)))
        self.reset_button.setStyleSheet("background-color: orange")

        # add a horizontal slider to change the speed
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(10)
        self.speed_slider.setMaximum(30)
        self.speed_slider.setValue(int(self.speed * 10))
        self.speed_slider.setTickInterval(1)
        self.speed_slider.valueChanged.connect(self.update_speed)

        # add a label to show the speed continuously
        self.speed_label = QLabel("Speed: " + str(self.speed), self)
        self.speed_label.setFont(QFont("Ubuntu", 15))

        # add a box with minus and plus button to change font size
        self.font_size_box = QSpinBox()
        self.font_size_box.setMaximum(20)
        self.font_size_box.setMinimum(5)
        self.font_size_box.setValue(13)
        self.font_size_box.setFixedSize(QSize(60, round(60 / 1.618)))
        self.font_size_box.valueChanged.connect(self.update_font_size)

        # add label to show the font size
        self.font_size_label = QLabel("Font:")
        self.font_size_label.setFont(QFont("Ubuntu", 14))

        # add a checkbox to diable/enable change font size
        self.font_size_checkbox = QCheckBox()

        # add status bar to resize the window
        self.statusbar = QStatusBar()

        # create a grid layout
        self.grid = QGridLayout(self)
        self.grid.addWidget(self.text_edit, 1, 0, 1, 9)
        self.grid.addWidget(self.copy_button, 3, 0, 1, 1)
        self.grid.addWidget(self.close_button, 3, 1, 1, 1)
        self.grid.addWidget(self.speed_slider, 2, 1, 1, 1)
        self.grid.addWidget(self.speak_button, 2, 2, 1, 1)
        self.grid.addWidget(self.reset_button, 3, 2, 1, 1)

        self.grid.addWidget(self.font_size_box, 3, 5, 1, 2)

        self.grid.addWidget(self.speed_label, 2, 0, 1, 1)
        self.grid.addWidget(self.font_size_label, 2, 5, 1, 1)
        self.grid.addWidget(self.font_size_checkbox, 2, 6, 1, 1)
        self.grid.addWidget(self.font_size_checkbox, 2, 6, 1, 1)
        self.grid.addWidget(self.statusbar, 4, 8, 1, 1)

    @Slot()
    def reset_content(self):
        self.text_edit.setText(self.trans)

    @Slot()
    def update_font_size(self):
        size = self.font_size_box.value()
        if size > 0:
            self.text_edit.setFont(QFont("Ubuntu", size))

    @Slot()
    def update_speed(self):
        self.speed = float(self.speed_slider.value()) / 10
        self.speed_label.setText("Speed: " + str(self.speed))

    @Slot()
    def copy_content(self):
        print("copy")
        # copy the text in textbox to clipboard
        self.clipboard = QApplication.clipboard()
        self.clipboard.setText(self.text_edit.toPlainText())

    @Slot()
    def close_window(self):
        killed_pid(self.tts_pid[0])
        killed_pid(self.tts_pid[1])

        # # focus to editor window
        # focus_window(self.editor_window_id)
        #
        # press_key("Escape")
        # press_key("shift+g")
        # # paste content
        # press_key("p")

        self.close()

    @Slot()
    def speak(self):
        print("speak")

        self.tts_pid[0] = get_pid(self.player)

        if self.tts_pid[0]:
            killed_pid(self.tts_pid[0])
            killed_pid(self.tts_pid[1])
        else:
            self.tts_pid[1] = tts_process(
                text=self.text_edit.toPlainText(),
                mode=self.tts_mode,
                player=self.player,
                speed=self.speed,
            )


if __name__ == "__main__":
    with open("/media/lucifer/DATA/My-utilities/config.json") as file:
        config = json.load(file)

    if config["editor_window_id"] == 0:
        print("Config editor PID first")
        exit()

    app = QApplication(sys.argv)
    window = Window(config)
    window.show()
    sys.exit(app.exec())
