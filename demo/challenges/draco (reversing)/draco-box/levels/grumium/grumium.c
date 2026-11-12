/* Grumium (demo): the flag sits in the program as plain text, and nothing
   prints it. `strings grumium` finds it. setup.sh passes the flag in as FLAG. */
#include <stdio.h>

/* "used" keeps the flag in the program even though no code reads it. */
__attribute__((used)) static const char flag[] = FLAG;

int main(void)
{
    puts("Grumium, in the dragon's jaw, has three things to say:");
    puts("  1. Dragons guard treasure.");
    puts("  2. This dragon guards a flag.");
    puts("  3. It's not going to say it out loud.");
    return 0;
}
