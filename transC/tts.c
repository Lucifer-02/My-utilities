#include <SDL2/SDL.h>
#include <assert.h>
#include <ctype.h>
#include <curl/curl.h>
#include <soundio/soundio.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER_SIZE 1048576 // 1Mb

// Struct to hold translated data and its size
typedef struct {
  char *data;
  size_t size;
} TTS;

typedef struct {
  char *client;
  char *ie;
  char *tl;
  char *q;
} TTSParams;

// Callback function to handle received data
size_t write_data(void *buffer, size_t size, size_t nmemb, TTS *tts) {
  // size_t written = fwrite(buffer, size, nmemb, userp);
  size_t written = size * nmemb;
  memcpy(tts->data + tts->size, buffer, written);
  tts->size += written;
  return written;
}

// Function to perform translation request using Google Translate API
void request_tts(TTS *tts, const char *url) {
  assert(tts != NULL);
  assert(url != NULL);

  CURL *curl = curl_easy_init();
  if (curl) {

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, tts);

    CURLcode res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
      fprintf(stderr, "curl_easy_perform() failed: %s\n",
              curl_easy_strerror(res));
    }
    curl_easy_cleanup(curl);
  }
  assert(tts->data != NULL);
  assert(tts->size != 0);
  printf("Output: %s, size: %ld\n", tts->data, strlen(tts->data));
}

void genarate_url(char *url, const char *base, const TTSParams params) {
  assert(base != NULL);
  assert(params.client != NULL && params.ie != NULL && params.tl != NULL &&
         params.q != NULL);

  sprintf(url, "%s?client=%s&ie=%s&tl=%s&q=%s", base, params.client, params.ie,
          params.tl, params.q);
}

// replace all ' ' characters into '+'
char *normalize_text(char *text) {
  assert(text != NULL);

  for (int i = 0; text[i] != '\0'; i++) {
    if (isblank(text[i])) {
      text[i] = '+';
    }
  }
  return text;
}

int main() {
  char base[] = "https://translate.googleapis.com/translate_tts";
  char text[] = "how are you?. What's your name?. Do you love me?. Let's go.";
  // "This line is a giveaway: you have named your script json. but "
  // "you are trying to import the builtin module called json, "
  // "?since your script is in the current directory, it comes first "
  // "in sys.path, and so that's the module that gets imported.";

  assert(strlen(base) < BUFFER_SIZE);
  assert(strlen(text) < BUFFER_SIZE);

  char url[BUFFER_SIZE];
  normalize_text(text);
  TTSParams params = {
      .client = "gtx", .ie = "UTF-8", .tl = "en", .q = normalize_text(text)};
  genarate_url(url, base, params);
  printf("url: %s\n", url);

  char data[BUFFER_SIZE];
  TTS tts = {.data = data, .size = 0};
  request_tts(&tts, url);

  FILE *fp = fopen("audio.mp3", "wb");
  fwrite(tts.data, 1, tts.size, fp);
  fclose(fp);

  // ---------------------------------------

  return 0;
}
