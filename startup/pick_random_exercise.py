from pathlib import Path
from subprocess import run

import polars as pl
import numpy as np

from open_doc import open_pdf_with_edge


def send_notify(title: str, message: str):
    run(["notify-send", title, message])


def main():
    # Path to the directory where the books are stored
    BOOK_PATH = Path("/media/lucifer/STORAGE/IMPORTANT/Books/READING/book.pdf")

    # get list exercises
    df = pl.read_csv(Path(__file__).parent / "exercises.csv")

    # pick a random exercise set in first column
    row = df.sample(1)
    page = row["page"][0]
    exercise = np.random.choice(range(1, row["numExercises"][0] + 1))

    # # send notification
    title = "🖕🏾"
    msg = f"Exercise: {exercise}, page: {page}"
    send_notify(title, msg)

    open_pdf_with_edge(BOOK_PATH, page_number=page)


if __name__ == "__main__":
    main()
