// Resizes a BMP file into a new file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize infile outfile resize-factor\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[1];
    char *outfile = argv[2];
    int factor = atoi(argv[3]);

    // check if factor is valid
    if (factor < 1 || factor > 99)
    {
        fprintf(stderr, "Please input factor number between 1 and 99.\n");
        return 1;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }



    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    BITMAPFILEHEADER bfnew;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    bfnew = bf;

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    BITMAPINFOHEADER binew;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    binew = bi;

    // declare new height and width

    binew.biWidth = bi.biWidth * factor;
    binew.biHeight = bi.biHeight * factor;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // set new padding
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int newpadding = (4 - (binew.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // new file size (54 for header)
    bfnew.bfSize = 54 + (binew.biWidth * sizeof(RGBTRIPLE) + newpadding) * abs(binew.biHeight);
    binew.biSizeImage = bfnew.bfSize - 54;



    // write outfile's BITMAPFILEHEADER
    fwrite(&bfnew, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&binew, sizeof(BITMAPINFOHEADER), 1, outptr);



    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // vertical resizing
        int rowresize = 0;
        while  (rowresize < factor)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // write RGB triple to outfile                // horizontal resizing
                int columnresize = 0;
                while (columnresize < factor)
                {
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                columnresize++;
                }
            }


            // add new padding
            for (int k = 0; k < newpadding; k++)
                fputc(0x00, outptr);

            // seek back to the beginning of row in input file
            if (rowresize < (factor -1))
            fseek(inptr, -(bi.biWidth * sizeof(RGBTRIPLE)), SEEK_CUR);
            rowresize++;

        }

        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);


    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
