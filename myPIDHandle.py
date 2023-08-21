from subprocess import CalledProcessError, check_output, call
import os


def getPID(player: str) -> str | None:
    try:
        return (
            check_output(["pidof", "-s", player])
            .decode(encoding="utf8")
            .replace("\n", "")
        )
    except CalledProcessError:
        print("Player is not running")
        return None


# kill pid of player and raise exception if player is not running
def killPID(player: str) -> bool:
    pid = getPID(player)
    if pid is not None:
        call(["kill", pid])
        return True
    else:
        return False


# check pid of the process
def killed_pid(pid: int) -> bool:
    if pid == 0:
        return False
    try:
        os.kill(pid, 2)
        print("process " + str(pid) + " is running")
        return True
    except:
        print("process " + str(pid) + " is not running")
        return False
