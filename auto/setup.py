import os
import json


def get_dir_path() -> str:
    try:
        path = os.environ["STATS_PATH"]
        return path
    except KeyError:
        print("Please set the environment variable STATS_PATH")
        exit(1)


# get all browsers installed
def get_browsers() -> list:
    browsers = (
        os.popen(
            "ls /usr/bin | grep -E 'firefox|chromium|brave|microsoft-edge|google-chrome'"
        )
        .read()
        .split("\n")
    )

    return [browser for browser in browsers if browser != ""]


if __name__ == "__main__":
    result = {
        "stats_practices": {
            "Stats": {
                "book": get_dir_path() + "/statistics_freedman.pdf",
                "reader": "microsoft-edge",
            }
        }
    }

    # save result in json file
    with open("config.json", "w") as file:
        json.dump(result, file, indent=4)
