from gtts import gTTS
from subprocess import Popen, PIPE, call
from multiprocessing import Process


def tts(text: str, mode: str, player: str, speed: float):
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
        if p.stdin is not None:
            p.stdin.close()
            p.wait()


# create new process to run tts independently from the main process and get return value frome tts function
def tts_process(text: str, mode: str, player: str, speed: float) -> int | None:
    p = Process(target=tts, args=(text, mode, player, speed))
    p.start()
    return p.pid
