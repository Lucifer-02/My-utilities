from subprocess import call, check_output
import pyperclip


def getText() -> str:
    text = check_output(["xsel"], shell=True).decode("utf-8")
    print(text)
    return text


# def getText() -> str:
#     call(["xdotool", "key", "ctrl+c"])
#     return pyperclip.paste().decode("utf-8")
