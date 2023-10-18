#include <assert.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include <curl/curl.h>
#include <jansson.h>
#include <vlc/vlc.h>

#include "lib/common.h"
#include "lib/trans.h"
#include "lib/tts.h"

void trans(char *translation, char text[]) {

  assert(strlen(text) < TRANS_BUFFER_SIZE);

  char url[TRANS_BUFFER_SIZE];
  const Text source = {.data = text, .size = strlen(text)};
  TransParams params = {.client = "gtx",
                        .ie = "UTF-8",
                        .oe = "UTF-8",
                        .dt = "t",
                        .sl = "auto",
                        .tl = "vi"};
  genarate_trans_url(url, params, source);
  // printf("url: %s\n", url);

  char data[TRANS_BUFFER_SIZE];
  Text trans = {.data = data, .size = 0};
  request_api(&trans, url);
  // printf("Output: %s, size: %ld\n", trans.data, trans.size);
  parse_resp(translation, trans.data);
}

void tts(char *text, float speed) {

  assert(text != NULL);

  int text_len = strlen(text);
  assert(text_len < TTS_BUFFER_SIZE);
  assert(text_len != 0);

  char url[TTS_BUFFER_SIZE];
  const Text source = {.data = text, .size = text_len};
  TTSParams params = {.client = "gtx", .ie = "UTF-8", .tl = "vi"};

  const int limit = 250;
  char *pointer = source.data + 0;
  int size = source.size - 0;
  char data[TTS_BUFFER_SIZE];
  Text audio = {.data = data, .size = 0};

  while (size > 0) {

    const Text slice = tok(pointer, size, limit);
    // fwrite(slice.data, 1, slice.size, stdout);
    // printf("\n");
    // printf("\nlen: %d\n", slice.size);
    genarate_tts_url(url, params, slice);
    // printf("url: %s\n", url);
    pointer = slice.data + slice.size + 1;
    size -= slice.size + 1;

    // put all audio chunk together
    Text resp = {.data = data + audio.size,
                 .size = 0}; // resp also a slice to audio
    request_api(&resp, url);
    audio.size += resp.size;
    // printf("TTS: %s, size: %d\n", all.data, all.size);
  }

  MemAudioData mem = {.audio = audio.data, .size = audio.size, .pos = 0};
  play_audio(mem, speed);
}

int main(int argc, char *argv[]) {
  // char text[] =
  // "Xin chào";
  // "xin cam on, ban ten la gi?\0";
  // "how old are you?. What's your name?. Do you love me?. Let's go.";
  // "This line is a giveaway: you have named your script json. but "
  // "you are trying to import the builtin module called json, "
  // "?since your script is in the current directory, it comes first "
  // "in sys.path, and so that's the module that gets imported.";
  //
  if (argc < 2) {
    printf("Please run with arguments!!!\n");
    exit(0);
  }

  char translation[TRANS_BUFFER_SIZE];
  trans(translation, argv[1]);
  // printf("Translation: %s\n", translation);
  float speed = 2.0;
  tts(translation, speed);

  return 0;
}
