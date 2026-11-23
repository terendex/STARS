/* Strings Attached: the flag sits in the program as plain text, and nothing
   prints it. `strings secret | grep FLAG` finds it. setup.sh passes the flag in
   as FLAG. */
#include <stdio.h>

/* "used" keeps the flag in the program even though no code reads it. */
__attribute__((used)) static const char flag[] = FLAG;

int main(void)
{
    puts("Nothing to see here. Really.");
    puts("Well, nothing that this program will ever print.");
    return 0;
}
