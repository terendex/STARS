/* Setting: reads the environment variable PANTRY_CODE and compares it with a
   scrambled secret using strcmp. `ltrace ./pantry` shows getenv("PANTRY_CODE")
   coming back empty (nil). Run again with the variable set to anything
   (PANTRY_CODE=hello ltrace ./pantry) and ltrace shows the strcmp call with the
   real value in it. setup.sh passes in KEY, SECRET_BYTES and FLAG_BYTES. */
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
    const char *code = getenv("PANTRY_CODE");

    puts("The pantry is locked with a code.");
    if (code == NULL) {
        puts("No code given. It's waiting for a setting you haven't given it.");
        return 1;
    }

    unscramble(secret_bytes, sizeof secret_bytes, secret);
    if (strcmp(code, secret) != 0) {
        puts("Wrong code. The pantry stays locked.");
        return 1;
    }

    unscramble(flag_bytes, sizeof flag_bytes, flag);
    printf("The pantry opens. %s\n", flag);
    return 0;
}
