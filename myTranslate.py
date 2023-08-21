from subprocess import check_output

def trans(text: str) -> str:
    return check_output(["crow", "-b", "-t", "vi", text]).decode("utf-8")
