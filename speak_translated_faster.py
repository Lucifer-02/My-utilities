from myLib.copy import getText
from myLib.normalize_str import removeNewline, removeReturn
from myLib.translate import trans
from myLib.TTS import tts
from myLib.pidHandle import killPIDByName


def normalize_str(text: str) -> str:
    text = removeReturn(removeNewline(text))
    return text


def run(speed: float, player: str, tts_mode: str):
    # kill player if it is running
    if not killPIDByName(player):
        text = normalize_str(getText())
        print(text)
        translated = trans(
            source_lang="auto",
            target_lang="vi",
            source_text=text,
            translator="crow",
        )
        tts(text=translated, mode=tts_mode, player=player, speed=speed)


if __name__ == "__main__":
    # config_path = os.getenv("DATA_PATH", "") + "/My-utilities/config.json"
    # with open(config_path, "r") as file:
    #     config = json.load(file)["tts"]
    #     run(speed=config["speed"], player=config["player"], tts_mode=config["tts_mode"])

    run(speed=2.0, player="ffplay", tts_mode="online")
