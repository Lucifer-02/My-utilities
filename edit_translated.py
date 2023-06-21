# create a window to edit text and a button copy text to clipboard using PySide6 and can auto adapt to the size of the text
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QGridLayout,
    QTextEdit,
    QSlider,
    QLabel,
    QSpinBox,
    QSizePolicy,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import QSize, Qt, Slot
from subprocess import check_output, call, Popen, PIPE
from gtts.tts import gTTS
import sys
import os
from multiprocessing import Process
import pyperclip


def getText() -> str:
    return check_output(["xsel"]).decode("utf-8")


def align(string, width):
    length = len(string)
    if length <= width or width <= 10:
        return string

    lines = []
    start = 0
    end = width
    while end < length:
        index = nearest_space_index(string, end)
        lines.append(string[start:index])
        start = index + 1
        end = start + width

    if start < length:
        lines.append(string[start:])

    return "\n".join(lines)


# normalize text, remove new line
def normalize(text) -> str:
    return text.replace("\n", " ").replace("\r", " ").replace("  ", " ")


def nearest_space_index(string, index):
    left = string.rfind(" ", 0, index)
    right = string.find(" ", index)

    if left == -1:
        return right
    if right == -1:
        return left

    return left if index - left <= right - index else right


def trans(text) -> str:
    return check_output(["crow", "-b", "-t", "vi", text]).decode("utf-8")


def tts(text, mode, player, speed):
    if mode == "offline":
        call(["espeak-ng", "-vvi", text])
    else:
        tts = gTTS(text=text, lang="vi")
        # uncomment this line to use mpv instead of ffplay below
        if player == "mpv":
            p = Popen(["mpv", "--speed=" + str(speed), "--no-video", "-"], stdin=PIPE)
        else:
            p = Popen(
                [
                    "ffplay",
                    "-af",
                    "atempo=" + str(speed),
                    "-v",
                    "quiet",
                    "-nodisp",
                    "-autoexit",
                    "-",
                ],
                stdin=PIPE,
            )
        tts.write_to_fp(p.stdin)
        p.stdin.close()
        print("tts pid: " + str(p.pid))


# check pid of the process
def killed_pid(pid: int) -> bool:
    if pid == 0:
        return False
    try:
        os.kill(pid, 2)
        print("process " + str(pid) + " is running")
        return True
    except:
        print("process " + str(pid) + " is not running")
        return False


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


class Window(QWidget):
    speed = 1.5
    player = "ffplay"
    tts_mode = "online"
    tts_pid = [0, 0]
    font_size = 13
    line_size = 70

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # set the window size and title
        self.setGeometry(900, 300, 900, 450)
        self.setWindowTitle("Edit translation")

        self.trans = align(trans(normalize(getText())), self.line_size)

        # create textbox to edit text with default text
        self.text_edit = QTextEdit(self)
        self.text_edit.setFont(QFont("Arial", self.font_size))
        self.text_edit.setText(self.trans)
        # adjust the size of the textbox to fit the text
        self.text_edit.adjustSize()

        # create copy button in green color
        self.copy_button = QPushButton("Copy", self)
        self.copy_button.setFont(QFont("Arial", 20))
        self.copy_button.clicked.connect(self.copy_close)
        self.copy_button.setFixedSize(QSize(120, 60))
        self.copy_button.setStyleSheet("background-color: green")

        self.speak_button = QPushButton("Speak", self)
        self.speak_button.setFont(QFont("Arial", 20))
        self.speak_button.clicked.connect(self.speak)
        self.speak_button.setFixedSize(QSize(120, 60))

        # add a horizontal slider to change the speed
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(10)
        self.speed_slider.setMaximum(30)
        self.speed_slider.setValue(int(self.speed * 10))
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.speed_slider.valueChanged.connect(self.update_speed)

        # add a label to show the speed continuously
        self.speed_label = QLabel("Speed: " + str(self.speed), self)
        self.speed_label.setFont(QFont("Arial", 15))

        # add a box with minus and plus button to change font size
        self.font_size_box = QSpinBox()
        self.font_size_box.setMaximum(30)
        self.font_size_box.setMinimum(5)
        self.font_size_box.setValue(13)
        self.font_size_box.setFixedSize(QSize(90, 60))
        self.font_size_box.valueChanged.connect(self.update_font_size)

        # add label to show the font size
        self.font_size_label = QLabel("Font size:")
        self.font_size_label.setFont(QFont("Arial", 14))

        # add a box with minus and plus button to change line size
        self.line_size_box = QSpinBox()
        self.line_size_box.setMaximum(100)
        self.line_size_box.setMinimum(9)
        self.line_size_box.setValue(self.line_size)
        self.line_size_box.setSingleStep(2)
        self.line_size_box.setFixedSize(QSize(90, 60))
        self.line_size_box.valueChanged.connect(self.update_line_size)

        # add label to show the line size
        self.line_size_label = QLabel("Line size:")
        self.line_size_label.setFont(QFont("Arial", 14))

        # create a grid layout
        self.grid = QGridLayout(self)
        self.grid.addWidget(self.text_edit, 1, 0, 1, 4)
        self.grid.addWidget(self.copy_button, 3, 0, 1, 1)
        self.grid.addWidget(self.speak_button, 3, 1, 1, 1)
        self.grid.addWidget(self.font_size_box, 3, 2, 1, 1)
        self.grid.addWidget(self.line_size_box, 3, 3, 1, 1)
        self.grid.addWidget(self.speed_slider, 4, 1, 1, 1)
        self.grid.addWidget(self.speed_label, 4, 0, 1, 1)
        self.grid.addWidget(self.font_size_label, 2, 2, 1, 1)
        self.grid.addWidget(self.line_size_label, 2, 3, 1, 1)

    @Slot()
    def update_line_size(self):
        size = self.line_size_box.value()
        self.text_edit.setText(align(normalize(self.trans), size))

    @Slot()
    def update_font_size(self):
        size = self.font_size_box.value()
        if size > 0:
            self.text_edit.setFont(QFont("Arial", size))

    @Slot()
    def update_speed(self):
        self.speed = float(self.speed_slider.value()) / 10
        self.speed_label.setText("Speed: " + str(self.speed))

    @Slot()
    def copy_close(self):
        print("copy")
        # copy the text in textbox to clipboard the close the app
        # self.clipboard = QApplication.clipboard()
        # self.clipboard.setText(self.text_edit.toPlainText())
        pyperclip.copy(self.text_edit.toPlainText())
        killed_pid(self.tts_pid[0])
        killed_pid(self.tts_pid[1])
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
                text=self.trans,
                mode=self.tts_mode,
                player=self.player,
                speed=self.speed,
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
