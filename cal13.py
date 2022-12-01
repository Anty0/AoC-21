#!/usr/bin/env python3

import sys
import math
import json
import itertools

dots = []
max_x = 0
max_y = 0

for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]
    
    if len(line) == 0:
        break

    x, y = tuple(int(t) for t in line.split(','))
    max_x = max(max_x, x + 1)
    max_y = max(max_y, y + 1)
    dots.append((x, y))

dot_map = [[False for _ in range(max_x)] for _ in range(max_y)]

def print_dot_map():
    for y in range(max_y):
        for x in range(max_x):
            print('#' if dot_map[y][x] else '.', end='')
        print()
    print()

print_dot_map()

for x, y in dots:
    dot_map[y][x] = True

print_dot_map()


fold_prefix = 'fold along '

for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]

    assert line.startswith(fold_prefix)
    line = line[len(fold_prefix):]

    ch, val = line.split('=')
    val = int(val)

    assert ch in ('x', 'y')

    if ch == 'x':
        for x in range(val, max_x):
            tx = val - (x - val)
            for y in range(max_y):
                dot_map[y][tx] = dot_map[y][tx] or dot_map[y][x]
        for y in range(max_y):
            dot_map[y] = dot_map[y][:val]
        max_x = val
    else:
        for y in range(val, max_y):
            ty = val - (y - val)
            for x in range(max_x):
                dot_map[ty][x] = dot_map[ty][x] or dot_map[y][x]
        dot_map = dot_map[:val]
        max_y = val
    
    print_dot_map()

print(sum(sum(l) for l in dot_map))
