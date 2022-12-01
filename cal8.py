#!/usr/bin/env python3

import sys
import math
import json
import itertools

s = 0

chi = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

valid_per_len = [
    [], # 0
    [], # 1
    ['c', 'f'], # 2
    ['a', 'c', 'f'], # 3
    ['b', 'c', 'd', 'f'], # 4
    [c for c in chi], # 5
    [c for c in chi], # 6
    [c for c in chi], # 7
]

num_to_segments = [
    ['a', 'b', 'c', 'e', 'f', 'g'], # num 0
    ['c', 'f'], # num 1
    ['a', 'c', 'd', 'e', 'g'], # num 2
    ['a', 'c', 'd', 'f', 'g'], # num 3
    ['b', 'c', 'd', 'f'], # num 4
    ['a', 'b', 'd', 'f', 'g'], # num 5
    ['a', 'b', 'd', 'e', 'f', 'g'], # num 6
    ['a', 'c', 'f'], # num 7
    ['a', 'b', 'c', 'd', 'e', 'f', 'g'], # num 8
    ['a', 'b', 'c', 'd', 'f', 'g'], # num 9
]

num_per_len = [
    [], # 0
    [], # 1
    [1], # 2
    [7], # 3
    [4], # 4
    [2, 3, 5], # 5
    [0, 6, 9], # 6
    [8], # 7
]

# 1 - 2
# 7 - 3
# 4 - 4
# 2 - 5
# 3 - 5
# 5 - 5
# 0 - 6
# 6 - 6
# 9 - 6
# 8 - 7

def find_mappings_inner(w_map, i, current, results):
    if i == len(w_map):
        results.append(current)
        return
    for c in w_map[i]:
        if c in current:
            continue
        find_mappings_inner(w_map, i + 1, current + c, results)
    

def find_mappings(w_map):
    results = []
    find_mappings_inner(w_map, 0, '', results)
    return results
        

    

for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]
    line_split = line.split(' ')
    line_middle = line_split.index('|')
    line_split1 = line_split[:line_middle]
    line_split2 = line_split[line_middle + 1:]
    # print(line_split1)
    # print(line_split2)

    mapping = [[c for c in chi] for i in range(len(chi))]

    for w in itertools.chain(line_split1, line_split2):
        valid = valid_per_len[len(w)]
        for c in w:
            ci = chi.index(c)
            mapping[ci] = list(cm for cm in mapping[ci] if cm in valid)
    
    # print(mapping)


    change = True
    while change:
        change = False
        # print('----------------------------------------')
        for w in itertools.chain(line_split1, line_split2):
            # print('-------------------')
            # print(w)
            decoded_w = list(mapping[chi.index(c)] for c in w)
            # print(decoded_w)
            
            nums = num_per_len[len(w)]
            mappings = list(m for m in find_mappings(decoded_w) if any(all(s in m for s in num_to_segments[num]) for num in nums))
            # print(mappings)

            for i in range(len(w)):
                ci = chi.index(w[i])
                valid = list(dict.fromkeys(m[i] for m in mappings))
                # print(mapping[ci])
                # print(valid)
                assert all(v in mapping[ci] for v in valid)
                if len(valid) != len(mapping[ci]):
                    mapping[ci] = valid
                    change = True
    
    print(mapping)

    outnum = ''
    for w in line_split2:
        decoded_w = list(mapping[chi.index(c)] for c in w)
        mappings = find_mappings(decoded_w)
        nums = list(
            num
            for num in num_per_len[len(w)]
            if any(all(s in m for s in num_to_segments[num]) for m in mappings)
        )
        assert len(nums) == 1
        outnum += str(nums[0])
    outnum = int(outnum)
    print(outnum)

    s += outnum

print(s)
