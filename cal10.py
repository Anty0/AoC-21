#!/usr/bin/env python3

import sys
import math
import json
import itertools

ch_map = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
    ')': None,
    ']': None,
    '}': None,
    '>': None,
}

illegal_score_map = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

missing_score_map = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

results = []
stacks = []

for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]

    stack = []
    result = 0
    for ch in line:
        chs = ch_map[ch]
        if chs is None:
            che = stack.pop()
            if che != ch:
                print('Expected %s, but found %s instead.' % (che, ch))
                stack.clear()
                result = illegal_score_map[ch]
                break
        else:
            stack.append(chs)

    results.append(result)
    stacks.append(stack)

print(results)
print(sum(results))

# print(stacks)
missing_scores = sorted(
    sum(
        (score * (5**i))
        for i, score in
        enumerate(
            missing_score_map[ch]
            for ch in stack
        )
    )
    for stack in stacks if len(stack) != 0
)
print(missing_scores)
print(missing_scores[int((len(missing_scores)-1)/2)])