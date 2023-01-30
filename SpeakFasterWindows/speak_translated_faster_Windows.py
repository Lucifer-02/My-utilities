from subprocess import Popen, PIPE
from gtts.tts import gTTS
import pyautogui
import pyperclip
from keyboard import wait
from translators import translate_text
import multiprocessing
import os


# configs
speed = 2.0
shortkey = r"F9"

# kill prosses


def kill(pid: int) -> bool:
    try:
        os.kill(pid, 9)
    except OSError:
        return False
    else:
        return True


def get_text():
    pyautogui.hotkey('ctrl', 'c')
    return pyperclip.paste()

# translate selected text and read


def trans(text):
    return translate_text(text, translator='google', to_language='vi')


def tts_mpv(text):
    tts = gTTS(text=text, lang='vi')
    p = Popen(['mpv', '--speed=' + str(speed), '--no-video', '-'], stdin=PIPE)
    tts.write_to_fp(p.stdin)
    p.wait()


def tts_ffmpeg(text):
    tts = gTTS(text=text, lang='vi')
    p = Popen(['ffplay', '-af', 'atempo=' + str(speed),
              '-nodisp', '-autoexit'], stdin=PIPE)
    tts.write_to_fp(p.stdin)
    p.wait()


def run(prev_pid: int):
    if kill(prev_pid):
        print(f"killed {prev_pid}")
    else:
        tts_mpv(trans(get_text()))
        #  tts_ffmpeg(trans(get_text()))


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
