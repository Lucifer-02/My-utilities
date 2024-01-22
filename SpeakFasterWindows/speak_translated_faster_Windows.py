from subprocess import Popen, PIPE
import multiprocessing
import os

from gtts.tts import gTTS
import pyautogui
import pyperclip
from keyboard import wait
from translators import translate_text

from myLib.copy import getText
from myLib.normalize_str import removeNewline, removeReturn
from myLib.translate import trans
from myLib.TTS import tts
from myLib.pidHandle import killPIDByName


# configs
speed = 2.0
shortkey = r"F9"


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


# translate selected text and read
# def trans(text: str) -> str:
#     result = translate_text(text, translator="google", to_language="vi")
#     if isinstance(result, dict):
#         return "None"
#
#     return result


def tts_mpv(text: str) -> None:
    tts = gTTS(text=text, lang="vi")
    p = Popen(["mpv", "--speed=" + str(speed), "--no-video", "-"], stdin=PIPE)
    tts.write_to_fp(p.stdin)
    p.wait()


def tts_ffmpeg(text: str) -> None:
    tts = gTTS(text=text, lang="vi")
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
    if p.stdin is not None:
        p.stdin.close()
        p.wait()
    # p.wait()


def run(prev_pid: int):
    if kill(prev_pid):
        print(f"killed {prev_pid}")
    else:
        text = normalize_str(getText())
        # tts_mpv(trans(get_text()))
        # tts_ffmpeg(trans(get_text()))
        translated = trans(
            source_lang="en",
            target_lang="vi",
            source_text=text,
            translator="api",
        )
        tts_ffmpeg(translated)


def main():
    prev_pid = 0
    while True:
        wait(shortkey)
        p = multiprocessing.Process(target=run, args=(prev_pid,))
        p.start()
        prev_pid = p.pid

    #  wait(shortkey)
    #  run(0)


if __name__ == "__main__":
    main()
