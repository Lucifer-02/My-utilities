#include <assert.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>

#include "common.h"

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

  output[pos++] = '\0';
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
