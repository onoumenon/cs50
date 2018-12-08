import cs50 as cs
import crypt
import sys



def main ():
    try:
        if (len(sys.argv) == 3 and len(sys.argv[2]) == 13):
            hashedpw = sys.argv[2]
        else:
            hashedpw = input('Enter 13-char hashed password to crack:')
    except IndexError:
        hashedpw = input('Enter 13-char hashed password to crack:')

    salt = [None] * 2
    salt[0] = hashedpw[0]
    salt[1] = hashedpw[1]

    alphabets = [None] * 56
    for i in range(26):
        alphabets[i] = chr(65 + i)
        alphabets[26+i] = chr(97 + i)

    iterations = len(alphabets)
    password = [None] * 4


    def iterate( ):
        while True:
            counter = 0
            for i in range(iterations):
                password[counter] = alphabets[i]
                counter += 1
            if (crypt.crypt(password, salt) == hashedpw):
                print("Password is {}".format(password))
                break

if __name__== "__main__":
  main()
