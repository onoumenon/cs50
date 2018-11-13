import cs50 as cs

while True:
    print("How much change do I owe you in dollars?")
    cash = cs.get_float()
    if cash > 0:
        break

cash = round(cash,2)
coins = round(cash * 100)

while coins > 0:
    while coins > 49:
        fifties = (coins - coins%50) / 50
        coins = coins%50 #remainder
        print("{} half-dollars".format(fifties))
    while coins > 24:
        quarters = (coins - coins%25) / 25
        coins = coins%25 #remainder
        print("{} quarters".format(quarters))
    while coins > 9:
        dimes = (coins - coins%10) / 10
        coins = coins%10 #remainder
        print("{} dimes".format(dimes))
    while coins > 0:
        pennies = coins
        print("{} pennies".format(pennies))
        coins = 0
    break


