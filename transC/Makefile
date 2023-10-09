com:
	# gcc trans.c ./lib/yyjson.c -o trans -lcurl 
	# gcc trans.c -o trans -lcurl -ljansson 
	# -Wall -Wextra
	# gcc json.c -o json -ljansson -Wall -Wextra
	# gcc tts.c -o tts -lcurl -lpthread -lm -lSDL2
	# gcc -o audio audio.c -lavformat -lavcodec -lswresample -lSDL2 -lavutil -lm
	gcc -g -o audio audio.c -lvlc 

clean:
	# rm trans 
	# rm json
	# rm tts
	rm audio

run: com
	clear
	# ./json
	# python3 test.py
	# ./trans
	# ./tts
	./audio 
