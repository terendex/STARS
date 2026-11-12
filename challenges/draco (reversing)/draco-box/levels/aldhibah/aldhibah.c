/* Aldhibah: prints the flag only after sleeping for a thousand years, and only
   for root. In gdb, players `return` out of wait_for_dragon() to skip the
   sleep, and `return 1` out of is_rider() to pass the check. Built with -g so
   `return 1` works without casts. setup.sh passes in KEY and FLAG_BYTES. */
#include <stdio.h>
#include <unistd.h>

static const unsigned char flag_bytes[] = FLAG_BYTES;

/* The dragon sleeps for a thousand years before it will speak. */
static void wait_for_dragon(void)
{
    for (long seconds = 1000L * 365 * 24 * 60 * 60; seconds > 0; seconds--)
        sleep(1);
}

/* Only the dragon's rider may hear the flag, and the rider is root. */
static int is_rider(void)
{
    return getuid() == 0;
}

static void reveal_flag(char *flag)
{
    for (size_t i = 0; i < sizeof flag_bytes; i++)
        flag[i] = (char)(flag_bytes[i] ^ KEY);
    flag[sizeof flag_bytes] = '\0';
}

int main(void)
{
    char flag[64];

    puts("Aldhibah, the dragon, is asleep. It will wake in a thousand years.");
    fflush(stdout);
    wait_for_dragon();

    if (!is_rider()) {
        puts("The dragon wakes, sees you aren't its rider, and goes back to sleep.");
        return 1;
    }

    reveal_flag(flag);
    printf("The dragon speaks: %s\n", flag);
    return 0;
}
