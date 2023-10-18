#ifndef COMMON_H
#define COMMON_H

#include <stdbool.h>

// Struct to hold translated data and its size
typedef struct {
  char *data;
  int size;
} Text;

// Warning: May can't handle all cases. See https://www.url-encode-decode.com/
void url_encode(const Text text, char *output);
bool is_end_sentence(const char *text);
bool is_interrupt_sentence(const char *text);
Text tok(char *text, int len, int limit);

#endif
