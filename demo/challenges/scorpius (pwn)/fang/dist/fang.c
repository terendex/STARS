#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

static void print_flag(void) {
    char flag[128] = {0};
    FILE *file = fopen("/flag.txt", "r");
    if (file == NULL) {
        puts("flag.txt is missing. Tell an organizer.");
        exit(1);
    }
    fgets(flag, sizeof(flag), file);
    puts(flag);
}

int main(void) {
    char passcode[17];
    char guess[64];
    setvbuf(stdout, NULL, _IONBF, 0);

    /* A new random passcode for every visitor, so guessing is pointless. */
    srand(time(NULL) ^ getpid());
    for (int i = 0; i < 16; i++) {
        passcode[i] = 'a' + rand() % 26;
    }
    passcode[16] = '\0';

    puts("=== Fang Vault ===");
    puts("The vault opens for anyone who knows today's 16-letter passcode.");
    printf("Passcode: ");
    if (fgets(guess, sizeof(guess), stdin) == NULL) {
        return 0;
    }
    guess[strcspn(guess, "\r\n")] = '\0';

    /* Check what was typed against the passcode. */
    if (strncmp(guess, passcode, strlen(guess)) == 0) {
        puts("Access granted.");
        print_flag();
    } else {
        puts("Access denied. The passcode has already changed.");
    }
    return 0;
}
