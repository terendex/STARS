/* Freeze Frame: writes a secret note in memory, then burns it without printing
   it. In gdb: `break burn_note`, `run`, `info args` shows the note. Built with
   debug info (-g) so gdb can show the argument by name. setup.sh passes in KEY
   and FLAG_BYTES. */
#include <stdio.h>
#include <string.h>

static const unsigned char flag_bytes[] = FLAG_BYTES;

/* Prints the welcome. */
static void say_hello(void)
{
    puts("Passing a secret note in class...");
}

/* Writes the note into `note`. */
static void write_note(char *note)
{
    for (size_t i = 0; i < sizeof flag_bytes; i++)
        note[i] = (char)(flag_bytes[i] ^ KEY);
    note[sizeof flag_bytes] = '\0';
}

/* Wipes the note from memory before the teacher sees it. */
static void burn_note(char *note)
{
    memset(note, 0, 64);
}

int main(void)
{
    char note[64];

    say_hello();
    write_note(note);
    puts("The note was read... and then burned. Nobody saw what it said.");
    burn_note(note);
    return 0;
}
