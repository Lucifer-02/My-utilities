from subprocess import call, check_output
from gtts.tts import gTTS

speed = 2.0

text = check_output(['xsel'])
translated = check_output(['crow', '-b', '-t', 'vi', text])
tts = gTTS(translated.decode('utf8'), lang='vi')
tts.save('out.mp3')
call(['mpv', '--speed=' + str(speed), '--no-video', 'out.mp3'])
