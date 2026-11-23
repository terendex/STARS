/* Thuban: the flag sits in the program as plain text, and nothing prints it.
   `strings thuban` finds it. setup.sh passes the flag in as FLAG. */
#include <stdio.h>

/* "used" keeps the flag in the program even though no code reads it. */
__attribute__((used)) static const char flag[] = FLAG;

int main(void)
{
    puts("Thuban guided the builders of the pyramids, long before Polaris took over.");
    puts("It wrote its secret down somewhere in this program, then forgot to say it out loud.");
    return 0;
}
