#!/usr/bin/env python3

import sys
import copy
import math
import json
import time
import traceback
import itertools
import functools
import operator
import collections

from queue import LifoQueue
import numpy as np
import tkinter as tk


def full_range(start, stop):
    return range(start, stop + 1)

def calc_hash(x, y, z):
    # return hash(point)
    return str(x) + ':' + str(y) + ':' + str(z)


state_default = False
state_map = {}
min_x = 0
max_x = 0
min_y = 0
max_y = 0
min_z = 0
max_z = 0

def write_map(x, y, z, val):
    global min_x, max_x, min_y, max_y, min_z, max_z
    h = calc_hash(x, y, z)
    if val == state_default:
        state_map.pop(h, None)
        return

    min_x = min(min_x, x)
    max_x = max(max_x, x)
    min_y = min(min_y, y)
    max_y = max(max_y, y)
    min_z = min(min_z, z)
    max_z = max(max_z, z)

    state_map[h] = val

def read_map(x, y):
    return state_map.get(calc_hash(x, y), state_default)

for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]

    print('Processing:', line)
    
    target, line = line.split(' ')
    target_value = False if target == 'off' else True
    ranges = tuple(tuple(full_range(*(int(s) for s in r.split('..')))) for _, r in (v.split('=') for v in line.split(',')))
    # print(ranges)

    all_coords = zip(*(
        tuple(
            v
            for v in ranges[i] for _ in range(
                functools.reduce(operator.mul, (
                    len(r) for r in ranges[:i]
                ), 1)
            )
        ) * functools.reduce(operator.mul, (
            len(r) for r in ranges[i+1:]
        ), 1)
        for i in range(len(ranges))
    ))
    # print(list(all_coords))
    
    for x, y, z in all_coords:
        write_map(x, y, z, target_value)
    
    print('Processing of line done!')

print(min_x, max_x, min_y, max_y, min_z, max_z)
print(len(state_map))
