
#include <cs50.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
int X = atoi(&fraction[0]);
int Y = atoi(&fraction[2]);
int dur = (8/Y)*X;
return dur;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
char letter = note[0];
int octave = atoi(&note[strlen(note)-1]);

int A4hz = 440;
int octaveShift = (octave - 4);
int hz = round(A4hz * pow(2, octaveShift));
float n;
int freq;
float A=0., B=2., C=-9., D=-7., E=-5., F=-4., G=-2.;

switch (letter)
    {
        case 'A':
        n = A;
        break;

        case 'B':
        n = B;
        break;

        case 'C':
        n = C;
        break;

        case 'D':
        n = D;
        break;

        case 'E':
        n = E;
        break;

        case 'F':
        n = F;
        break;

        case 'G':
        n = G;
        break;

        default:
        return 1;
    }

int finalhz = round(hz * pow(2, n/12));
float accidhz = (hz * pow(2, n/12));

    if (note[1] == '#')
    {
    freq = round(accidhz * pow(2., 1./12.));
    return (freq);
    }
    else if (note[1] == 'b')
    {
    freq = round(accidhz/ pow(2., 1./12.));
    return (freq);
    }
return (finalhz);
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    if (s[0] == '\0')
    {
        return true;
    }
    else
    {
        return false;
    }
}
