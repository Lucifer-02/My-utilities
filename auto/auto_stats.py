import os
from time import sleep
from subprocess import call


def read_book(book, reader):
    # os.system("{} {}".format(reader, book))
    call([reader, book])


# create new tab with tilte in xfce4-terminal
def new_tab_with_cmd(title, cmd): 
    call(["xfce4-terminal", "--tab", "--title", title, "-e", cmd, "--hold"]) 

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


def translate_book(render_cmd, watch_cmd, edit_cmd):
    new_tab("edit")
    run_cmd(edit_cmd)
    new_tab_with_cmd("render", render_cmd)
    new_tab_with_cmd("watch", watch_cmd)


def split_window(on: str):
    os.system("xdotool key Super_L+{}".format(on))


def get_dir_path() -> str:
    try:
        path = os.environ["STATS_PATH"]
        return path
    except KeyError:
        print("Please set the environment variable STATS_PATH")
        exit(1)

# main
if __name__ == "__main__":
    # dir_path = "/media/lucifer/STORAGE/IMPORTANT/stats-practices/Stat"
    dir_path = get_dir_path() + "/Stat"
    book_path = dir_path + "/Statistics-Freedman.pdf"
    translate_path = dir_path + "/translate"

    render_cmd = r"mdbook serve --open " + translate_path
    watch_cmd = r"mdbook watch " + translate_path
    edit_cmd = "cd " + translate_path + "/src"

    translate_book(render_cmd=render_cmd, watch_cmd=watch_cmd, edit_cmd=edit_cmd)
    sleep(1)
    read_book(book=book_path, reader="microsoft-edge")
    sleep(2)
    split_window("Left")

