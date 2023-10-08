#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <vlc/vlc.h>

ssize_t read_callback(void *opaque, unsigned char *buf, size_t len) {

  printf("This\n");

  // This function should read 'len' bytes from the buffer and store them in
  // 'buf'. The 'opaque' parameter is a pointer to the data that you want to
  // pass to the callback. In this example, we'll assume that 'opaque' is a
  // pointer to an array of bytes.
  unsigned char *data = (unsigned char *)opaque;
  size_t data_len = sizeof(data);
  size_t bytes_to_copy = len < data_len ? len : data_len;
  memcpy(buf, data, bytes_to_copy);
  return bytes_to_copy;
}

int main(int argc, char **argv) {
  // Open file and read into buffer
  FILE *file = fopen("audio.mp3", "rb");
  fseek(file, 0, SEEK_END);
  long size = ftell(file);
  fseek(file, 0, SEEK_SET);

  unsigned char *buffer = malloc(size);
  fread(buffer, 1, size, file);

  libvlc_instance_t *inst;
  libvlc_media_t *m;
  libvlc_media_player_t *mp;
  unsigned char audio_data[] = {/* Your MP3 data here */};

  // Initialize libVLC
  inst = libvlc_new(0, NULL);

  // Create a new media item with a custom bitstream input
  m = libvlc_media_new_callbacks(inst, NULL, read_callback, NULL, NULL,
                                 buffer + 44);

  // m = libvlc_media_new_path(inst, "audio.mp3");

  // -------------- not modify ------------------
  // Create a media player for the media item
  mp = libvlc_media_player_new_from_media(m);

  // Set the playback rate to 2x
  libvlc_media_player_set_rate(mp, 2.0);

  // Play the media
  libvlc_media_player_play(mp);

  sleep(2);

  // Stop playing
  libvlc_media_player_stop(mp);

  // Release the media player
  libvlc_media_player_release(mp);

  // Release the media item
  libvlc_media_release(m);

  // Release libVLC
  libvlc_release(inst);
  fclose(file);

  return 0;
}
