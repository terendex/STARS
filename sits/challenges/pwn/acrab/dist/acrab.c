#include <stdio.h>
#include <stdlib.h>

int main(void) {
    char flag[64] = {0};
    char *flag_location = flag;
    char callsign[128];
    (void)flag_location;

    FILE *file = fopen("/flag.txt", "r");
    if (file == NULL) {
        puts("flag.txt is missing. Tell an organizer.");
        return 1;
    }
    fgets(flag, sizeof(flag), file);
    fclose(file);

    setvbuf(stdout, NULL, _IONBF, 0);
    puts("=== Acrab Radio Relay ===");
    puts("The flag is in memory, but this program never prints it.");

    for (;;) {
        printf("\nCallsign: ");
        if (fgets(callsign, sizeof(callsign), stdin) == NULL) {
            return 0;
        }
        printf("Transmitting: ");
        /* The bug: printf treats whatever the user typed as its format string. */
        printf(callsign);
    }
}
