/* Skip the Wait: puts you in a queue that takes a thousand years, then prints
   the flag. In gdb: `break wait_in_line`, `run`, `return` (answer y),
   `continue`. setup.sh passes in KEY and FLAG_BYTES. */
#include <stdio.h>
#include <unistd.h>

static const unsigned char flag_bytes[] = FLAG_BYTES;

/* The queue for the new phone. It's a long one. */
static void wait_in_line(void)
{
    for (long seconds = 1000L * 365 * 24 * 60 * 60; seconds > 0; seconds--)
        sleep(1);
}

int main(void)
{
    char flag[64];

    puts("You joined the queue for the new phone. Estimated wait: 1000 years.");
    fflush(stdout);
    wait_in_line();

    for (size_t i = 0; i < sizeof flag_bytes; i++)
        flag[i] = (char)(flag_bytes[i] ^ KEY);
    flag[sizeof flag_bytes] = '\0';
    printf("Your turn! Here's your receipt: %s\n", flag);
    return 0;
}
