#!/usr/bin/env python3

import sys
import json

counts = [0 for i in range(9)]
# vals = []

for line in sys.stdin:
    if line[-1] == "\n":
        line = line[:-1]
    # vals += (int(n) for n in line.split(','))
    for num in (int(n) for n in line.split(",")):
        counts[num] += 1

print(counts)
print(sum(counts))
# print(vals)
# print(max(vals))

for n in range(256):
    tmp_zero = counts[0]
    for i in range(1, len(counts)):
        counts[i - 1] = counts[i]
    counts[-1] = 0
    counts[8] = tmp_zero
    counts[6] += tmp_zero
    # for i in range(1, len(vals)):
    #     vals[i] -= 1
    #     if vals[i] < 0:
    #         vals[i] = 6
    #         vals.append(8)

    # print(vals)
    # print(n, len(vals))
    print(n, sum(counts))

# print(vals)
# print(len(vals))
print(sum(counts))
