import os
from time import sleep
import json
from subprocess import call


def read_book(book, reader):
    os.system("{} {}".format(reader, book))


def edit_book(book, cmd):
    os.system("{} {}".format(cmd, book))


# create new tab with tilte in xfce4-terminal
def new_tab_with_cmd(title, cmd):
    call(["xfce4-terminal", "--tab", "--title", title, "-e", cmd])


def new_tab(title):
    call(["xfce4-terminal", "--tab", "--title", title])


def run_cmd(cmd):
    call(["xdotool", "type", cmd])
    call(["xdotool", "key", "Return"])


def move_last_workspace():
    call(["xdotool", "key", "Super+End"])


def move_first_workspace():
    call(["xdotool", "key", "Super+Home"])


def change_dir(path):
    run_cmd("cd {}".format(path))


def translate_book(render_cmd, watch_cmd, edit_path):
    new_tab_with_cmd("render", render_cmd)
    new_tab_with_cmd("watch", watch_cmd)
    new_tab("edit")
    change_dir(edit_path)


def split_window(on: str):
    os.system("xdotool key Super_L+{}".format(on))


# main
if __name__ == "__main__":
    # load config
    with open("config.json", "r") as f:
        config = json.load(f)["stats_practices"]["Stats"]

    dir_path = "/media/lucifer/STORAGE/IMPORTANT/stats-practices/Stat"
    book_path = dir_path + "/Statistics-Freedman.pdf"
    translate_path = dir_path + "/translate"

    read_book(book=book_path, reader="microsoft-edge")
    sleep(1)
    split_window("Left")

    render_cmd = r"mdbook serve --open " + translate_path
    watch_cmd = r"mdbook watch " + translate_path
    edit_path = r"cd " + translate_path + "/src"
    translate_book(render_cmd=render_cmd, watch_cmd=watch_cmd, edit_path=edit_path)
