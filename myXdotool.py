from subprocess import call


def press_key(key: str):
    call(["xdotool", "key", key])


def focus_window(pid: int):
    call(["xdotool", "windowfocus", str(pid)])
