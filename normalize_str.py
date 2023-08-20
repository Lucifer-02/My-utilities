def removeNewline(text: str) -> str:
    result = text.replace("\n", " ")
    return result

def removeReturn(text: str) -> str:
    result = text.replace("\r", " ")
    return result


def removeSpace(text) -> str:
    return text.strip()


def align(string: str, width: int) -> str:
    length = len(string)
    if length <= width or width <= 10:
        return string

    lines = []
    start = 0
    end = width
    while end < length:
        index = _nearest_space_index(string, end)
        lines.append(string[start:index])
        start = index + 1
        end = start + width

    if start < length:
        lines.append(string[start:])

    return "\n".join(lines)


def _nearest_space_index(string: str, index: int) -> int:
    left = string.rfind(" ", 0, index)
    right = string.find(" ", index)

    if left == -1:
        return right
    if right == -1:
        return left

    return left if index - left <= right - index else right


def addIndent(text: str, num: int) -> str:
    return " " * num + text
