import datetime
from subprocess import check_output
from pathlib import Path
import logging

import numpy as np
import platform
from termcolor import colored


# get content with xsel (linux) and check_output
def get_clipboard() -> str:
    return check_output("xsel").decode("utf-8")


def normalize_text(text: str) -> str:
    return text.lower().replace("\n", "").replace("\r", "").replace("\t", "")


def get_char_count(text: str, char: str) -> int:
    return text.count(char)


def write_to_file(
    file_path: Path, content: str, char: str, guess: int, answer: int
) -> None:
    with open(file_path, "a") as file:
        file.write(
            str(datetime.datetime.now())
            + ";"
            + content
            + ";"
            + char
            + ";"
            + str(guess)
            + ";"
            + str(answer)
            + "\n"
        )


def main():
    content = normalize_text(get_clipboard())

    # random char from a-z
    char = np.random.choice(list("abcdefghijklmnopqrstuvwxyz"))

    guess = input('Guess number of "' + colored(char, "black", "on_white") + '": ')
    # check gess only contains numbers
    while not guess.isnumeric():
        logging.error("Invalid input!")
        guess = input('Guess number of "' + colored(char, "black", "on_white") + '": ')

    answer = get_char_count(content, char)

    if int(guess) == answer:
        print(colored("Correct!", "black", "on_green"))
    else:
        print(colored("Wrong!", "black", "on_red"))

    print(
        colored(char, "black", "on_white")
        + " is: "
        + colored(str(answer), "black", "on_magenta")
    )

    # print content with highlighted char
    print("---------------------------------Content---------------------------------")
    print(content.replace(char, colored(char, "black", "on_white")))
    print("-------------------------------------------------------------------------")

    path = Path(__file__).parent / Path("data.csv")

    write_to_file(path, content, char, int(guess), answer)


if __name__ == "__main__":
    main()
    # press any key to exit
    print("Press any key to exit...")
    input()
