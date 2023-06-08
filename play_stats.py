import webbrowser
import os
import multiprocessing


def open_book(book, browser="firefox"):
    webbrowser.get(browser).open(book)


def open_jupyter():
    os.system(
        "jupyter-lab /run/media/lucifer/STORAGE/IMPORTANTS/Documents/STATISTICS/EleStat/practices/"
    )


def split_window(direction):
    os.system("xdotool key Super_L+{}".format(direction))


# main
if __name__ == "__main__":
    # create new process for jupyter-lab
    p = multiprocessing.Process(target=open_jupyter)
    p.start()

    # wait for jupyter-lab to start
    os.system("sleep 5")

    split_window("Right")

    open_book(
        "/run/media/lucifer/STORAGE/IMPORTANTS/Documents/STATISTICS/EleStat/sanet.st-Elementary_Statistics_14th_Edition.pdf",
        browser="firefox",
    )

    # open book for answer
    open_book(
        "/run/media/lucifer/STORAGE/IMPORTANTS/Documents/STATISTICS/EleStat/sanet.st-Elementary_Statistics_14th_Edition.pdf",
        browser="firefox",
    )

    split_window("Left")
