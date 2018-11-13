// Not yet styled

#define _XOPEN_SOURCE
#include <cs50.h>
#include <unistd.h>
#include <crypt.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{

        if (argc !=  2 || strlen(argv[1]) != 13)
        {
        printf("Please enter a 13-char hashed password to crack in the command line.");
        return 1;
        }
        else {


        // get salty
        char salt[3];
        salt[0] = argv[1][0] ;
        salt[1] = argv[1][1];

        //make alphabets array
        int i = 0;
        char alphabets[52];
        for (i = 0; i < 26; i++){
        alphabets[i] = 65 + i;
        alphabets[26+i] = 97 + i;

        }


        int iterations = strlen(alphabets);
        char password1 [2];
        password1[1] = '\0';
        int index1 = 0;
        for (index1 = 0; index1 < iterations; index1++){
        password1[0] = alphabets[index1];

        int match = strcmp(crypt(password1,salt), argv[1]);
           if (match == 0){
               printf("Password is %s.\n", password1);
           }
        }



        char password2 [3];
        password2[2] = '\0';
        index1 = 0;
        int index2 = 0;
        for (index1 = 0; index1 < iterations; index1++){
        password2[0] = alphabets[index1];
        for (index2 = 0; index2 < iterations; index2++){
            password2[1] = alphabets[index2];

        int match = strcmp(crypt(password2,salt), argv[1]);
           if (match == 0){
               printf("Password is %s.\n", password2);
                 }
            }
        }

        char password3 [4];
        index1 = 0;
        index2 = 0;
        int index3 = 0;
        password3[3] = '\0';
        for (index1 = 0; index1 < iterations; index1++){
        password3[0] = alphabets[index1];
        for (index2 = 0; index2 < iterations; index2++){
            password3[1] = alphabets[index2];
        for (index3 = 0; index3 < iterations; index3++){
        password3[2] = alphabets[index3];
        int match = strcmp(crypt(password3,salt), argv[1]);
           if (match == 0){
               printf("Password is %s.\n", password3);
           }
        }
        }

        }

    }
}
