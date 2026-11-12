/* Eltanin: asks for a password and checks it with strcmp. The password and the
   flag are stored XORed with KEY, so strings can't find them, but
   `ltrace ./eltanin` shows the strcmp call with the real password in it.
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

int main(void)
{
    char password[64], guess[64], flag[64];

    unscramble(password_bytes, sizeof password_bytes, password);

    printf("Eltanin, the eye of the dragon, is watching you.\nPassword: ");
    fflush(stdout);
    if (!fgets(guess, sizeof guess, stdin))
        return 1;
    guess[strcspn(guess, "\n")] = '\0';

    if (strcmp(guess, password) != 0) {
        puts("The dragon doesn't know you.");
        return 1;
    }

    unscramble(flag_bytes, sizeof flag_bytes, flag);
    printf("The dragon blinks. %s\n", flag);
    return 0;
}
