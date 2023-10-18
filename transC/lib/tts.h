#ifndef TTS_H
#define TTS_H

#include "common.h"

#include <vlc/vlc.h>

#define TTS_BUFFER_SIZE 1048576 // 1Mb

typedef struct {
  char *client;
  char *ie; // input encode
  char *tl; // output encode
} TTSParams;

typedef struct {
  char *audio; // pointer to audio in memory
  size_t size;
  size_t pos; // for callback
} MemAudioData;

void genarate_tts_url(char *url, const TTSParams params, Text text);
void play_audio(MemAudioData mem, float speed);

#endif
