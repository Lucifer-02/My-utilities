from subprocess import Popen, check_output, PIPE
from gtts.tts import gTTS

speed = 2.0

text = check_output(['xsel'])
translated = check_output(['crow', '-b', '-t', 'vi', text]).decode('utf-8')
tts = gTTS(text=translated, lang='vi')
p = Popen(['mpv', '--speed=' + str(speed), '--no-video', '-'], stdin=PIPE)
tts.write_to_fp(p.stdin)
p.stdin.close()
p.wait()
