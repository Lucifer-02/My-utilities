from subprocess import Popen, PIPE, call, check_output
from multiprocessing import Process
from pathlib import Path

from gtts import gTTS


class MyTTS:
    def __init__(self, text: str, engine: str) -> None:
        self.engine = engine
        match engine:
            case "crow":
                self.audio = gTTS(text=text, lang="vi")
            case "my_lang_tool":
                # TODO: only using tts module
                TTS_PATH = Path(
                    f"/media/lucifer/STORAGE/IMPORTANT/My-utilities/myLib/{engine}"
                )
                assert TTS_PATH.is_file()
                self.audio = check_output(
                    [
                        str(TTS_PATH),
                        str(0),
                        "2",
                        text if len(text) > 0 else "No text",
                    ],
                )

    def write_to_stdin(self, p):
        match self.engine:
            case "crow":
                assert isinstance(self.audio, gTTS)
                self.audio.write_to_fp(p.stdin)
            case "my_lang_tool":
                assert isinstance(self.audio, bytes)
                p.stdin.write(self.audio)


def tts(text: str, mode: str, player: str, speed: float, engine: str):
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
                    "--no-video",
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


# create new process to run tts independently from the main process and get return value frome tts function
def tts_process(text: str, mode: str, player: str, speed: float) -> int | None:
    p = Process(target=tts, args=(text, mode, player, speed))
    p.start()
    return p.pid
