from subprocess import Popen, PIPE, call, check_output
from multiprocessing import Process
from pathlib import Path
import os

from gtts import gTTS


class MyTTS:
    def __init__(self, text: str, engine: str = "my_lang_tool") -> None:
        self.engine = engine
        match engine:
            case "crow":
                self.audio = gTTS(text=text, lang="vi")
            case "my_lang_tool" | "main.exe":
                # TODO: only using tts module
                SPEED = "0"  # not need speed
                MODE = "2"
                TTS_LINUX_PATH = Path(
                    f"/media/lucifer/STORAGE/IMPORTANT/My-utilities/myLib/{engine}"
                )
                TTS_WINDOWS_PATH = Path(f"D:\\IMPORTANT\\My-utilities\\myLib\\{engine}")
                TTS_PATH = TTS_LINUX_PATH if os.name == "posix" else TTS_WINDOWS_PATH
                assert TTS_PATH.is_file()

                self.audio = check_output(
                    [
                        str(TTS_PATH),
                        SPEED,
                        MODE,
                        text if len(text) > 0 else "No text",
                    ],
                )

    def write_to_stdin(self, p):
        match self.engine:
            case "crow":
                assert isinstance(self.audio, gTTS)
                self.audio.write_to_fp(p.stdin)
            case "my_lang_tool" | "main.exe":
                assert isinstance(self.audio, bytes)
                p.stdin.write(self.audio)
            case _:
                raise ValueError(f"Not support {self.engine} engine!")


def tts(text: str, mode: str, player: str, speed: float, engine: str = "my_lang_tool"):
    if mode == "offline":
        call(["espeak-ng", "-vvi", text])
        exit()

    tts = MyTTS(text, engine=engine)

    # uncomment this line to use mpv instead of ffplay below
    match player:
        case "mpv":
            p = Popen(
                [
                    "mpv",
                    "--speed=" + str(speed),
                    "--really-quiet",
                    "-",
                ],
                stdin=PIPE,
            )
            tts.write_to_stdin(p)
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
            tts.write_to_stdin(p)
            if p.stdin is not None:
                p.stdin.close()
                p.wait()
        case _:
            raise ValueError("Not support this player!")


# create new process to run tts independently from the main process and get return value frome tts function
def tts_process(text: str, mode: str, player: str, speed: float) -> int | None:
    p = Process(target=tts, args=(text, mode, player, speed))
    p.start()
    return p.pid
