from subprocess import CalledProcessError, check_output, call
import os


def getPID(player: str) -> int:
    try:
        return int(
            check_output(["pidof", "-s", player])
            .decode(encoding="utf8")
            .replace("\n", "")
        )
    except CalledProcessError:
        return 0


# kill pid of player and raise exception if player is not running
def killPIDByName(player: str) -> bool:
    pid = getPID(player)
    if pid != 0:
        call(["kill", str(pid)])
        return True
    else:
        return False


# check pid of the process
def killPIDByID(pid: int) -> bool:
    if pid == 0:
        return False
    try:
        os.kill(pid, 2)
        print("process " + str(pid) + " is running")
        return True
    except:
        print("process " + str(pid) + " is not running")
        return False
