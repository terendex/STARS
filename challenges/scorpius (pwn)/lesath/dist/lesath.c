#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct visitor {
    char name[16];
    int is_astronomer;
};

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
    struct visitor visitor = {0};
    setvbuf(stdout, NULL, _IONBF, 0);
    puts("=== Lesath Visitor Desk ===");
    printf("Please sign in. What's your name? ");

    /* Look closely: how much is this allowed to read, and how big is name? */
    fgets(visitor.name, sizeof(visitor), stdin);
    visitor.name[strcspn(visitor.name, "\n")] = '\0';

    printf("Welcome, %s!\n", visitor.name);
    if (visitor.is_astronomer != 0) {
        puts("Astronomer badge detected. Here's the archive key:");
        print_flag();
    } else {
        puts("You're signed in as a visitor. The archive is for astronomers only.");
    }
    return 0;
}
