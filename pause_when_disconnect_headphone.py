# NOTE: only on Linux

from time import sleep
from subprocess import call


def check_headphone_connect():
    file = open('/proc/asound/card0/codec#0', 'r')
    info = file.read().split('\n')
    index = 0
    for line in info:
        if r"Node 0x03" in line:
            break
        index += 1
    return r"[0x00 0x00]" in info[index + 5]


while True:
    if check_headphone_connect():
        # pause audio
        call(["playerctl", "pause"])
    else:
        # resume audio
        call(["playerctl", "play"])
    sleep(0.1)

