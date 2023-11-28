import string
from cs50 import get_string

text = get_string("Text: ")

l = 0
for i in text:
    if i.isalpha():
        l += 1

w = len(text.split())

s = 0
for m in text:
    if m == "." or m == "?" or m == "!":
        s += 1

words = w / 100
L = l / words
S = s / words

index = round(0.0588 * L - 0.296 * S - 15.8)

if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
