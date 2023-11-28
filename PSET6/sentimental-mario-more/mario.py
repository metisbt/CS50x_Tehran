from cs50 import get_int

while True:
    height = get_int("Height: ")

    if height >= 1 and height <= 8:
        break
    else:
        continue
for item in range(height):
    print(" " * (height - (item + 1)) + "#" * (item + 1) + "  " + "#" * (item + 1))
