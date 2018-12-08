In Pset2,

caesar.c iterates a caesar cypher over user-input text based on user-given number, accounting for lower and upper cases.
Basically, if the cypher is '2', a is shifted two positions to c, and z cycles back to b.
It is done by cycling through ascii values with modulus (with conversions between char/number).

crack.c cracks a short password that has been hashed with C’s DES-based crypt function, via brute force.
