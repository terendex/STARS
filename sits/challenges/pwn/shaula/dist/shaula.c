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
    char line[32];
    setvbuf(stdout, NULL, _IONBF, 0);
    puts("=== Shaula Night Tour ===");

    for (;;) {
        puts("\n1) Look at Shaula, the scorpion's sting");
        puts("2) Look at Lesath, its twin");
        puts("3) Leave the tour");
        printf("> ");
        if (fgets(line, sizeof(line), stdin) == NULL) {
            return 0;
        }

        switch (atoi(line)) {
        case 1:
            puts("Shaula is the second-brightest star in Scorpius.");
            break;
        case 2:
            puts("Lesath sits right next to Shaula. Together they're called the Cat's Eyes.");
            break;
        case 3:
            puts("Clear skies!");
            return 0;
        case 314:
            /* Guides only. Not on the printed menu. */
            puts("Welcome, guide. Here's tonight's code:");
            print_flag();
            return 0;
        default:
            puts("That's not on the menu.");
        }
    }
}
