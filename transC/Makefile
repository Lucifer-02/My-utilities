com:
	# gcc trans.c -o trans -lcurl -ljansson 
	# -Wall -Wextra
	# gcc json.c -o json -ljansson -Wall -Wextra
	gcc tts.c -o tts -lcurl -lvlc
	# gcc -o audio audio.c -lSDL2
	# gcc -g -o audio audio.c -lvlc
	# gcc -o convert convert.c -l

clean:
	rm trans ; rm json ; rm tts ; rm audio

run: com
	clear
	# ./json
	# python3 test.py
	# ./trans
	./tts
	# ./audio 
	# ./convert
