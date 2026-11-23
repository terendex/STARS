/* Altais: decodes a message holding the flag, then scrubs it without printing
   it. In gdb: `break scrub_message`, `run`, `info args` shows the flag. It's
   built with debug info (-g) so gdb can show the argument by name. setup.sh
   passes in KEY and FLAG_BYTES. */
#include <stdio.h>
#include <string.h>

static const unsigned char flag_bytes[] = FLAG_BYTES;

/* Prints the welcome. */
static void show_banner(void)
{
    puts("Altais is receiving a message from deep space...");
}

/* Decodes the message into `message`. */
static void decode_message(char *message)
{
    for (size_t i = 0; i < sizeof flag_bytes; i++)
        message[i] = (char)(flag_bytes[i] ^ KEY);
    message[sizeof flag_bytes] = '\0';
}

/* Wipes the message from memory. */
static void scrub_message(char *message)
{
    memset(message, 0, 64);
}

int main(void)
{
    char message[64];

    show_banner();
    decode_message(message);
    puts("Message decoded. Classified, so it won't be shown.");
    scrub_message(message);
    puts("Message scrubbed. Nothing to see here.");
    return 0;
}
