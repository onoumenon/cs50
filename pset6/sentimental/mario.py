import cs50 as cs

while True:
    n = cs.get_int()
    if n > 0 and n < 23:
        break

for i in range(n):
    print(" "* (n-i-1), end="")
    print("#"* (i+2), end="")
    print("")
