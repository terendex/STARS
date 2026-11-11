#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    char name[64];
    char command[160];
    setvbuf(stdout, NULL, _IONBF, 0);

    puts("=== Larawag Star Greeter ===");
    printf("Which star should we greet? ");
    if (fgets(name, sizeof(name), stdin) == NULL) {
        return 0;
    }
    name[strcspn(name, "\r\n")] = '\0';

    /* Put the name into a terminal command, then run it. */
    snprintf(command, sizeof(command), "echo Hello, %s", name);
    system(command);
    puts("Clear skies from Larawag.");
    return 0;
}
