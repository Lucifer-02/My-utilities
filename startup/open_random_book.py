import os
from pathlib import Path

import numpy as np

from open_doc import open_pdf_with_edge, open_epub_with_reader


def main():
    # Path to the directory where the books are stored
    READING_PATH = Path("/media/lucifer/STORAGE/IMPORTANT/Books/READING/")

    # List all the files in the directory
    files = os.listdir(READING_PATH)

    # Open a random book
    random_book = np.random.choice(files)

    # get the file extension
    ext = os.path.splitext(random_book)[1]

    match ext:
        case ".pdf":
            open_pdf_with_chrome(READING_PATH / random_book)
        case ".epub":
            open_epub_with_reader(READING_PATH / random_book)
        case _:
            print("File format not supported.")


if __name__ == "__main__":
    main()
