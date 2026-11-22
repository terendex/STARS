/* Kuma: reads the environment variable KUMA_EYE and compares it with a
   scrambled secret using strcmp. `ltrace ./kuma` shows getenv("KUMA_EYE")
   coming back empty (nil). Run again with the variable set to anything
   (KUMA_EYE=hello ltrace ./kuma) and ltrace shows the strcmp call with the real
   value in it. setup.sh passes in KEY, SECRET_BYTES and FLAG_BYTES. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const unsigned char secret_bytes[] = SECRET_BYTES;
static const unsigned char flag_bytes[] = FLAG_BYTES;

static void unscramble(const unsigned char *in, size_t len, char *out)
{
    for (size_t i = 0; i < len; i++)
        out[i] = (char)(in[i] ^ KEY);
    out[len] = '\0';
}

int main(void)
{
    char secret[64], flag[64];
    const char *eye = getenv("KUMA_EYE");

    puts("Kuma, in the dragon's head, only wakes for the right setting.");
    if (eye == NULL) {
        puts("Kuma's eye stays shut. It's waiting for a setting you haven't given it.");
        return 1;
    }

    unscramble(secret_bytes, sizeof secret_bytes, secret);
    if (strcmp(eye, secret) != 0) {
        puts("Kuma opens one eye, doesn't like what it sees, and goes back to sleep.");
        return 1;
    }

    unscramble(flag_bytes, sizeof flag_bytes, flag);
    printf("Kuma's eyes open wide. %s\n", flag);
    return 0;
}
