#!/usr/bin/env python3

import sys
import json

occupied = {}

for line in sys.stdin:
    if line[-1] == "\n":
        line = line[:-1]
    start, end = line.split(" -> ")
    sx, sy = tuple(int(s) for s in start.split(","))
    ex, ey = tuple(int(s) for s in end.split(","))

    # if sx != ex and sy != ey:
    #     continue

    while sx != ex or sy != ey:
        pid = "%i:%i" % (sx, sy)
        n = occupied.get(pid)
        if n is None:
            n = 0
        occupied[pid] = n + 1

        sx = sx + (0 if sx == ex else (1 if sx < ex else -1))
        sy = sy + (0 if sy == ey else (1 if sy < ey else -1))

    pid = "%i:%i" % (sx, sy)
    n = occupied.get(pid)
    if n is None:
        n = 0
    occupied[pid] = n + 1

print(json.dumps(occupied, indent=2))
for y in range(10):
    for x in range(10):
        n = occupied.get("%i:%i" % (x, y))
        if n is None:
            n = 0
        print("." if n == 0 else str(n), end="")
    print()

dangerous = list(pid for pid, n in occupied.items() if n >= 2)
print(dangerous)
print(len(dangerous))
