/* Level Up: the game only gives the flag to players at level 9000 or more, and
   everyone starts at level 1. In gdb: `break check_level`, `run`,
   `set var level = 9000`, `continue`. Built with debug info (-g) so gdb knows
   the variable's name. setup.sh passes in KEY and FLAG_BYTES. */
#include <stdio.h>

static const unsigned char flag_bytes[] = FLAG_BYTES;

static void check_level(int level)
{
    char flag[64];

    printf("Your level is %d.\n", level);
    if (level < 9000) {
        puts("The secret ending is only for level 9000 or more. Keep grinding!");
        return;
    }

    for (size_t i = 0; i < sizeof flag_bytes; i++)
        flag[i] = (char)(flag_bytes[i] ^ KEY);
    flag[sizeof flag_bytes] = '\0';
    printf("It's over 9000! Secret ending unlocked: %s\n", flag);
}

int main(void)
{
    int level = 1;

    puts("Welcome back to the game.");
    check_level(level);
    return 0;
}
