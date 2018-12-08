import cs50 as cs
import sys



def main():
    try:
        cypher = int(sys.argv[1])
    except IndexError:
        print("Usage: program number, or input number now: ")
        cypher = cs.get_int()



    if cypher > 0:
        print("Your cypher is {}" .format(cypher))
    else:
        print("Usage: program number. Cypher number has to be positive integer.")
        return 1

    while True:
        plaintext = cs.get_string("Enter text to be encrypted: ")
        if plaintext:
            break

    print("Your encrypted text: ", end="")
    for i in range(len(plaintext)):
        if plaintext[i].isupper() == True:
            character = 65 + (ord(plaintext[i]) - 65 + cypher) % 26
            print(chr(character), end="")
        elif plaintext[i].islower() == True:
            character = (((ord(plaintext[i]) + cypher - 97) % 26) + 97)
            print(chr(character), end="")
        else:
            print("{}".format(plaintext[i]), end="")

    print("")
    return 0







if __name__== "__main__":
  main()
