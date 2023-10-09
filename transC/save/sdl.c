#include <SDL2/SDL.h>
#include <SDL2/SDL_audio.h>
#include <stdlib.h>

typedef struct {
  uint8_t *data;
  size_t size;
  size_t index;
} UserData;

// Audio callback function
void audioCallback(void *userdata, Uint8 *stream, int len) {

  UserData *data = ((UserData *)userdata);
  // Copy audio data from the buffer to the stream
  size_t bytesToCopy = len;
  if (data->index + bytesToCopy > data->size) {
    bytesToCopy = data->size - data->index;
  }
  memcpy(stream, data->data + data->index, bytesToCopy);
  data->index += bytesToCopy;

  // If the buffer is fully consumed, stop playback
  if (data->index >= data->size) {
    SDL_PauseAudio(1);
  }
}

int main() {
  uint8_t *audioBuffer;
  size_t bufferSize;
  size_t bufferIndex = 0;

  // Open file and read into buffer
  FILE *file = fopen("sound/abc", "rb");
  fseek(file, 0, SEEK_END);
  bufferSize = ftell(file);
  fseek(file, 0, SEEK_SET);

  audioBuffer = malloc(bufferSize);
  fread(audioBuffer, 1, bufferSize, file);

  UserData user_data = {.data = audioBuffer, .size = bufferSize, .index = 0};

  // Initialize SDL2
  if (SDL_Init(SDL_INIT_AUDIO) < 0) {
    printf("SDL initialization failed: %s\n", SDL_GetError());
    return 1;
  }

  // Set up audio specifications
  SDL_AudioSpec desiredSpec, obtainedSpec;
  desiredSpec.freq = 24000;
  desiredSpec.format = AUDIO_S16SYS;
  desiredSpec.channels = 2;
  desiredSpec.samples = 4096;
  desiredSpec.callback = audioCallback;
  desiredSpec.userdata = &user_data;
  desiredSpec.size = user_data.size;

  // Open the audio device
  if (SDL_OpenAudio(&desiredSpec, NULL) < 0) {
    printf("Failed to open audio device: %s\n", SDL_GetError());
    return 1;
  }

  // Start audio playback
  SDL_PauseAudio(0);

  // Wait for audio to finish playing
  while (bufferIndex < bufferSize) {
    SDL_Delay(100);
  }

  // Clean up
  SDL_CloseAudio();
  SDL_Quit();
  free(audioBuffer);

  return 0;
}
