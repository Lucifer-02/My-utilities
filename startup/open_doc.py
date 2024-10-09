from subprocess import Popen
from pathlib import Path


def open_pdf_with_chrome(file_path: Path, page_number: int = 1) -> None:
    url = f"file://{file_path}#page={page_number}"
    Popen(["google-chrome", url])


def open_epub_with_reader(file_path: Path) -> None:
    Popen(
        [
            "ebook-viewer",
            str(file_path),
        ]
    )
