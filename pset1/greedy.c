#include <cs50.h>
#include <stdio.h>
#include <math.h>


int main(void)
{

//variable declarations
int fifties;
int quarters;
int dimes;
int pennies;

float change;

   do
   {
   printf("How much do I owe you in dollars?\n");
   change = get_float();
   }
   while (change <= 0);

change = roundf(change * 100) / 100; //converts to 2 decimals
int coins = change * 100; //converts into cents
printf("I owe you %i cents\n", coins);

//Returns the least amount of coins given, if you only have 50 cents, 25 cents, 10 cents and 1 cent coins
   while (coins > 0)
   {
      if (coins >49)
      {
      fifties = (coins-coins%50)/50; // half dollars
      coins = coins%50;
      printf("%i half dollars given, ", fifties);
             while (coins < 1)
            {
               printf("and that's it.\n");
               break;
            }
      }

      else if (coins >24)
      {
      quarters = (coins-coins%25)/25; // quarters
      coins = coins%25;
      printf("%i quarters given, ", quarters);
             while (coins < 1)
            {
               printf("and that's it.\n");
               break;
            }
      }

      else if (coins >9)
      {
      dimes = (coins-coins%10)/10; // dimes
      coins = coins%10;
      printf("%i dimes given, ", dimes);
            while (coins < 1)
            {
               printf("and that's it.\n");
               break;
            }
      }

      else  {
             pennies = coins; // pennies
             coins = 0;
         printf("and %i pennies given.\n", pennies);
     }

   }
}
