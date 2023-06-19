# create a window to edit text and a button copy text to clipboard using PySide6 and can auto adapt to the size of the text
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QGridLayout,
    QTextEdit,
    QSlider,
    QLabel,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import QSize, Qt
from subprocess import check_output, call, Popen, PIPE
from gtts.tts import gTTS
import sys
import os
from multiprocessing import Process


def getText() -> bytes:
    return check_output(["xsel"])


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

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # set the window size and title
        self.setGeometry(900, 300, 900, 450)
        self.setWindowTitle("Edit translation")

        self.trans = trans(getText())

        # create textbox to edit text with default text
        self.text_edit = QTextEdit(self)
        self.text_edit.setFont(QFont("Arial", 13))
        self.text_edit.setText(self.trans)

        # create copy button in green color
        self.copy_button = QPushButton("Copy", self)
        self.copy_button.setFont(QFont("Arial", 20))
        self.copy_button.clicked.connect(self.copy_close)
        self.copy_button.setFixedSize(QSize(150, 80))
        self.copy_button.setStyleSheet("background-color: green")

        self.speak_button = QPushButton("Speak", self)
        self.speak_button.setFont(QFont("Arial", 20))
        self.speak_button.clicked.connect(self.speak)
        self.speak_button.setFixedSize(QSize(150, 80))

        # add a horizontal slider to change the speed
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(10)
        self.slider.setMaximum(30)
        self.slider.setValue(15)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.update_speed)

        # add a label to show the speed continuously
        self.speed_label = QLabel("Speed: " + str(self.speed), self)
        self.speed_label.setFont(QFont("Arial", 15))

        # create a grid layout
        self.grid = QGridLayout(self)
        self.grid.setSpacing(5)
        self.grid.addWidget(self.text_edit, 1, 0, 1, 3)
        self.grid.addWidget(self.copy_button, 2, 0, 1, 2)
        self.grid.addWidget(self.speak_button, 2, 1, 1, 2)
        self.grid.addWidget(self.slider, 3, 0, 1, 3)
        self.grid.addWidget(self.speed_label, 4, 0, 1, 3)

    def update_speed(self):
        self.speed = float(self.slider.value()) / 10
        self.speed_label.setText("Speed: " + str(self.speed))

    def copy_close(self):
        print("copy")
        # copy the text to clipboard the close the app
        self.clipboard = QApplication.clipboard()
        self.clipboard.setText(self.text_edit.toPlainText())
        killed_pid(self.tts_pid[0])
        killed_pid(self.tts_pid[1])
        self.close()

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
