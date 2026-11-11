#include <stdio.h>
#include <stdlib.h>

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
    int credits = 100;
    char line[32];
    setvbuf(stdout, NULL, _IONBF, 0);
    puts("=== Sargas Star Shop ===");

    for (;;) {
        printf("\nYou have %d credits.\n", credits);
        puts("1) Buy star maps (10 credits each)");
        puts("2) Buy the flag (1000 credits)");
        puts("3) Leave");
        printf("> ");
        if (fgets(line, sizeof(line), stdin) == NULL) {
            return 0;
        }

        int choice = atoi(line);
        if (choice == 1) {
            printf("How many maps? ");
            if (fgets(line, sizeof(line), stdin) == NULL) {
                return 0;
            }
            int cost = atoi(line) * 10;
            if (cost > credits) {
                puts("You can't afford that.");
            } else {
                credits -= cost;
                puts("Thanks for your purchase!");
            }
        } else if (choice == 2) {
            if (credits >= 1000) {
                print_flag();
                return 0;
            }
            puts("You can't afford the flag.");
        } else if (choice == 3) {
            puts("Clear skies!");
            return 0;
        } else {
            puts("That's not an option.");
        }
    }
}
