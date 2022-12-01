#!/usr/bin/env python3

import sys
import copy
import math
import json
import time
import traceback
import itertools
import operator
import collections

from queue import LifoQueue
import numpy as np
import tkinter as tk

def calc_hash(x, y):
    # return hash(point)
    return str(x) + ':' + str(y)

translation_table = tuple(True if ch == '#' else False for ch in next(sys.stdin)[:-1])

assert next(sys.stdin)[:-1] == ''

image_default_tmp = False
image_default = False
image_map_tmp = {}
image_map = {}
min_x = 0
max_x = 0
min_y = 0
max_y = 0

def write_map(x, y, val):
    global min_x, max_x, min_y, max_y
    h = calc_hash(x, y)
    if val == image_default_tmp:
        image_map_tmp.pop(h, None)
        return

    min_x = min(min_x, x)
    max_x = max(max_x, x)
    min_y = min(min_y, y)
    max_y = max(max_y, y)

    image_map_tmp[h] = val

def read_map_bak(x, y):
    return image_map.get(calc_hash(x, y), image_default)

def read_map(x, y):
    return image_map_tmp.get(calc_hash(x, y), image_default_tmp)

def apply_changes_map():
    global image_map, image_map_tmp, image_default, image_default_tmp
    image_map = copy.copy(image_map_tmp)
    image_default = image_default_tmp


y = 0
for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]

    for x, ch in enumerate(line):
        if ch != '#':
            continue
        write_map(x, y, True)
    y += 1

apply_changes_map()

print('Reading done!')

iterations = 50

src_indexes = tuple(
    (x, y)
    for y in range(-1,2)
    for x in range(-1,2)
)

for i in range(iterations):
    print('Iteration', i)
    print('Other pixels value', image_default)
    print('Lit pixels', sum(image_map.values()))

    image_map_tmp = {}
    if translation_table[0]:
        image_default_tmp = not image_default_tmp

    for x, y in ((x, y) for y in range(min_y - 1, max_y + 2) for x in range(min_x - 1, max_x + 2)):
        val = translation_table[int(''.join(
            str(int(read_map_bak(tx, ty)))
            for tx, ty in (
                (x + cx, y + cy)
                for cx, cy in src_indexes
            )
        ), 2)]
        write_map(x, y, val)

    apply_changes_map()

print('Done!', i)
print('Other pixels value', image_default)
print('Lit pixels', sum(image_map.values()))


for y in range(min_y - 1, max_y + 2):
    for x in range(min_x - 1, max_x + 2):
        print('#' if read_map(x, y) else '.', end='')
    print()
