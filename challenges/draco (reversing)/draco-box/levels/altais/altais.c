/* Altais: rebuilds the flag in memory, then wipes it without printing it.
   In gdb: `break forget_flag`, `run`, `info args` shows the flag. It's built
   with debug info (-g) so gdb can show the argument by name. setup.sh passes
   in KEY and FLAG_BYTES. */
#include <stdio.h>
#include <string.h>

static const unsigned char flag_bytes[] = FLAG_BYTES;

/* Rebuilds the flag into `flag`. */
static void remember_flag(char *flag)
{
    for (size_t i = 0; i < sizeof flag_bytes; i++)
        flag[i] = (char)(flag_bytes[i] ^ KEY);
    flag[sizeof flag_bytes] = '\0';
}

/* Wipes the flag from memory. */
static void forget_flag(char *flag)
{
    memset(flag, 0, 64);
}

int main(void)
{
    char flag[64];

    remember_flag(flag);
    puts("Altais remembered the flag for a moment...");
    forget_flag(flag);
    puts("...and now it's forgotten. If only you'd been watching.");
    return 0;
}
