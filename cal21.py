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


dice_cnt = 0
dice_tmp = -1
def deterministic_dice():
    global dice_tmp, dice_cnt
    dice_cnt += 1
    dice_tmp = (dice_tmp + 1) % 100
    return dice_tmp + 1


# pos = [4, 8]
pos = [6, 1]
pos_limit = 10
score = [0 for _ in pos]
score_limit = 1000
turn = 0

# normalize pos
pos = [p-1 for p in pos]

# simulate game
while all(s < score_limit for s in score):
    pos[turn] = (pos[turn] + sum(deterministic_dice() for _ in range(3))) % pos_limit
    score[turn] += pos[turn] + 1
    print('Player %i moves to space %i for a total score of %i.' % (turn, pos[turn] + 1, score[turn]))
    turn = (turn + 1) % len(pos)

# debug
print(pos)
print(score)

# calculate result
r = min(score) * dice_cnt
print(r)
