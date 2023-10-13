#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <vlc/vlc.h>

typedef struct {
  char *video; // pointer to video in memory
  size_t bytes;
  size_t pos;
} MemVideoData;

ssize_t media_read_cb(void *opaque, unsigned char *buf, size_t len) {
  MemVideoData *mVid = (MemVideoData *)opaque; // cast and give context

  size_t copyLen =
      (mVid->bytes - mVid->pos < len) ? mVid->bytes - mVid->pos : len;
  char *start = mVid->video + mVid->pos;
  memcpy(buf, start, copyLen); // copy bytes requested to buffer.
  mVid->pos += copyLen;

  return copyLen;
}

int media_open_cb(void *opaque, void **datap, uint64_t *sizep) {
  // cast opaque to our video state struct
  MemVideoData *mVid = (MemVideoData *)opaque;
  *sizep = mVid->bytes; // set stream length
  *datap = mVid;

  return 0;
}

int media_seek_cb(void *opaque, uint64_t offset) {
  MemVideoData *mVid = (MemVideoData *)opaque;
  mVid->pos = offset;
  return 0;
}

void media_close_cb(void *opaque) {}

// load a file to memory, write address into "fileInRam"
int loadFileToMem(const char *filePath, char **fileInRam) {
  int bytes = 0;

  FILE *file = fopen("../media/audio.mp3", "r");

  if (NULL == file) {
    return -1;
  }

  fseek(file, 0L, SEEK_END); // seek to end
  bytes = ftell(file);       // record size in bytes

  *fileInRam = (char *)malloc(bytes * sizeof(char)); // allocate ram

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

// Event handler function
static void handleEvents(const libvlc_event_t *pEvent, void *pUserData) {
  libvlc_media_player_t *mp = pUserData;
  switch (pEvent->type) {
  case libvlc_MediaPlayerEndReached:
    printf("Player End Reached\n");
    libvlc_media_player_stop(mp);
    libvlc_media_player_release(mp);
    break;
  default:
    break;
  }
}

void play_audio(MemVideoData mem) {

  libvlc_instance_t *vlc;

  // add Verbose option to instance
  const char *options[] = {"--quiet"};

  vlc = libvlc_new(1, options);

  for (int i = 0; i < 2; i++) {

    mem.pos = 0;

    libvlc_media_t *media =
        libvlc_media_new_callbacks(vlc, media_open_cb, media_read_cb,
                                   media_seek_cb, media_close_cb, (void *)&mem);

    // Create a media player playing environment
    libvlc_media_player_t *mediaPlayer =
        libvlc_media_player_new_from_media(media);

    // Set the playback rate to 2x
    libvlc_media_player_set_rate(mediaPlayer, 2.0);

    // // Register event manager
    // libvlc_event_manager_t *eventManager =
    //     libvlc_media_player_event_manager(mediaPlayer);
    // libvlc_event_attach(eventManager, libvlc_MediaPlayerEndReached,
    //                     handleEvents, mediaPlayer);

    // play the media_player
    libvlc_media_player_play(mediaPlayer);

    sleep(1);
    // Main event loop
    while (libvlc_media_player_is_playing(mediaPlayer)) {
    }

    // Stop playing
    libvlc_media_player_stop(mediaPlayer);

    // Free the media_player
    libvlc_media_player_release(mediaPlayer);
  }
  // Free vlc
  libvlc_release(vlc);
}

int main(int argc, const char **argv) {
  const char *filePath = "media/audio.mp3";
  char *ramBuff;

  long bytes =
      loadFileToMem(filePath, &ramBuff); // load file into byte (char) vector

  if (-1 == bytes) {
    printf("Could not open file !\n");
    return -1;
  } else if (-2 == bytes) {
    printf("Could not allocate memory! \n");
    return -1;
  } else if (0 == bytes) {
    printf("File length 0 bytes! \n");
    return -1;
  }

  printf("Loaded file to memory address: %p\n", ramBuff);
  printf("Bytes: %ld\n", bytes);

  MemVideoData mem = {ramBuff, bytes, 0};

  play_audio(mem);

  free(ramBuff);
}
