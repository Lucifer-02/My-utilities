from subprocess import Popen, PIPE
import multiprocessing
import os

from gtts.tts import gTTS
import pyautogui
import pyperclip
from keyboard import wait

from myLib.normalize_str import removeNewline, removeReturn
from myLib.translate import trans
from myLib.TTS import tts


def normalize_str(text: str) -> str:
    text = removeReturn(removeNewline(text))
    return text


# kill prosses
def kill(pid: int) -> bool:
    try:
        os.kill(pid, 9)
    except OSError:
        return False
    else:
        return True


def get_text():
    pyautogui.hotkey("ctrl", "c")
    return pyperclip.paste()


def run(prev_pid: int):
    if kill(prev_pid):
        print(f"killed {prev_pid}")
    else:
        text = normalize_str(get_text())
        translated = trans(
            source_lang="en",
            target_lang="vi",
            source_text=text,
            translator="api",
        )
        tts(
            text=translated,
            mode="online",
            player="ffmpeg",
            speed=2.0,
        )


def main():
    # configs
    hotkey = r"F9"

    prev_pid = 0
    while True:
        wait(hotkey)
        p = multiprocessing.Process(target=run, args=(prev_pid,))
        p.start()
        prev_pid = p.pid


if __name__ == "__main__":
    main()
