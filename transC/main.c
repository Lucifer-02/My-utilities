#include <assert.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include <curl/curl.h>
#include <jansson.h>
#include <vlc/vlc.h>

#define TRANS_BUFFER_SIZE 8192
#define TTS_BUFFER_SIZE 1048576 // 1Mb

typedef struct {
  char *client;
  char *ie;
  char *tl;
} TTSParams;

typedef struct {
  char *client;
  char *ie;
  char *oe;
  char *dt;
  char *sl;
  char *tl;
} TransParams;

typedef struct {
  char *audio; // pointer to audio in memory
  size_t bytes;
  size_t pos;
} MemAudioData;

// Struct to hold translated data and its size
typedef struct {
  char *data;
  size_t size;
} Text;

// Callback function to handle received data
size_t write_data(const void *ptr, size_t size, size_t nmemb, Text *resp) {
  assert(resp->data != NULL);
  // assert(size < TRANS_BUFFER_SIZE);

  size_t new_size = resp->size + size * nmemb;
  memcpy(resp->data + resp->size, ptr, size * nmemb);
  resp->size = new_size;
  resp->data[resp->size] = '\0';
  return size * nmemb;
}

// Function to perform translation request using Google Translate API
void request_api(Text *output, const char *url) {
  CURL *curl = curl_easy_init();
  if (curl) {
    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, output);
    CURLcode res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
      fprintf(stderr, "curl_easy_perform() failed: %s\n",
              curl_easy_strerror(res));
    }
    curl_easy_cleanup(curl);
  }
  assert(output->data != NULL);
  assert(output->size != 0);
}

void url_encode(const Text text, char *output) {

  assert(output != NULL);
  assert(text.size != 0);
  assert(text.data != NULL);

  int pos = 0;

  for (int i = 0; i < text.size; i++) {
    unsigned char ch = text.data[i];

    // printf("char: %02x\n", ch);

    if (('A' <= ch && ch <= 'Z') || ('a' <= ch && ch <= 'z') ||
        ('0' <= ch && ch <= '9')) {
      output[pos++] = ch;
    } else if (ch == ' ') {
      output[pos++] = '+';
    } else if (ch == '-' || ch == '_' || ch == '.' || ch == '!' || ch == '~' ||
               ch == '*' || ch == '\'' || ch == '(' || ch == ')') {
      output[pos++] = ch;
    } else {
      sprintf(output + pos, "%%%02X", ch);
      pos += 3;
    }
  }

  output[pos++] = '\0'; // Null-terminate the encoded string
}

void genarate_trans_url(char *url, const TransParams params, Text text) {
  const char base[] = "https://translate.googleapis.com/translate_a/single";
  assert(params.client != NULL && params.ie != NULL && params.oe != NULL &&
         params.dt != NULL && params.sl != NULL && params.tl != NULL);

  sprintf(url, "%s?client=%s&ie=%s&oe=%s&dt=%s&sl=%s&tl=%s&q=", base,
          params.client, params.ie, params.oe, params.dt, params.sl, params.tl);

  int len = strlen(url);
  url_encode(text, url + len);
}

void parse_resp(char *parsed, const char *json_string) {

  json_t *root = json_loads(json_string, 0, NULL);
  json_t *array = json_array_get(root, 0);

  size_t offset = 0;

  for (size_t i = 0; i < json_array_size(array); i++) {

    json_t *dialogue = json_array_get(array, i);
    json_t *chunk = json_array_get(dialogue, 0);

    const char *paragaph = json_string_value(chunk);
    size_t para_size = json_string_length(chunk);
    memcpy(parsed + offset, paragaph, para_size);
    offset += para_size;
  }
  parsed[offset] = '\0';

  json_decref(root);
}

void genarate_tts_url(char *url, const TTSParams params, Text text) {
  const char base[] = "https://translate.googleapis.com/translate_tts";

  assert(base != NULL);
  assert(params.client != NULL && params.ie != NULL && params.tl != NULL);

  sprintf(url, "%s?client=%s&ie=%s&tl=%s&q=", base, params.client, params.ie,
          params.tl);

  int len = strlen(url);
  url_encode(text, url + len);
}

