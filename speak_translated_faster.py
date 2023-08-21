import my_copy
from normalize_str import removeNewline, removeReturn
from myTranslate import trans
from myTTS import tts
from myPIDHandle import killPID


def run(speed:float, player:str, tts_mode:str):
    # kill player if it is running
    if not killPID(player):
        text = my_copy.getText()
        translated = trans(removeReturn(removeNewline(text)))
        tts(text=translated, mode=tts_mode, player=player, speed=speed)

if __name__ == "__main__":
    # configs
    speed = 2.0
    player = "ffplay"
    tts_mode = "online"
    run(speed=speed, player=player, tts_mode=tts_mode)
