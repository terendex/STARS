/* Aldhibah: hibernates for a thousand years, then asks rider_rank() for your
   rank, and only rank 7 hears the flag. Your rank is 0 unless you're root. In
   gdb, players `return` out of hibernate() to skip the sleep, which shows them
   that rank 7 is needed, then `return 7` out of rider_rank(). Built with -g so
   `return 7` works without casts. setup.sh passes in KEY and FLAG_BYTES. */
#include <stdio.h>
#include <unistd.h>

static const unsigned char flag_bytes[] = FLAG_BYTES;

/* The dragon sleeps for a thousand years before it will speak. */
static void hibernate(void)
{
    for (long seconds = 1000L * 365 * 24 * 60 * 60; seconds > 0; seconds--)
        sleep(1);
}

/* The dragon's riders have ranks, and only root holds the top one. */
static int rider_rank(void)
{
    return getuid() == 0 ? 7 : 0;
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
    int rank;

    puts("Aldhibah, the dragon, is hibernating. It will wake in a thousand years.");
    fflush(stdout);
    hibernate();

    rank = rider_rank();
    if (rank != 7) {
        printf("The dragon wakes and sees a rider of rank %d. It only speaks to riders of rank 7, so it goes back to sleep.\n", rank);
        return 1;
    }

    reveal_flag(flag);
    printf("The dragon speaks: %s\n", flag);
    return 0;
}
