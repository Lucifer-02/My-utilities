com:
	# gcc trans.c -o trans -lcurl -ljansson 
	# -Wall -Wextra
	# gcc json.c -o json -ljansson -Wall -Wextra
	gcc tts.c -o tts -lcurl -lvlc -O3
	# gcc -o convert convert.c -l
	# gcc -o encode encode.c -lcurl
	# gcc audio.c -o audio -lvlc

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
	# ./encode
