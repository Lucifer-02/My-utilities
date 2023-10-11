#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void url_encode(const char *input, int len, char *output) {

  int pos = 0;

  for (int i = 0; i < len; i++) {
    unsigned char ch = input[i];

    // printf("char: %02x\n", ch);

    if (('A' <= ch && ch <= 'Z') || ('a' <= ch && ch <= 'z') ||
        ('0' <= ch && ch <= '9')) {
      output[pos++] = ch;
    } else if (ch == ' ') {
      output[pos++] = '+';
    } else if (ch == '-' || ch == '_' || ch == '.' || ch == '!' || ch == '~' ||
               ch == '*' || ch == '\'' || ch == '(' || ch == ')') {
      output[pos++] = ch;
    }

    else {
      sprintf(output + pos, "%%%02X", ch);
      pos += 3;
    }
  }

  output[pos++] = '\0'; // Null-terminate the encoded string
}

int main() {
  const char *input = "xin chào";
  char encoded[256];
  url_encode(input, strlen(input), encoded);
  printf("Encoded: %s\n", encoded);
  return 0;
}
