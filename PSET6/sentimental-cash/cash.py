from cs50 import get_float

while True:
    n = get_float("Change owed: ")
    if n > 0:
        break
    else:
        continue

n = round(n * 100)

coins = 0

while n > 0:
    if n >= 25:
        n -= 25
    elif n >= 10:
        n -= 10
    elif n >= 5:
        n -= 5
    else:
        n -= 1
    coins += 1

print(coins)
