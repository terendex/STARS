/* Compare Notes: takes a password after its name (./checker hello) and checks
   it with strcmp. The password and the flag are stored XORed with KEY, so
   strings can't find them, but `ltrace ./checker hello` shows the strcmp call
   with the real password in it. setup.sh passes in KEY, PASSWORD_BYTES and
   FLAG_BYTES. */
#include <stdio.h>
#include <string.h>

static const unsigned char password_bytes[] = PASSWORD_BYTES;
static const unsigned char flag_bytes[] = FLAG_BYTES;

static void unscramble(const unsigned char *in, size_t len, char *out)
{
    for (size_t i = 0; i < len; i++)
        out[i] = (char)(in[i] ^ KEY);
    out[len] = '\0';
}

int main(int argc, char *argv[])
{
    char password[64], flag[64];

    if (argc != 2) {
        puts("Give the password after the program's name, like this: ./checker hello");
        return 1;
    }

    unscramble(password_bytes, sizeof password_bytes, password);
    if (strcmp(argv[1], password) != 0) {
        puts("Wrong password.");
        return 1;
    }

    unscramble(flag_bytes, sizeof flag_bytes, flag);
    printf("Correct! %s\n", flag);
    return 0;
}
