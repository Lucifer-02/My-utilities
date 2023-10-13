#include <assert.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <curl/curl.h>
#include <vlc/libvlc.h>
#include <vlc/vlc.h>

#define BUFFER_SIZE 1048576 // 1Mb

// Struct to hold translated data and its size
typedef struct {
  char *data;
  int size;
} Text;

typedef struct {
  char *client;
  char *ie;
  char *tl;
} TTSParams;

typedef struct {
  char *audio; // pointer to audio in memory
  size_t bytes;
  size_t pos;
} MemAudioData;

// Callback function to handle received data
size_t write_data(void *buffer, size_t size, size_t nmemb, Text *tts) {
  size_t written = size * nmemb;
  memcpy(tts->data + tts->size, buffer, written);
  tts->size += written;
  return written;
}

// Function to perform translation request using Google Translate API
void request_tts(Text *tts, const char *url) {
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
}

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

void genarate_url(char *url, const TTSParams params, Text text) {
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

void play_audio(MemAudioData mem) {

  // add Verbose option to instance
  const char *options[] = {"--quiet"};

  // libvlc_instance_t *vlc = libvlc_new(1, options);
  libvlc_instance_t *vlc = libvlc_new(0, NULL);

  libvlc_media_t *media = libvlc_media_new_callbacks(
      vlc, media_open_cb, media_read_cb, media_seek_cb, NULL, (void *)&mem);

  // Create a media player playing environment
  libvlc_media_player_t *mediaPlayer =
      libvlc_media_player_new_from_media(media);

  // Set the playback rate to 2x
  libvlc_media_player_set_rate(mediaPlayer, 2.0);

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
      end = end_sentence_pos == 0 ? interrupt_sentence_pos : end_sentence_pos;
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

int main() {
  char text[] =
      "Có rất nhiều khoảng cách xung quanh đường 45 độ trong scatter diagram "
      "thực tế so với trong Hình 3. Sự chênh lệch này cho thấy điểm yếu của "
      "mối quan hệ giữa chiều cao của cha và chiều cao của con trai. Ví dụ, "
      "giả sử bạn phải đoán chiều cao của một đứa con trai. Chiều cao của bố "
      "giúp ích cho bạn bao nhiêu? Trong Hình 1, các chấm trong ống khói đại "
      "diện cho tất cả các cặp cha-con trong đó người cha cao từ 72 inch đến "
      "inch gần nhất (chiều cao của người cha từ 71,5 inch đến 72,5 inch, "
      "trong đó các đường thẳng đứng nét đứt cắt ngang trục x). Vẫn có rất "
      "nhiều sự thay đổi về chiều cao của các con trai, được biểu thị bằng sự "
      "phân tán theo chiều dọc trong ống khói. Ngay cả khi bạn biết chiều cao "
      "của người cha, vẫn có rất nhiều sai sót khi cố gắng đoán chiều cao của "
      "con trai mình.";

  // "Bạn có khỏe không? Tên bạn là gì?";
  // "ASCII là viết tắt của Mã tiêu chuẩn Mỹ để trao đổi thông tin. Máy tính "
  // "chỉ có thể hiểu được các con số, vì vậy mã ASCII là sự biểu diễn bằng "
  // "số của một ký tự như 'a' hoặc '@' hoặc một hành động nào đó. ASCII đã "
  // "được phát triển từ lâu và hiện nay các ký tự không in được hiếm khi "
  // "được sử dụng cho mục đích ban đầu của chúng. Dưới đây là bảng ký tự "
  // "ASCII và bảng này bao gồm các mô tả về 32 ký tự không in được đầu tiên. "
  // "ASCII thực sự được thiết kế để sử dụng với teletypes và do đó các mô tả "
  // "có phần mơ hồ. Tuy nhiên, nếu ai đó nói rằng họ muốn CV của bạn ở định "
  // "dạng ASCII, tất cả điều này có nghĩa là họ muốn văn bản 'thuần túy' "
  // "không có định dạng như tab, in đậm hoặc gạch dưới - định dạng thô mà "
  // "bất kỳ máy tính nào cũng có thể hiểu được. Điều này thường là để họ có "
  // "thể dễ dàng nhập tệp vào ứng dụng của riêng mình mà không gặp vấn đề "
  // "gì. Notepad.exe tạo văn bản ASCII hoặc trong MS Word bạn có thể lưu tệp "
  // "dưới dạng 'chỉ văn bản'";

  // "how old are you?. What's your name?. Do you love me?. Let's go.";
  // "This line is a giveaway: you have named your script json. but "
  // "you are trying to import the builtin module called json, "
  // "?since your script is in the current directory, it comes first "
  // "in sys.path, and so that's the module that gets imported.";

  int trans_len = strlen(text);
  assert(trans_len < BUFFER_SIZE);
  assert(trans_len != 0);

  char url[BUFFER_SIZE];
  Text trans = {.data = text, .size = trans_len};
  TTSParams params = {.client = "gtx", .ie = "UTF-8", .tl = "vi"};

  const int limit = 250;
  char *pointer = trans.data + 0;
  int size = trans.size - 0;
  char data[BUFFER_SIZE];
  Text audio = {.data = data, .size = 0};

  while (size > 0) {

    Text slice = tok(pointer, size, limit);
    // fwrite(slice.data, 1, slice.size, stdout);
    // printf("\n");
    // printf("\nlen: %d\n", slice.size);
    genarate_url(url, params, slice);
    // printf("url: %s\n", url);
    pointer = slice.data + slice.size + 1;
    size -= slice.size + 1;
    // printf("Remain: %d\n", size);

    // put all audio chunk together
    Text resp = {.data = data + audio.size,
                 .size = 0}; // resp also a slice to audio
    request_tts(&resp, url);
    audio.size += resp.size;
    // printf("TTS: %s, size: %d\n", all.data, all.size);

    // ---------------------------------------
    // MemAudioData mem = {.audio = resp.data, .bytes = resp.size, .pos = 0};

    // play_audio(mem);
  }

  MemAudioData mem = {.audio = audio.data, .bytes = audio.size, .pos = 0};
  play_audio(mem);

  return 0;
}
