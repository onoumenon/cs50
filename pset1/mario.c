#include <cs50.h>
#include <stdio.h>

// print out a half pyramid of # with the number of levels = user input
// conditions: levels 1 to 22

int main (void)
{
    int n;
    do
    {
        printf("Input levels for half pyramid (number 1 to 22): ");
        n = get_int();
    }
    while (n < 0 || n > 23);



    for (int i = 0; i < n; i++)
    {
       for (int spaces = n - i; spaces > 1; spaces--)
        {
                printf(" ");
        }
        for (int hashes = 0; hashes < i + 2; hashes++)
        {
                printf("#");
        }
            printf("\n");
    }
}
