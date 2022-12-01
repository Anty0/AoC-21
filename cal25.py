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

cucumber_map = []

for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]
    
    cucumber_map.append(list(1 if ch == '>' else (2 if ch == 'v' else 0) for ch in line))

cucumber_val_to_ch = {
    0: '.',
    1: '>',
    2: 'v',
}

def print_map():
    for l in cucumber_map:
        for v in l:
            print(cucumber_val_to_ch[v], end='')
        print()
    print()

print('Initial state:')
print_map()

iterations = 0
change = True
while change:
    change = False
    iterations += 1
    print('Iteration:', iterations)

    old_cucumber_map = copy.deepcopy(cucumber_map)

    for y in range(len(old_cucumber_map)):
        zero_occupied = old_cucumber_map[y][0] != 0
        last_occupied = old_cucumber_map[y][-1] == 1
        for x in range(len(old_cucumber_map[y]) - 1):
            if old_cucumber_map[y][x] == 1 and old_cucumber_map[y][x+1] == 0:
                cucumber_map[y][x] = 0
                cucumber_map[y][x+1] = 1
                change = True
        if not zero_occupied and last_occupied:
            cucumber_map[y][-1] = 0
            cucumber_map[y][0] = 1
            change = True

    old_cucumber_map = copy.deepcopy(cucumber_map)
    
    for x in range(len(old_cucumber_map[0])):
        zero_occupied = old_cucumber_map[0][x] != 0
        last_occupied = old_cucumber_map[-1][x] == 2
        for y in range(len(old_cucumber_map) - 1):
            if old_cucumber_map[y][x] == 2 and old_cucumber_map[y+1][x] == 0:
                cucumber_map[y][x] = 0
                cucumber_map[y+1][x] = 2
                change = True
        if not zero_occupied and last_occupied:
            cucumber_map[-1][x] = 0
            cucumber_map[0][x] = 2
            change = True

    # print_map()
    # if iterations > 20:
    #     break

print()

print_map()
