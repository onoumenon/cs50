// Implement a program that encrypts messages using Caesar’s cipher, per https://docs.cs50.net/2018/x/psets/2/caesar/caesar.html

#include <cs50.h>
#include <stdio.h>

#include <stdlib.h>
#include <string.h>
#include <ctype.h>


int main(int argc, string argv[])
{
    // get input for cypher number
    if (argc != 2)
    {
        printf("Usage:./caesar number'\n");
        return (1);
    }


int cypher = atoi(argv[1]);



    if (argc == 2 && cypher > 0)
    {
        printf("Your cypher is %i.\n", cypher);
    }
    else
    {
        printf("Cypher number has to be positive integer.\n");
        return (1);
    }



    // get plaintext to encrypt
    string plaintext;
    do
    {
        plaintext = get_string("Enter text to be encrypted: ");
    } while (plaintext == NULL);

    // return encrypted text
    int i = 0;
    printf("Your encrypted text: ");
    for (i = 0; i < strlen(plaintext); i++)
    {
        if (isupper (plaintext[i]))
        printf("%c", 65 + (plaintext[i] - 65 + cypher) % 26);

        else if islower(plaintext[i])
        printf("%c", (((plaintext[i] + cypher - 97) % 26) + 97));

        //if neither then print char as is
        else
        printf("%c", plaintext[i]);
    }
    printf("\n");
    return 0;
}

