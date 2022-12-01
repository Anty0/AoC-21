#!/usr/bin/env python3

import sys
import copy
import math
import json
import traceback
import itertools
import operator
import collections

from queue import LifoQueue
import numpy as np
import tkinter as tk

def propagate_num(num, n, left):
    for i in (range(len(num)-1, -1, -1) if left else range(len(num))):
        if type(num[i]) == int:
            num[i] += n
            return None
        else:
            if propagate_num(num[i], n, left) is None:
                return None
    return n

def fix_nested(num, depth):
    pair = all(type(n) == int for n in num)
    if pair:
        if depth > 3:
            n1, n2 = num[0], num[1]
            num.clear()
            return True, n1, n2
        return False, None, None

    for i in range(len(num)):
        if type(num[i]) == int:
            continue

        r, n1, n2 = fix_nested(num[i], depth+1)
        if len(num[i]) == 0:
            num[i] = 0
        if r:
            if n1 is not None:
                snum = num[:i]
                n1 = propagate_num(snum, n1, True)
                num[:i] = snum
            if n2 is not None:
                snum = num[i+1:]
                n2 = propagate_num(snum, n2, False)
                num[i+1:] = snum
            return True, n1, n2
    return False, None, None


def fix_great(num):
    for i in range(len(num)):
        if type(num[i]) == int:
            if num[i] >= 10:
                v = num[i]
                num[i] = [v // 2, v // 2 + v % 2]
                return True
            continue

        if fix_great(num[i]):
            return True
    return False


def magnitude_of(num):
    if type(num) == int:
        return num
    
    return 3 * magnitude_of(num[0]) + 2 * magnitude_of(num[-1])


# print(fix_nested(num1, 0))
# print(num1)
# exit()



# num1 = json.loads(next(sys.stdin))
# print(num1)
#
# for line in sys.stdin:
#     if line[-1] == '\n':
#         line = line[:-1]
#     num2 = json.loads(line)
#     print(num2)

#     num1 = [num1, num2]
#     # num1 = num2

#     print(num1)

#     while fix_nested(num1, 0)[0] or fix_great(num1):
#         pass

#     print(num1)

# mag = magnitude_of(num1)
# print(mag)

nums = []
for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]
    nums.append(json.loads(line))

mm = 0
tn = ()
for i1 in range(len(nums)):
    print(i1, '/', len(nums))
    for i2 in range(len(nums)):
        if i1 == i2:
            continue
        num = [copy.deepcopy(nums[i1]), copy.deepcopy(nums[i2])]
        while fix_nested(num, 0)[0] or fix_great(num):
            pass
        mag = magnitude_of(num)
        if mag > mm:
            mm = mag
            tn = (nums[i1], nums[i2], num)
        # mm = max(mm, magnitude_of(num))


print(mm)
print(tn)
