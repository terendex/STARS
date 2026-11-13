/* Eltanin: takes a password after its name (./eltanin hello) and checks it with
   strcmp. The password and the flag are stored XORed with KEY, so strings
   can't find them, but `ltrace ./eltanin hello` shows the strcmp call with the
   real password in it. The guess comes from the command line rather than a
   prompt, so ltrace's output isn't tangled up with a prompt waiting for input.
   setup.sh passes in KEY, PASSWORD_BYTES and FLAG_BYTES. */
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
        puts("Eltanin, the eye of the dragon, is watching you.");
        puts("Give it the password after its name, like this: ./eltanin hello");
        return 1;
    }

    unscramble(password_bytes, sizeof password_bytes, password);
    if (strcmp(argv[1], password) != 0) {
        puts("The dragon doesn't know you.");
        return 1;
    }

    unscramble(flag_bytes, sizeof flag_bytes, flag);
    printf("The dragon blinks. %s\n", flag);
    return 0;
}
