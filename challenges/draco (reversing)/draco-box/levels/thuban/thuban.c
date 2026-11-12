/* Thuban: the flag sits in the program as plain text, and nothing prints it.
   `strings thuban` finds it. setup.sh passes the flag in as FLAG. */
#include <stdio.h>

/* "used" keeps the flag in the program even though no code reads it. */
__attribute__((used)) static const char flag[] = FLAG;

int main(void)
{
    puts("Thuban was the pole star when the pyramids were built.");
    puts("It has kept one secret ever since, and it isn't telling you.");
    return 0;
}
