com:
	# gcc trans.c -o trans -lcurl -ljansson 
	# -Wall -Wextra
	# gcc json.c -o json -ljansson -Wall -Wextra
	gcc tts.c -o tts -lcurl -lvlc 
	# gcc -o convert convert.c -l
	# gcc -o encode encode.c -lcurl
	# gcc audio.c -o audio -lvlc

clean:
	rm trans json tts audio out.folded perf.data perf.data.old out.perf out.svg

run: com
	clear
	# ./json
	# python3 test.py
	# ./trans
	./tts
	# ./audio 
	# ./convert
	# ./encode

perf: 
	sudo perf record -F 99 -a -g ./tts && perf script > out.perf && ../../../FlameGraph/stackcollapse-perf.pl out.perf > out.perf && perf script > out.perf && ../../../FlameGraph/stackcollapse-perf.pl out.perf > out.folded && ../../../FlameGraph/flamegraph.pl out.folded > out.svg && microsoft-edge out.svg
