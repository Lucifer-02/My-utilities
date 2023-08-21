from gtts import gTTS
from subprocess import Popen, PIPE, call

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
        p.stdin.close()
        p.wait()

# def tts(text: str, mode: str, player: str, speed: int):
#     if mode == "offline":
#         call(["espeak-ng", "-vvi", text])
#     else:
#         tts = gTTS(text=text, lang="vi")
#         # uncomment this line to use mpv instead of ffplay below
#         if player == "mpv":
#             p = Popen(["mpv", "--speed=" + str(speed), "--no-video", "-"], stdin=PIPE)
#         else:
#             p = Popen(
#                 [
#                     "ffplay",
#                     "-af",
#                     "atempo=" + str(speed),
#                     "-v",
#                     "quiet",
#                     "-nodisp",
#                     "-autoexit",
#                     "-",
#                 ],
#                 stdin=PIPE,
#             )
#         tts.write_to_fp(p.stdin)
#         p.stdin.close()
#         print("tts pid: " + str(p.pid))
#
