#ifndef TRANS_H
#define TRANS_H

#include <stddef.h>

#include "common.h"

#define TRANS_BUFFER_SIZE 8192

// https://stackoverflow.com/questions/26714426/what-is-the-meaning-of-google-translate-query-params
typedef struct {
  char *client;
  char *ie; // input encode
  char *oe; // output encode
  char *dt; // translate mode
  char *sl; // source language
  char *tl; // target language
} TransParams;

// Function to perform translation request using Google Translate API
void request_api(Text *output, const char *url);
void genarate_trans_url(char *url, const TransParams params, Text text);
void parse_resp(char *parsed, const char *json_string);

#endif
