from myLib.copy import getText
from myLib.normalize_str import removeNewline, removeReturn
from myLib.translate import trans
from myLib.TTS import tts
from myLib.pidHandle import killPIDByName


def run(speed: float, player: str, tts_mode: str):
    # kill player if it is running
    if not killPIDByName(player):
        text = getText()
        translated = trans(removeReturn(removeNewline(text)))
        tts(text=translated, mode=tts_mode, player=player, speed=speed)


if __name__ == "__main__":
    # configs
    speed = 2.0
    player = "ffplay"
    tts_mode = "online"
    run(speed=speed, player=player, tts_mode=tts_mode)
