CC = gcc
WARNING +=	-Wall -Wextra 

LINKLIBS +=	-lvlc -ljansson -lcurl
INCLUDED +=	./lib/tts.c ./lib/trans.c ./lib/common.c

SOURCE = main
SOURCE_CODE = $(SOURCE).c
OUTPFILE += $(SOURCE)

clean:
	clear
	rm main

debug:
	$(CC) -g $(SOURCE_CODE) $(INCLUDED) -o $(OUTPFILE) $(LINKLIBS) $(WARNING)

release:
	$(CC) -O2 $(SOURCE_CODE) $(INCLUDED) -o $(OUTPFILE) $(LINKLIBS) -DNDEBUG

run: release
	./main "In this paper, we introduce TimeGPT, the first foundation model for time series, capable of generating accurate predictions for diverse datasets not seen during training. We evaluate our pre-trained model against established statistical, machine learning, and deep learning methods, demonstrating that TimeGPT zero-shot inference excels in performance, efficiency, and simplicity. Our study provides compelling evidence that insights from other domains of artificial intelligence can be effectively applied to time series analysis. We conclude that large-scale time series models offer an exciting opportunity to democratize access to precise predictions and reduce uncertainty by leveraging the capabilities of contemporary advancements in deep learning."
	
