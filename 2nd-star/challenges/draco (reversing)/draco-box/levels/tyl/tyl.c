/* Tyl: only gives the flag to observers of level 9000 or more, and everyone
   starts at level 1. In gdb: `break check_level`, `run`, `set var level = 9000`,
   `continue`. Built with debug info (-g) so gdb knows the variable's name.
   setup.sh passes in KEY and FLAG_BYTES. */
#include <stdio.h>

static const unsigned char flag_bytes[] = FLAG_BYTES;

static void check_level(int level)
{
    char flag[64];

    printf("Your observer level is %d.\n", level);
    if (level < 9000) {
        puts("Tyl only talks to observers of level 9000 or more. Come back when you've levelled up.");
        return;
    }

    for (size_t i = 0; i < sizeof flag_bytes; i++)
        flag[i] = (char)(flag_bytes[i] ^ KEY);
    flag[sizeof flag_bytes] = '\0';
    printf("Tyl salutes you, master observer. %s\n", flag);
}

int main(void)
{
    int level = 1;

    puts("Tyl keeps watch over the dragon's coils.");
    check_level(level);
    return 0;
}
