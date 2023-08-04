from subprocess import Popen, check_output, PIPE, call
from gtts.tts import gTTS

# import pyperclip

# configs
speed = 2.0
player = "ffplay"
tts_mode = "online"


def getText() -> bytes:
    return check_output(["xsel"])


# def getText() -> bytes:
#     call(["xdotool", "key", "ctrl+c"])
#     return pyperclip.paste().encode("utf-8")


def trans(text: bytes) -> str:
    return check_output(["crow", "-b", "-t", "vi", text]).decode("utf-8")


def tts(text, mode, player):
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
        p.wait()


def run():
    try:
        pid = (
            check_output(["pidof", "-s", player])
            .decode(encoding="utf8")
            .replace("\n", "")
        )
        call(["kill", pid])
    except:
        text = getText()
        translated = trans(text)
        tts(text=translated, mode=tts_mode, player=player)


def main():
    run()


if __name__ == "__main__":
    main()
