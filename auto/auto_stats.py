import os
from time import sleep
import json


def read_book(book, browser):
    os.system("{} {}".format(browser, book))


def edit_book(book):
    os.system("masterpdfeditor5 {}".format(book))


def split_window(on: str):
    os.system("xdotool key Super_L+{}".format(on))


# main
if __name__ == "__main__":
    # load config
    with open("config.json", "r") as f:
        config = json.load(f)["stats_practices"]["Stats"]

    read_book(book=config["backup_book"], browser=config["browser"])
    sleep(1)
    split_window("Left")
    edit_book(book=config["edit_book"])
