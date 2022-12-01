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
from heapq import heappop, heappush
import numpy as np
import tkinter as tk


def calc_hash(hallway, rooms):
    return ':'.join(str(v) for v in hallway) + ',' + '(' + ','.join(':'.join(str(o) for o in room) for room in rooms) + ')'


# Was also trying to do it by hand, but wasn't able to get it right, so bruteforce it is.
# 
# Fortunately it takes only ~5 seconds to bruteforce it. They specified so many constrains there isn't that much valid states.

path = []
used = {}

FREE = 0
A = 1
B = 10
C = 100
D = 1000
INVALID = 10000

def path_add(p):
    cost, hallway, rooms, _ = p
    h = calc_hash(hallway, rooms)
    if h in used:
        cost_old = used[h]
        if cost >= cost_old:
            return

    heappush(path, p)
    used[h] = cost


# path_add((
#     0,
#     tuple(FREE for _ in range(11)),
#     (
#         tuple(),
#         tuple(),
#         (B, D, D, A),
#         tuple(),
#         (C, C, B, D),
#         tuple(),
#         (B, B, A, C),
#         tuple(),
#         (D, A, C, A),
#         tuple(),
#         tuple(),
#     ),
#     None
# ))

path_add((
    0,
    tuple(FREE for _ in range(11)),
    (
        tuple(),
        tuple(),
        (D, D, D, D),
        tuple(),
        (C, C, B, A),
        tuple(),
        (B, B, A, A),
        tuple(),
        (C, A, C, B),
        tuple(),
        tuple(),
    ),
    None
))

target_room = {
    A: 2,
    B: 4,
    C: 6,
    D: 8,
    INVALID: -1,
}

symbol = {
    FREE: '.',
    A: 'A',
    B: 'B',
    C: 'C',
    D: 'D',
    INVALID: '#',
}

def first_nonzero(l):
    for i in range(len(l)):
        if l[i] != 0:
            return i
    return len(l)

def print_state(hallway, rooms):
    print('#' * (len(hallway) + 2))
    print('#' + ''.join(symbol[v] for v in hallway) + '#')
    for i in range(4):
        print('#' + ''.join(symbol[room[i] if len(room) > i else INVALID] for room in rooms) + '#')
    print('#' * (len(hallway) + 2))
    print()

# print_state(path[0][1], path[0][2])

result = None
iterations = 0

while len(path) != 0:
    cost, hallway, rooms, previous = heappop(path)

    print('Cost', cost)
    print_state(hallway, rooms)

    if all(val != 0 and i == target_room[val] for i, room in enumerate(rooms) for val in room):
        result = (cost, hallway, rooms, previous)
        break

    # min_leave_value = max(hallway)

    next_room_indexes = (i for i, _ in filter(
        lambda it: any(itv != FREE and it[0] != target_room[itv] for itv in it[1]),
        sorted(
            enumerate(rooms),
            key=lambda it: next(filter(lambda x: x != FREE, it[1]), INVALID)
        )
    ))

    for i in next_room_indexes:
        pos = first_nonzero(rooms[i])

        # if rooms[i][pos] < min_leave_value:
        #     continue

        # print(i)
        # print(pos)

        for j in range(i, len(hallway)):
            if hallway[j] != 0:
                break
            if len(rooms[j]) != 0:
                continue
            path_add((
                cost + rooms[i][pos] * (pos + j - i + 1),
                tuple(o if k != j else rooms[i][pos] for k, o in enumerate(hallway)),
                tuple(
                    tuple(
                        o if i != k or l != pos else FREE
                        for l, o in enumerate(room)
                    )
                    for k, room in enumerate(rooms)
                ),
                (cost, hallway, rooms, previous)
            ))

        for j in range(i, -1, -1):
            if hallway[j] != 0:
                break
            if len(rooms[j]) != 0:
                continue
            path_add((
                cost + rooms[i][pos] * (pos + i - j + 1),
                tuple(o if k != j else rooms[i][pos] for k, o in enumerate(hallway)),
                tuple(
                    tuple(
                        o if i != k or l != pos else FREE
                        for l, o in enumerate(room)
                    )
                    for k, room in enumerate(rooms)
                ),
                (cost, hallway, rooms, previous)
            ))
    
    for i in range(len(hallway)):
        if hallway[i] == 0:
            continue
        t = target_room[hallway[i]]

        if any(v != FREE and v != hallway[i] for v in rooms[t]):
            # Room still contains invalid occupants
            continue
        
        r = (i + 1, t + 1) if t > i else (t, i)
        if any(hallway[j] != 0 for j in range(*r)):
            continue

        room_pos = first_nonzero(rooms[t]) - 1

        path_add((
            cost + hallway[i] * (room_pos + abs(i - t) + 1),
            tuple(o if k != i else FREE for k, o in enumerate(hallway)),
            tuple(
                tuple(
                    o if t != k or l != room_pos else hallway[i]
                    for l, o in enumerate(room)
                )
                for k, room in enumerate(rooms)
            ),
                (cost, hallway, rooms, previous)
        ))
    
    # path.sort(key=lambda p: -p[0])
    # for cost, hallway, rooms in path:
    #     print('Cost', cost)
    #     print_state(hallway, rooms)
    print('Path options', len(path))
    iterations += 1
    print('Path iterations', iterations)
    # if iterations >= 2:
    #     break

def print_result(result):
    if result is None:
        return
    cost, hallway, rooms, previous = result
    print('Cost', cost)
    print_state(hallway, rooms)
    print_result(previous)


print()
print('Start result')
print()
print_result(result)
print('End result')



#############
#...........#
###D#C#B#C###
  #D#A#A#B#
  #########

#############
#.........B.#
###D#C#.#C###
  #D#A#A#B#
  #########

# 4B

#############
#A........B.#
###D#C#.#C###
  #D#A#.#B#
  #########

# 8A

#############
#A........B.#
###D#.#C#.###
  #D#A#C#B#
  #########

# 5+4C

#############
#AA.......B.#
###D#.#C#.###
  #D#.#C#B#
  #########

# 5A

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########

# 8+6B
# 9+9D
# 3+3A


# A 8+5+3+3 * 1
# B 4+8+6   * 10
# C 5+4     * 100
# D 9+9     * 1000


#############
#...B......A#
###D#C#.#C###
  #D#A#.#B#
  #########

# 6A
# 5B

#############
#...B......A#
###D#.#C#.###
  #D#A#C#B#
  #########

# 5+4C

#############
#.A........A#
###D#B#C#.###
  #D#B#C#.#
  #########

# 3A
# 3B
# 4A
# 7B
# 9+9D
# 9+3A

# A 6+9   * 1
# B 5+8+2 * 10
# C 5+4   * 100
# D 9+9   * 1000

# A 6+3+4+9+3 * 1
# B 5+3+7     * 10
# C 5+4       * 100
# D 9+9       * 1000
