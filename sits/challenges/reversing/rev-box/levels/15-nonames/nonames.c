/* No Names: decodes the flag into memory, then wipes it with memset, and the
   program is stripped, so gdb has none of its function names. But memset is a
   library function, so `break memset` still works: when it pauses, memset's
   first argument (the address of the flag) is in the register rdi, and
   `x/s $rdi` prints it. setup.sh passes in KEY and FLAG_BYTES. */
#include <stdio.h>
#include <string.h>

static const unsigned char flag_bytes[] = FLAG_BYTES;

static void decode(char *out)
{
    for (size_t i = 0; i < sizeof flag_bytes; i++)
        out[i] = (char)(flag_bytes[i] ^ KEY);
    out[sizeof flag_bytes] = '\0';
}

static void wipe(char *buffer)
{
    memset(buffer, 0, 64);
}

int main(void)
{
    char buffer[64];

    puts("This program's names have all been scrubbed off.");
    decode(buffer);
    puts("It knew the flag for a moment...");
    wipe(buffer);
    puts("...and now it's wiped.");
    return 0;
}
