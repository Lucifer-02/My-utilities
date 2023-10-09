#include <assert.h>
#include <ctype.h>
#include <curl/curl.h>
#include <jansson.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER_SIZE 1024

// Struct to hold translated data and its size
typedef struct {
  char *data;
  size_t size;
} Translate;

typedef struct {
  char *client;
  char *ie;
  char *oe;
  char *dt;
  char *sl;
  char *tl;
  char *q;
} TransParams;

// Callback function to handle received data
size_t write_data(void *ptr, size_t size, size_t nmemb, Translate *trans) {
  assert(trans->data != NULL);
  assert(size < BUFFER_SIZE);

  size_t new_size = trans->size + size * nmemb;
  // trans->data = realloc(trans->data, new_size + 1);
  // if (trans->data == NULL) {
  //   fprintf(stderr, "Failed to allocate memory\n");
  //   return 0;
  // }
  memcpy(trans->data + trans->size, ptr, size * nmemb);
  trans->size = new_size;
  trans->data[trans->size] = '\0';
  return size * nmemb;
}

// Function to perform translation request using Google Translate API
void request_trans(Translate *trans, const char *url) {
  CURL *curl = curl_easy_init();
  if (curl) {
    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, trans);
    CURLcode res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
      fprintf(stderr, "curl_easy_perform() failed: %s\n",
              curl_easy_strerror(res));
    }
    curl_easy_cleanup(curl);
  }
  assert(trans->data != NULL);
  assert(trans->size != 0);
}

void genarate_url(char *url, const char *base, const TransParams params) {
  assert(base != NULL);
  assert(params.client != NULL && params.ie != NULL && params.oe != NULL &&
         params.dt != NULL && params.sl != NULL && params.tl != NULL &&
         params.q != NULL);

  sprintf(url, "%s?client=%s&ie=%s&oe=%s&dt=%s&sl=%s&tl=%s&q=%s", base,
          params.client, params.ie, params.oe, params.dt, params.sl, params.tl,
          params.q);
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

void get_trans(char *translation, const char *json_string) {

  // abc
  json_t *root = json_loads(json_string, 0, NULL);
  json_t *array = json_array_get(root, 0);

  size_t offset = 0;

  for (size_t i = 0; i < json_array_size(array); i++) {

    json_t *dialogue = json_array_get(array, i);
    json_t *chunk = json_array_get(dialogue, 0);

    const char *paragaph = json_string_value(chunk);
    size_t para_size = json_string_length(chunk);
    memcpy(translation + offset, paragaph, para_size);
    offset += para_size;
  }

  json_decref(root);
}

int main() {
  // char url[] =
  //     "https://translate.googleapis.com/translate_a/"
  //     "single?client=gtx&ie=UTF-8&oe=UTF-8&dt=t&sl=auto&tl=vi&q=game+show";
  char base[] = "https://translate.googleapis.com/translate_a/single";
  char text[] = "Tôi buồn ngủ quá";
  // "This line is a giveaway: you have named your script json. but "
  // "you are trying to import the builtin module called json, "
  // "?since your script is in the current directory, it comes first "
  // "in sys.path, and so that's the module that gets imported.";
  // "how are your?. What's your name?. Do you love me?. Let's go.";

  assert(strlen(base) < BUFFER_SIZE);
  assert(strlen(text) < BUFFER_SIZE);

  char url[BUFFER_SIZE];
  normalize_text(text);
  TransParams params = {.client = "gtx",
                        .ie = "UTF-8",
                        .oe = "UTF-8",
                        .dt = "t",
                        .sl = "auto",
                        .tl = "en",
                        .q = normalize_text(text)};
  genarate_url(url, base, params);
  printf("url: %s\n", url);

  char data[BUFFER_SIZE];
  Translate trans = {.data = data, .size = 0};
  request_trans(&trans, url);
  printf("Output: %s, size: %ld\n", trans.data, trans.size);
  char translation[BUFFER_SIZE];
  get_trans(translation, trans.data);
  printf("Translation: %s\n", translation);

  return 0;
}
