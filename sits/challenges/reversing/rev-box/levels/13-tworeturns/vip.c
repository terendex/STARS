/* Two Returns: the club has a thousand-year queue, then the bouncer asks
   vip_tier() for your tier, and only tier 3 gets in. Your tier is 0 unless
   you're root. In gdb, players `return` out of queue_up() to skip the wait,
   which shows them tier 3 is needed, then `return 3` out of vip_tier(). Built
   with -g so `return 3` works without casts. setup.sh passes in KEY and
   FLAG_BYTES. */
#include <stdio.h>
#include <unistd.h>

static const unsigned char flag_bytes[] = FLAG_BYTES;

/* The queue outside the club. It's a long one. */
static void queue_up(void)
{
    for (long seconds = 1000L * 365 * 24 * 60 * 60; seconds > 0; seconds--)
        sleep(1);
}

/* Only the owner (root) is a tier 3 VIP. */
static int vip_tier(void)
{
    return getuid() == 0 ? 3 : 0;
}

int main(void)
{
    char flag[64];
    int tier;

    puts("You're in the queue for the club. Estimated wait: 1000 years.");
    fflush(stdout);
    queue_up();

    tier = vip_tier();
    if (tier != 3) {
        printf("Bouncer: you're a tier %d guest. Only tier 3 VIPs get in tonight.\n", tier);
        return 1;
    }

    for (size_t i = 0; i < sizeof flag_bytes; i++)
        flag[i] = (char)(flag_bytes[i] ^ KEY);
    flag[sizeof flag_bytes] = '\0';
    printf("Bouncer: welcome in. %s\n", flag);
    return 0;
}
