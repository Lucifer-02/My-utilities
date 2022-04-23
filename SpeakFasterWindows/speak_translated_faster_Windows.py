from subprocess import check_output, Popen, PIPE
from gtts.tts import gTTS
import pyautogui
import pyperclip
from keyboard import wait
from translators import google


speed = 2.0


# translate selected text and read
def trans():
    pyautogui.hotkey('ctrl', 'c')
    text = pyperclip.paste()
    translated = google(text, "en", "vi")
    tts = gTTS(text=translated, lang='vi')
    p = Popen(['mpv', '--speed=' + str(speed), '--no-video', '-'], stdin=PIPE)
    tts.write_to_fp(p.stdin)
    p.stdin.close()
    p.wait()


shortkey = r"ctrl+`"
while True:
    wait(shortkey)
    trans()
