#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct record {
    char name[32];
    unsigned int visits;
    unsigned int key;
    char notes[8];
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
    struct record record = {0};
    setvbuf(stdout, NULL, _IONBF, 0);
    puts("=== Dschubba Observatory Records ===");
    printf("Enter your name: ");

    fgets(record.name, sizeof(record), stdin);
    record.name[strcspn(record.name, "\n")] = '\0';

    printf("Key on file: 0x%08x\n", record.key);
    if (record.key == 0x41564f4e) {
        puts("Key accepted.");
        print_flag();
    } else {
        puts("Wrong key. Access denied.");
    }
    return 0;
}
