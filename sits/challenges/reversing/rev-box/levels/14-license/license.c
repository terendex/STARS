/* License Key: asks for a license key. check_key() wants exactly 8 digits that
   add up to TOTAL. The messages say which rule a key broke, but not the total.
   `disassemble check_key` in gdb shows the rules as cmp lines: $0x8 (the
   length), $0x2f and $0x39 (just below '0', and '9'), and the total. Any key
   that follows the rules works, so players make their own: a "keygen".
   setup.sh passes in TOTAL, KEY and FLAG_BYTES. */
#include <stdio.h>
#include <string.h>

static const unsigned char flag_bytes[] = FLAG_BYTES;

/* 0 if the key is valid, otherwise which rule it broke. */
static int check_key(const char *key)
{
    size_t length = strlen(key);
    int total = 0;

    if (length != 8)
        return 1;
    for (size_t i = 0; i < length; i++) {
        if (key[i] <= '/' || key[i] > '9')
            return 2;
        total += key[i] - '0';
    }
    if (total != TOTAL)
        return 3;
    return 0;
}

int main(void)
{
    char line[64], flag[64];

    puts("PhotoFix Pro: trial expired. Enter your license key to keep editing.");
    printf("License key: ");
    fflush(stdout);
    if (fgets(line, sizeof line, stdin) == NULL)
        return 1;
    line[strcspn(line, "\r\n")] = '\0';

    switch (check_key(line)) {
    case 1:
        puts("Invalid key: a license key is 8 characters long.");
        return 1;
    case 2:
        puts("Invalid key: a license key is only digits.");
        return 1;
    case 3:
        puts("Invalid key: those digits don't add up to the right total.");
        return 1;
    }

    for (size_t i = 0; i < sizeof flag_bytes; i++)
        flag[i] = (char)(flag_bytes[i] ^ KEY);
    flag[sizeof flag_bytes] = '\0';
    printf("License accepted. Thank you! %s\n", flag);
    return 0;
}
