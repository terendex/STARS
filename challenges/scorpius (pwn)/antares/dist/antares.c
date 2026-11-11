#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/* Realigns the stack on entry so a plain return-to-function works. */
__attribute__((force_align_arg_pointer))
void supernova(void) {
    char flag[128] = {0};
    FILE *file = fopen("/flag.txt", "r");
    if (file == NULL) {
        puts("The core is unstable, but flag.txt is missing. Tell an organizer.");
        exit(1);
    }
    fgets(flag, sizeof(flag), file);
    puts("*** CORE COLLAPSE ***");
    puts(flag);
    exit(0);
}

static void take_reading(void) {
    char reading[64];
    puts("Antares core monitor online.");
    printf("Diagnostics: supernova() is at %p\n", (void *)supernova);
    puts("Enter fusion reading:");
    /* Reads up to 256 bytes into a 64-byte buffer. */
    read(STDIN_FILENO, reading, 256);
    puts("Reading logged.");
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    take_reading();
    puts("Core stable. Nothing to report.");
    return 0;
}
