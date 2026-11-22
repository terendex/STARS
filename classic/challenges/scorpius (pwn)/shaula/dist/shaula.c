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
    puts("=== Shaula Sky Tour ===");

    for (;;) {
        puts("\n1) Look at Shaula");
        puts("2) Look at Scorpius");
        puts("3) Leave the tour");
        printf("> ");
        if (fgets(line, sizeof(line), stdin) == NULL) {
            return 0;
        }

        switch (atoi(line)) {
        case 1:
            puts("Shaula sits at the tip of the scorpion's tail.");
            break;
        case 2:
            puts("Scorpius curls across the southern sky.");
            break;
        case 3:
            puts("Clear skies!");
            return 0;
        case 42:
            /* Staff only. The tour guide never mentions this one. */
            print_flag();
            return 0;
        default:
            puts("That's not on the menu.");
        }
    }
}
