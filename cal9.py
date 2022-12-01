#!/usr/bin/env python3

import sys
import math
import json
import itertools

# counts = [0 for i in range(9)]
# vals = []

# s = 0
# c = 0

vals = []

for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]
    vals.append(list(int(c) for c in line))

height = len(vals)
width = len(vals[0])

points = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def neigh(x, y):
    return ((x2, y2) for x2, y2 in ((x+x3, y+y3) for x3, y3 in points) if x2 >= 0 and x2 < width and y2 >= 0 and y2 < height)

l = []

for i in range(height):
    for j in range(width):
        if all(vals[y][x] > vals[i][j] for x, y in neigh(j, i)):
            l.append((j, i))

lv = [vals[y][x] for x, y in l]

print(lv)

print(sum(lv) + len(lv))


def find_neigh(p):
    l = [p]
    for x, y in l:
        for x2, y2 in neigh(x, y):
            if (x2, y2) not in l and vals[y2][x2] < 9:
                l.append((x2, y2))
    return l


nei = [find_neigh(p) for p in l]
neis = sorted(nei, key=lambda n: -len(n))

for n in neis:
    print(n)
    print([vals[y][x] for x, y in n])

print(len(neis[0]), len(neis[1]), len(neis[2]))
print(len(neis[0]) * len(neis[1]) * len(neis[2]))