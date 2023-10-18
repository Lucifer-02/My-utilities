#include <assert.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include <curl/curl.h>
#include <jansson.h>
#include <vlc/vlc.h>

#include "trans.h"

// Callback function to handle received data
static size_t write_data(const void *ptr, size_t size, size_t nmemb,
                         Text *resp) {
  assert(resp->data != NULL);

  size_t new_size = resp->size + size * nmemb;
  memcpy(resp->data + resp->size, ptr, size * nmemb);
  resp->size = new_size;
  resp->data[resp->size] = '\0';
  return size * nmemb;
}

// Function to perform translation request using Google Translate API
void request_api(Text *output, const char *url) {
  assert(url != NULL);
  assert(output->data != NULL);

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

void genarate_trans_url(char *url, const TransParams params, Text text) {
  assert(params.client != NULL && params.ie != NULL && params.oe != NULL &&
         params.dt != NULL && params.sl != NULL && params.tl != NULL);

  const char base[] = "https://translate.googleapis.com/translate_a/single";

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
