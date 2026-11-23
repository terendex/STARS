/* Read the Assembly: asks for a code and compares it with a number written
   straight into the program's instructions. `disassemble check_code` in gdb
   (or objdump -d) shows it in a `cmp $0x...` line. strtol with base 0 accepts
   hex such as 0x1f as well as decimal, so players can type the number exactly
   as the assembly shows it. setup.sh passes in CODE, KEY and FLAG_BYTES. */
#include <stdio.h>
#include <stdlib.h>

static const unsigned char flag_bytes[] = FLAG_BYTES;

static int check_code(long code)
{
    return code == CODE;
}

static void reveal_flag(char *flag)
{
    for (size_t i = 0; i < sizeof flag_bytes; i++)
        flag[i] = (char)(flag_bytes[i] ^ KEY);
    flag[sizeof flag_bytes] = '\0';
}

int main(void)
{
    char line[64], flag[64];

    puts("Piggy bank vault. Enter the code to open it.");
    printf("Code: ");
    fflush(stdout);
    if (fgets(line, sizeof line, stdin) == NULL)
        return 1;

    if (!check_code(strtol(line, NULL, 0))) {
        puts("Wrong code. The vault stays shut.");
        return 1;
    }

    reveal_flag(flag);
    printf("The vault opens. %s\n", flag);
    return 0;
}
