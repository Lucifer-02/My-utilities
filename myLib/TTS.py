from subprocess import Popen, PIPE, call
from multiprocessing import Process
from pathlib import Path

from gtts import gTTS


def tts(text: str, mode: str, player: str, speed: float):
    if mode == "offline":
        call(["espeak-ng", "-vvi", text])
    else:
        tts = gTTS(text=text, lang="vi")
        # uncomment this line to use mpv instead of ffplay below
        match player:
            case "mpv":
                p = Popen(
                    ["mpv", "--speed=" + str(speed), "--no-video", "-"], stdin=PIPE
                )
                tts.write_to_fp(p.stdin)
                if p.stdin is not None:
                    p.stdin.close()
                    p.wait()
            case "ffplay":
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
            case "my_tts":
                # TODO: only using tts module
                TTS_PATH = Path(
                    f"/media/lucifer/STORAGE/IMPORTANT/My-utilities/myLib/{player}"
                )
                assert TTS_PATH.is_file()
                call([str(TTS_PATH), text if len(text) > 0 else "No text"])
            case _:
                raise ValueError(f"Not support {player} player")


# create new process to run tts independently from the main process and get return value frome tts function
def tts_process(text: str, mode: str, player: str, speed: float) -> int | None:
    p = Process(target=tts, args=(text, mode, player, speed))
    p.start()
    return p.pid
