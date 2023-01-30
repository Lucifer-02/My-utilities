from subprocess import Popen, check_output, PIPE
from gtts.tts import gTTS
import psutil

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower() and proc.status() != 'zombie':
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

def handle():
    speed = 2.0

    text = check_output(['xsel'])
    translated = check_output(['crow', '-b', '-t', 'vi', text]).decode('utf-8')
    tts = gTTS(text=translated, lang='vi')
    p = Popen(['mpv', '--speed=' + str(speed), '--no-video', '-'], stdin=PIPE)
    tts.write_to_fp(p.stdin)
    p.stdin.close()
    p.wait()


if(checkIfProcessRunning('mpv') == True):
    Popen(['killall','mpv'])
else:
    handle()
