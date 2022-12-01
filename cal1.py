#!/usr/bin/env python3

import sys

n = 0
p = 0
bufLen = 3
first = True
buffer = [0 for i in range(bufLen)]
for line in sys.stdin:
    num = int(line)
    if not first and buffer[p] < buffer[(p + 1) % bufLen] + num:
        n += 1
    buffer[p] = 0
    p = (p + 1) % bufLen
    first = first and p != 0
    buffer = [buffer[i] + num for i in range(bufLen)]


print(n)
