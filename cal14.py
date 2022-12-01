#!/usr/bin/env python3

import sys
import math
import json
import itertools

template = next(sys.stdin)[:-1]
print('Template:', template)

assert next(sys.stdin)[:-1] == ''

ch_map = {}

for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]
    source, target = line.split(' -> ')
    assert source not in ch_map
    ch_map[source] = target

limit = 40

# for n in range(limit):
#     i = 0
#     while i < len(template) - 1:
#         pair = template[i:i+2]
#         # print(pair)
#         change = ch_map.get(pair)
#         if change is not None:
#             template = template[:i+1] + change + template[i+1:]
#             i += 1
#         i += 1
#     print(f'After step {n}:', len(template))

# cnt = {}
# for ch in template:
#     cnt[ch] = cnt.setdefault(ch, 0) + 1
# print(cnt)

# cnt = sorted(cnt.items(), key=lambda i: i[1])
# print(cnt)

# print(cnt[-1][1] - cnt[0][1])

pair_count = {}
for i in range(len(template) - 1):
    pair = template[i:i+2]
    # print(pair)
    pair_count[pair] = pair_count.setdefault(pair, 0) + 1

pair_count_tmp = {}
for n in range(limit):
    for k, v in pair_count.items():
        change = ch_map.get(k)
        # print(k)
        for pair in (k[0] + change, change + k[1]) if change is not None else (k,):
            # if pair == 'BB':
            # print('   ', pair)
            pair_count_tmp[pair] = pair_count_tmp.setdefault(pair, 0) + v
    pair_count = pair_count_tmp
    pair_count_tmp = {}
    print(f'After step {n}:', sum(pair_count.values()))
    # print(f'After step {n}:', pair_count)

cnt = {}
for k, v in pair_count.items():
    ch = k[0]
    cnt[ch] = cnt.setdefault(ch, 0) + v
last = template[-1]
cnt[last] = cnt.setdefault(last, 0) + 1
print(cnt)

cnt = sorted(cnt.items(), key=lambda i: i[1])
print(cnt)

print(cnt[-1][1] - cnt[0][1])
