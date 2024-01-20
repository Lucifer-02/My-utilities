import os
from time import sleep
from subprocess import call


def read_book(book, reader):
    call([reader, book])


# create new tab with tilte in xfce4-terminal
def new_tab_with_cmd(title, cmd):
    call(["xfce4-terminal", "--tab", "--title", title, "-e", cmd, "--hold"])


def new_tab(title):
    call(["xfce4-terminal", "--tab", "--title", title])


def type_run_cmd(cmd):
    call(["xdotool", "type", cmd])
    call(["xdotool", "key", "Return"])


def press(key: str):
    call(["xdotool", "key", key])


def change_dir(path):
    type_run_cmd("cd {}".format(path))


def translate_book(render_cmd, watch_cmd, edit_cmd):
    new_tab("edit")
    type_run_cmd(edit_cmd)
    new_tab_with_cmd("render", render_cmd)
    new_tab_with_cmd("watch", watch_cmd)


def split_window(on: str):
    os.system("xdotool key Super_L+{}".format(on))


def get_dir_path() -> str:
    try:
        path = os.environ["DATA_PATH"]
        return path
    except KeyError:
        print("Please set the environment variable DATA_PATH")
        exit(1)


# main
if __name__ == "__main__":
    # dir_path = "/media/lucifer/STORAGE/IMPORTANT/stats-practices/Stat"
    dir_path = get_dir_path() + "/stats-practices/Stat"
    book_path = dir_path + "/book.pdf"
    translate_path = dir_path + "/translate"

    print(f"{book_path} and {translate_path}")

    render_cmd = r"mdbook serve --open " + translate_path
    watch_cmd = r"mdbook watch " + translate_path
    edit_cmd = "cd " + translate_path + "/src"

    translate_book(
        render_cmd=render_cmd,
        watch_cmd=watch_cmd,
        edit_cmd=edit_cmd,
    )
    sleep(1)
    read_book(book=book_path, reader="microsoft-edge")
    sleep(1.5)
    press("Super_L+Left")
    sleep(1)

    # return to edit
    press("alt+Tab")
    sleep(0.5)
    press("alt+2")
    sleep(0.5)
    press("Super_L+Right")