ssize_t media_read_cb(void *opaque, unsigned char *buf, size_t len) {
  MemAudioData *mVid = (MemAudioData *)opaque; // cast and give context

  size_t copyLen =
      (mVid->bytes - mVid->pos < len) ? mVid->bytes - mVid->pos : len;
  char *start = mVid->audio + mVid->pos;
  memcpy(buf, start, copyLen); // copy bytes requested to buffer.
  mVid->pos += copyLen;

  return copyLen;
}

int media_open_cb(void *opaque, void **datap, uint64_t *sizep) {
  // cast opaque to our audio state struct
  MemAudioData *mVid = (MemAudioData *)opaque;
  *sizep = mVid->bytes; // set stream length
  *datap = mVid;

  return 0;
}

int media_seek_cb(void *opaque, uint64_t offset) {
  MemAudioData *mVid = (MemAudioData *)opaque;
  mVid->pos = offset;
  return 0;
}

void play_audio(MemAudioData mem, float speed) {

  libvlc_instance_t *vlc;

  // add Verbose option to instance
  const char *options[] = {"--quiet"};

  vlc = libvlc_new(1, options);
  // vlc = libvlc_new(0, NULL);
  libvlc_media_t *media = libvlc_media_new_callbacks(
      vlc, media_open_cb, media_read_cb, media_seek_cb, NULL, (void *)&mem);

  // Create a media player playing environment
  libvlc_media_player_t *mediaPlayer =
      libvlc_media_player_new_from_media(media);

  // Set the playback rate to 2x
  libvlc_media_player_set_rate(mediaPlayer, speed);

  // play the media_player
  libvlc_media_player_play(mediaPlayer);

  sleep(1);
  // Main event loop
  while (libvlc_media_player_is_playing(mediaPlayer)) {
  }

  libvlc_media_player_stop(mediaPlayer);
  libvlc_media_player_release(mediaPlayer);
  // Free vlc
  libvlc_release(vlc);
}

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

bool is_end_sentence(const char *text) {
  if ((text[0] == '?' || text[0] == '.') && isspace(text[1])) {
    return true;
  }
  return false;
}

bool is_interrupt_sentence(const char *text) {
  if ((text[0] == ',' || text[0] == ';') && isspace(text[1])) {
    return true;
  }
  return false;
}

Text tok(char *text, int len, int limit) {

  int blank_pos = 0;
  int end_sentence_pos = 0;
  int interrupt_sentence_pos = 0;

  int count = 0;
  const int start = 0;
  int end = 0;
  int pos = 0;

  // printf("Origin:\n");
  // fwrite(text, 1, len, stdout);
  // // printf("\nlen: %d\nEnd\n", len);
  // printf("\n");

  if (len <= limit) {
    return (Text){.data = text, .size = len};
  }

  while (true) {

    if (isspace(text[pos])) {
      blank_pos = pos;
    }

    if (is_end_sentence(text + pos)) {
      end_sentence_pos = pos;
    }

    if (is_interrupt_sentence(text + pos)) {
      interrupt_sentence_pos = pos;
    }

    if (count == limit) {
      // end = fmax(interrupt_sentence_pos, end_sentence_pos);
      end =
          end_sentence_pos == 0
              ? interrupt_sentence_pos == 0 ? blank_pos : interrupt_sentence_pos
              : end_sentence_pos;
      // printf("End: %d and %d\n", interrupt_sentence_pos,
      // end_sentence_pos); end = interrupt_sentence_pos;
      assert(start < end);
      return (Text){.data = text, .size = end - start + 1};
    }

    if (pos == len - 1) {
      end = pos;
      return (Text){.data = text, .size = end - start + 1};
    }

    count++;
    pos++;
  }
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

  MemAudioData mem = {.audio = audio.data, .bytes = audio.size, .pos = 0};
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
