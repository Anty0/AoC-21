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

def calc_hash(vals):
    return ':'.join(str(v) for v in vals)

# 1        2        3  
# 1  2  3  1  2  3  1  2  3  
# 123123123123123123123123123

# 1  3
# 3  444
# 6  555555
# 7  6666666
# 6  777777
# 3  888
# 1  9


dirac_dice = [
    (1, 3),
    (3, 4),
    (6, 5),
    (7, 6),
    (6, 7),
    (3, 8),
    (1, 9),
]

assert sum(c for c, n in dirac_dice) == 3*3*3

pos_limit = 10
score_limit = 21

# init_pos = (4, 8)
init_pos = (6, 1)
init_pos = tuple(p-1 for p in init_pos)
init_score = tuple(0 for _ in init_pos)
init_state = (init_pos, init_score, 1)

states = {}
new_states = {}
states_done = {}

def state_add(states, pos, score, val):
    h = calc_hash((*pos, *score))
    _, _, old_val = states.get(h, (pos, score, 0))
    states[h] = (pos, score, old_val + val)

state_add(states, *init_state)

print(states)

# score = {}
# score[calc_hash((0, 0))] = ((0, 0), 1)

turn = 0
while len(states) != 0:
    for pos, score, n in states.values():
        if any(s >= score_limit for s in score):
            # Keep winning states
            state_add(states_done, pos, score, n)
            continue
            
        for count, val in dirac_dice:
            new_pos = list(pos)
            new_score = list(score)
            new_pos[turn] = (new_pos[turn] + val) % pos_limit
            new_score[turn] = new_score[turn] + new_pos[turn] + 1
            state_add(new_states, tuple(new_pos), tuple(new_score), n * count)
    states = new_states
    new_states = {}
    turn = (turn + 1) % len(init_pos)
    print('Turn done. States', len(states), '. States done', len(states_done))
    # if len(states) < 50:
    #     print(states)


# calculate result
wins = [0 for _ in init_pos]
for _, score, n in states_done.values():
    for i, v in enumerate(score):
        if v >= score_limit:
            wins[i] += n
            break

print('Wins', wins)
print('Top wins', max(wins))
