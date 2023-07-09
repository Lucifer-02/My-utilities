from termcolor import colored
import datetime
from subprocess import check_output
import platform


# get content with xsel (linux) and check_output
def get_clipboard() -> str:
    return check_output("xsel").decode("utf-8")


def normalize_text(text) -> str:
    return text.lower().replace("\n", "").replace("\r", "").replace("\t", "")


def get_char_count(text, char) -> int:
    return text.count(char)


def write_to_file(file_path, content, char, gess, answer):
    with open(file_path, "a") as file:
        file.write(
            str(datetime.datetime.now())
            + ";"
            + content
            + ";"
            + char
            + ";"
            + str(gess)
            + ";"
            + str(answer)
            + "\n"
        )
    file.close()


def main():
    content = normalize_text(get_clipboard())

    char = input("Character to count: ")
    # check char only contains characters
    while not char.isalpha():
        print("Invalid input!")
        char = input("Character to count: ")

    gess = input('Guess number of "' + colored(char, "black", "on_white") + '": ')
    # check gess only contains numbers
    while not gess.isnumeric():
        print("Invalid input!")
        gess = input('Guess number of "' + colored(char, "black", "on_white") + '": ')

    answer = get_char_count(content, char)

    if int(gess) == answer:
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

    # ATTENTION: change path to your needs
    if platform.node() == "lap":
        path = "/media/lucifer/STORAGE/IMPORTANT/My-utilities/eng_prac/data.csv"
    else:
        path = "/media/lucifer/DATA/My-utilities/eng_prac/data.csv"

    write_to_file(path, content, char, gess, answer)
    # print("Data written to: " + path)


if __name__ == "__main__":
    main()
    # press any key to exit
    print("Press any key to exit...")
    input()
