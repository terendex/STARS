/* Fafnir: only answers to its true name. It compares the name it was started
   under (argv[0], without the folder) with its true name using strcmp. The
   true name is stored as plain text, so `strings fafnir` lists it and
   `ltrace ./fafnir` shows the comparison. The flag is XORed with the true name,
   so skipping the check in gdb only prints garbage: players have to start the
   program under that name, with a link (ln -s) or bash's exec -a.
   setup.sh passes in TRUE_NAME and FLAG_BYTES. */
#include <stdio.h>
#include <string.h>

static const char true_name[] = TRUE_NAME;
static const unsigned char flag_bytes[] = FLAG_BYTES;

int main(int argc, char *argv[])
{
    char flag[128];
    const char *called;
    size_t length;

    if (argc < 1)
        return 1;
    called = strrchr(argv[0], '/');
    called = called ? called + 1 : argv[0];

    if (strcmp(called, true_name) != 0) {
        printf("You called me \"%s\". That is only the name on my door.\n", called);
        puts("Fafnir answers to his true name, and to nothing else.");
        return 1;
    }

    length = strlen(called);
    for (size_t i = 0; i < sizeof flag_bytes; i++)
        flag[i] = (char)(flag_bytes[i] ^ (unsigned char)called[i % length]);
    flag[sizeof flag_bytes] = '\0';
    printf("You know my true name. %s\n", flag);
    return 0;
}
