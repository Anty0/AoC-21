#!/usr/bin/env python3

import sys

x = 0
y = 0
a = 0

for line in sys.stdin:
    # line = line[:-1]
    command, n = line.split(" ")
    n = int(n)
    # print(command, n)
    if command == "forward":
        x += n
        y += a * n
    elif command == "down":
        a += n
    elif command == "up":
        a -= n

print("x:", x, " y:", y, " a:", a)
print(x * y)
