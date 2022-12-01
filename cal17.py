#!/usr/bin/env python3

import sys
import math
import json
import traceback
import itertools
import operator
import collections

from queue import LifoQueue
import numpy as np
import tkinter as tk

# target area: x=217..240, y=-126..-69
x=(217, 240)
y=(-126, -69)

# # target area: x=20..30, y=-10..-5
# x=(20, 30)
# y=(-10, -5)

n = 0
v = 1
while v <= x[1]:
    n += 1
    v += n + 1
    if v >= x[0]:
        n += 1
        break

min_vel_x = n

# n = 0
# v = 1
# while v <= x[1]:
#     n += 1
#     v += n + 1

# max_vel_x = n
max_vel_x = x[1]

# def to_target(n):
#     i = 0
#     p = n
#     s = n - 1
#     while p >= y[0] or s > 0:
#         i += 1
#         p += s
#         s -= 1
#         if p <= y[1] and p + s <= y[0]:
#             break
#     return i

# n = 0
# v = 1
# while to_target(n) <= max_vel_x:
#     n += 1
#     v += n + 1

# min_vel_y = n
min_vel_y = y[0]
max_vel_y = -y[0] - 1



def check_path(vx, vy, tx, ty):
    x, y = 0, 0
    while x <= tx[1] and (y >= ty[0] or vy > 0):
        x += vx
        y += vy
        vx = 0 if vx == 0 else (vx - 1 if vx > 0 else vx + 1)
        vy -= 1
        if tx[0] <= x <= tx[1] and ty[0] <= y <= ty[1]:
            return True
    return False



def calc_path(vx, vy, lx, ly):
    x, y = 0, 0
    yield x, y
    while x <= lx and y >= ly:
        x += vx
        y += vy
        vx = 0 if vx == 0 else (vx - 1 if vx > 0 else vx + 1)
        vy -= 1
        yield x, y

def print_map(tx, ty, path, lx, ly):
    print(tx, lx)
    print(ty, ly)
    print(path)
    for y in range(ly[1], ly[0], -1):
        for x in range(lx[0], lx[1]):
            print('#' if (x, y) in path else ('T' if tx[0] <= x <= tx[1] and ty[0] <= y <= ty[1] else '.'), end='')
        print()


print((min_vel_x, max_vel_x), (min_vel_y, max_vel_y))
cnt = 0
for vx in range(min_vel_x, max_vel_x+1):
    for vy in range(min_vel_y, max_vel_y+1):
        if check_path(vx, vy, x, y):
            cnt += 1
print('Total: ', cnt)

# path = sum((list(calc_path(max_vel_x, vy, x[1], y[0])) for vy in range(min_vel_y, max_vel_y + 1)), start=[])
# print(path)

# max_height = max(p[1] for p in path)
# print('Max height: ', max_height)

# print_map(x, y, path, (0-3, x[1]+3), (y[0]-3, sum(i for i in range(max_vel_y + 1))+3))
