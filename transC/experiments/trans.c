#include <assert.h>
#include <ctype.h>
#include <curl/curl.h>
#include <jansson.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER_SIZE 8194 

// Struct to hold translated data and its size
typedef struct {
  char *data;
  size_t size;
} Text;

typedef struct {
  char *client;
  char *ie;
  char *oe;
  char *dt;
  char *sl;
  char *tl;
} TransParams;

// Warning: May can't handle all cases. See https://www.url-encode-decode.com/
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
// Callback function to handle received data
size_t write_data(void *ptr, size_t size, size_t nmemb, Text *resp) {
  assert(resp->data != NULL);
  assert(size < BUFFER_SIZE);

  size_t new_size = resp->size + size * nmemb;
  memcpy(resp->data + resp->size, ptr, size * nmemb);
  resp->size = new_size;
  resp->data[resp->size] = '\0';
  return size * nmemb;
}

// Function to perform translation request using Google Translate API
void request_trans(Text *resp, const char *url) {
  CURL *curl = curl_easy_init();
  if (curl) {
    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, resp);
    CURLcode res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
      fprintf(stderr, "curl_easy_perform() failed: %s\n",
              curl_easy_strerror(res));
    }
    curl_easy_cleanup(curl);
  }
  assert(resp->data != NULL);
  assert(resp->size != 0);
}

void parse_resp(Text json_string, Text *output) {
  json_t *root = json_loads(json_string.data, 0, NULL);
  json_t *array = json_array_get(root, 0);

  size_t offset = 0;

  for (size_t i = 0; i < json_array_size(array); i++) {

    json_t *dialogue = json_array_get(array, i);
    json_t *chunk = json_array_get(dialogue, 0);

    const char *paragaph = json_string_value(chunk);
    size_t para_size = json_string_length(chunk);
    memcpy(output->data + offset, paragaph, para_size);
    offset += para_size;
  }

  output->data[offset] = '\0';
  output->size = offset;

  json_decref(root);
}

void get_trans(Text *trans, Text resp) {

  assert(trans != NULL);
  assert(resp.size != 0);

  parse_resp(resp, trans);

  assert(trans->size != 0);
}

void genarate_url(char *url, const TransParams params, Text text) {
  // char url[] =
  //     "https://translate.googleapis.com/translate_a/"
  //     "single?client=gtx&ie=UTF-8&oe=UTF-8&dt=t&sl=auto&tl=vi&q=game+show";
  //
  const char base[] = "https://translate.googleapis.com/translate_a/single";
  assert(base != NULL);
  assert(params.client != NULL && params.ie != NULL && params.oe != NULL &&
         params.dt != NULL && params.sl != NULL && params.tl != NULL);

  sprintf(url, "%s?client=%s&ie=%s&oe=%s&dt=%s&sl=%s&tl=%s&q=", base,
          params.client, params.ie, params.oe, params.dt, params.sl, params.tl);

  size_t len = strlen(url);
  url_encode(text, url + len);
}

int main() {
  char text[] =
      // "ai? tôi là ai?";

      "In this paper, we introduce TimeGPT, the first foundation model for "
      "time series, capable of generating accurate predictions for diverse "
      "datasets not seen during training. We evaluate our pre-trained model "
      "against established statistical, machine learning, and deep learning "
      "methods, demonstrating that TimeGPT zero-shot inference excels in "
      "performance, efficiency, and simplicity. Our study provides compelling "
      "evidence that insights from other domains of artificial intelligence "
      "can be effectively applied to time series analysis. We conclude that "
      "large-scale time series models offer an exciting opportunity to "
      "democratize access to precise predictions and reduce uncertainty by "
      "leveraging the capabilities of contemporary advancements in deep "
      "learning.";
      // "xin chào, tên tôi là Hoàng.. Bạn có khỏe không? Chiều nay ta "
      // "có hẹn tại ";
      // "This line is a giveaway: you have named your script json. but "
      // "you are trying to import the builtin module called json, "
      // "?since your script is in the current directory, it comes first "
      // "in sys.path, and so that's the module that gets imported.";
      // "how are your?. What's your name?. Do you love me?. Let's go.";
      size_t source_len = strlen(text);
  Text source = {.data = text, .size = source_len};

  assert(source_len < BUFFER_SIZE);
  assert(source_len != 0);

  char url[BUFFER_SIZE];
  TransParams params = {.client = "gtx",
                        .ie = "UTF-8",
                        .oe = "UTF-8",
                        .dt = "t",
                        .sl = "auto",
                        .tl = "vi"};

  genarate_url(url, params, source);
  // printf("url: %s\n", url);

  char data[BUFFER_SIZE];
  Text resp = {.data = data, .size = 0};

  request_trans(&resp, url);
  // printf("Output: %s, size: %ld\n", resp.data, resp.size);

  char translation[BUFFER_SIZE];
  Text trans = {.data = translation, .size = 0};

  get_trans(&trans, resp);
  printf("Translation: %s\n", trans.data);
}
