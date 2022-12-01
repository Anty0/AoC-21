#!/usr/bin/env python3

import sys
import math
import json
import itertools


grid = []

for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]
    grid.append([int(ch) for ch in line])

adjacent = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x != 0 or y != 0]
# print(adjacent)

def range2d(l):
    ly = len(l)
    lx = len(l[0]) if ly != 0 else 0
    return ((x, y) for x in range(lx) for y in range(ly))

def find_adjacent(x, y, l):
    ly = len(l)
    lx = len(l[0]) if ly != 0 else 0
    for xd, yd in adjacent:
        xr, yr = x + xd, y + yd
        if xr < lx and xr >= 0 and yr < ly and yr >= 0:
            yield xr, yr
        
def print_grid():
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            print(grid[y][x], end='')
        print()
    print()


limit = 1000
cnt = 0
all_flash = 0

print_grid()

for n in range(limit):
    to_flash = []
    for x, y in range2d(grid):
        grid[y][x] += 1
        if grid[y][x] > 9:
            to_flash.append((x, y))
    
    i = 0
    while i < len(to_flash):
        xt, yt = to_flash[i]
        for x, y in find_adjacent(xt, yt, grid):
            grid[y][x] += 1
            if (x, y) not in to_flash and grid[y][x] > 9:
                to_flash.append((x, y))
        i += 1
    
    for x, y in to_flash:
        grid[y][x] = 0
    
    cnt += len(to_flash)

    print('%i:' % (n + 1))
    print_grid()

    if all((x, y) in to_flash for x, y in range2d(grid)):
        all_flash = n + 1
        break

print(cnt)
print(all_flash)
