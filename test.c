#include <curl/curl.h>
#include <jansson.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
  CURL *curl;
  CURLcode res;

  curl_global_init(CURL_GLOBAL_DEFAULT);

  curl = curl_easy_init();

  if (curl) {
    char url[1024];
    char *client = "gtx";
    char *ie = "UTF-8";
    char *oe = "UTF-8";
    char *dt = "t";
    char *sl = "en";
    char *tl = "vi";
    char *q = "hello";
    sprintf(url,
            "https://translate.googleapis.com/translate_a/"
            "single?client=%s&ie=%s&oe=%s&dt=%s&sl=%s&tl=%s&q=%s",
            client, ie, oe, dt, sl, tl, q);

    // struct curl_slist *headers = NULL;
    //
    // headers = curl_slist_append(headers, "Content-Type: application/json");
    //
    // curl_easy_setopt(curl, CURLOPT_URL,
    //                  "https://translate.googleapis.com/translate_a/single?");
    // curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    // curl_easy_setopt(curl, CURLOPT_POSTFIELDS,
    //                  "{ 'client': 'gtx', 'ie': 'UTF-8', "
    //                  "'oe': 'UTF-8', 'dt': 't', 'sl' : 'en', 'tl': 'vi' ,
    //                  'q': "
    //                  "'Hello, world!'}");
    curl_easy_setopt(curl, CURLOPT_URL, url);

    FILE *fp;
    char out[1024];
    fp = fopen("out.txt", "wb");
    curl_easy_setopt(curl, CURLOPT_READFUNCTION, NULL);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, out);
    // curl_easy_setopt(curl, CURLOPT_HTTPHEADER, out);

    int a;
    // curl_easy_getinfo(curl, CURLINFO_HEADER_SIZE, a);
    printf("Output: %s\n", out);
    // printf("Output: %d\n", a);

    /* Perform the request, res will get the return code */
    res = curl_easy_perform(curl);

    /* Check for errors */
    // if (res != CURLE_OK)
    //   fprintf(stderr, "curl_easy_perform() failed: %s\n",
    //           curl_easy_strerror(res));

    /* always cleanup */
    curl_easy_cleanup(curl);
    fclose(fp);
  }

  curl_global_cleanup();

  return 0;
}
