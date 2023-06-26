import os
import multiprocessing


def open_book(book, browser):
    os.system("{} {}".format(browser, book))


def edit_book(book):
    os.system("masterpdfeditor5 {}".format(book))


def split_window(direction):
    os.system("xdotool key Super_L+{}".format(direction))


# main
if __name__ == "__main__":
    dir_path = "/media/lucifer/STORAGE/IMPORTANT/stats-practices/Stat/"

    p = multiprocessing.Process(
        target=open_book,
        args=(dir_path + "statistics-freedman_backup.pdf", "microsoft-edge"),
    )
    p.start()
    os.system("sleep 1")
    split_window("Left")

    edit_book(
        dir_path + "statistics-freedman.pdf",
    )
