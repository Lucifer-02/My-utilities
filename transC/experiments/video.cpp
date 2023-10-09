#include <cstring>
#include <fstream>
#include <iostream>
#include <memory>
#include <unistd.h>
#include <vector>
#include <vlc/vlc.h>

using namespace std;

class MemVideoData {
public:
  MemVideoData(char *data, int data_bytes)
      : video(data), bytes(data_bytes) {} // init

  ~MemVideoData() {}

  char *video; //  pointer to video in memory
  size_t bytes;
  size_t pos = 0;
};

ssize_t media_read_cb(void *opaque, unsigned char *buf, size_t len) {
  MemVideoData *mVid = (MemVideoData *)opaque; // cast and give context

  size_t copyLen = std::min(mVid->bytes - mVid->pos, len);
  char *start = mVid->video + mVid->pos;
  memcpy(buf, start, copyLen); // copy bytes requested to buffer.
  mVid->pos += copyLen;

  return copyLen;
}

int media_open_cb(void *opaque, void **datap, uint64_t *sizep) {
  // cast opaque to our video state struct
  MemVideoData *mVid = static_cast<MemVideoData *>(opaque);
  *sizep = mVid->bytes; // set stream length
  *datap = mVid;

  return 0;
}

int media_seek_cb(void *opaque, uint64_t offset) {
  MemVideoData *mVid = static_cast<MemVideoData *>(opaque);
  mVid->pos = offset;
  return 0;
}

void media_close_cb(void *opaque) {}

// load a file to memory, write address into "fileInRam"
int loadFileToMem(const char *filePath, char **fileInRam) {
  int bytes = 0;

  FILE *file = fopen(filePath, "r");

  if (NULL == file) {
    return -1;
  }

  fseek(file, 0L, SEEK_END); // seek to end
  bytes = ftell(file);       // record size in bytes

  *fileInRam = new char[bytes]; // allocate ram

  if (NULL == *fileInRam) {
    return -2;
  }

  fseek(file, 0L, SEEK_SET);
  char *ptr = *fileInRam;
  int remaining = bytes;
  while (remaining > 0) {
    ssize_t len = fread(ptr, 1, remaining, file);
    ptr += len;
    remaining -= len;
  }
  fclose(file); // close file

  return bytes;
}

int main(int argc, const char **argv) {
  const char *filePath = "media/audio.mp3";
  char *ramBuff;

  int bytes =
      loadFileToMem(filePath, &ramBuff); // load file into byte (char) vector

  if (-1 == bytes) {
    cout << "Could not open file !" << endl;
    return -1;
  } else if (-2 == bytes) {
    cout << "Could not allocate memory! " << endl;
    return -1;
  } else if (0 == bytes) {
    cout << "File length 0 bytes! " << endl;
    return -1;
  }

  cout << "Loaded file to memory address: " << std::hex
       << static_cast<void *>(ramBuff) << endl;
  cout << "Bytes: " << std::dec << bytes << endl;

  MemVideoData mem(ramBuff, bytes);

  libvlc_instance_t *vlc;

  // add Verbose option to instance
  std::vector<const char *> options;
  options.push_back("--verbose=4");

  vlc = libvlc_new(int(options.size()), options.data());
  libvlc_media_t *media =
      libvlc_media_new_callbacks(vlc, media_open_cb, media_read_cb,
                                 media_seek_cb, media_close_cb, (void *)&mem);

  // Create a media player playing environment
  libvlc_media_player_t *mediaPlayer =
      libvlc_media_player_new_from_media(media);

  // play the media_player
  libvlc_media_player_play(mediaPlayer);
  sleep(15);

  // Stop playing
  libvlc_media_player_stop(mediaPlayer);

  // Free the media_player
  libvlc_media_player_release(mediaPlayer);

  // Free vlc
  libvlc_release(vlc);

  delete[] ramBuff;
}
