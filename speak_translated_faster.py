from myLib.copy import getText
from myLib.normalize_str import normalize_input
from myLib.translate import trans
from myLib.TTS import tts
from myLib.pidHandle import killPIDByName


def run(speed: float, player: str, tts_mode: str, engine: str):
    # kill player if it is running
    if not killPIDByName(player):
        text = normalize_input(getText())
        translated = trans(
            source_lang="auto",
            target_lang="vi",
            source_text=text,
            translator="google_new",
        )
        tts(text=translated, mode=tts_mode, player=player, speed=speed, engine=engine)


if __name__ == "__main__":
    # config_path = os.getenv("DATA_PATH", "") + "/My-utilities/config.json"
    # with open(config_path, "r") as file:
    #     config = json.load(file)["tts"]
    #     run(speed=config["speed"], player=config["player"], tts_mode=config["tts_mode"])

    run(speed=2.0, player="mpv", tts_mode="online", engine="new_lang_tool")
