// Copies a BMP file

#include <stdio.h> //standard input output lib
#include <stdint.h> //define int lib
typedef uint8_t  BYTE;  // define our BYTE type


int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover filename\n");
        return 1;
    }

    // variable declarations
    char *memCard = argv[1]; //name of memory card
    FILE *memCardPtr;        // pointer to memory card

    FILE *newImg = NULL;   // file pointer to a new image
    BYTE buffer[512];         // array per buffer
    int imgNo = 0;      // keep track of Jpeg count
    char filename[8];       // array for filename (000.jpg\n)

    // open input file
    memCardPtr = fopen(memCard, "r");
    if (memCardPtr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", memCard);
        return 2;
    }


    // read memCard till jpeg header
   while (fread(buffer,512, 1, memCardPtr) > 0) //fread gives no of blocks
   {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0) //if start of jpeg is found
    {

             if (newImg != NULL) //closes previous image file if any
             {
             fclose(newImg);
             }

             sprintf(filename, "%03i.jpg", imgNo);      //3 digits, padded 0s (d refers to  signed decimal integer, i to integer)
             newImg = fopen(filename, "w");                // w: open for writing only
             imgNo++;

    }

        if (newImg != NULL)                              //writes onto created image & continues till new jpeg is found
        {
            fwrite(buffer, 512, 1, newImg);
        }

   }

     // closes files after all of memCard is scanned
    if (newImg != NULL)
    {
        fclose(newImg);
    }


    fclose(memCardPtr);


    // success
    return 0;
}
