from subprocess import Popen, check_output, PIPE, call
from gtts.tts import gTTS


speed = 2.0


def run():
    try:
        pid = check_output(["pidof", "-s", "mpv"]
                           ).decode(encoding='utf8').replace('\n', '')
        call(["kill", pid])
    except:
        text = check_output(['xsel'])
        translated = check_output(
            ['crow-translate', '-b', '-t', 'vi', text]).decode('utf-8')
        tts = gTTS(text=translated, lang='vi')

        # uncomment this line to use mpv instead of ffplay below
        p = Popen(['mpv', '--speed=' + str(speed),
                  '--no-video', '-'], stdin=PIPE)
        #  p = Popen(['ffmpeg', '-af', 'atempo=' + str(speed), '-v',
        #            'quiet', '-nodisp', '-autoexit', '-'], stdin=PIPE)
        tts.write_to_fp(p.stdin)
        p.stdin.close()
        p.wait()


if __name__ == "__main__":
    run()
