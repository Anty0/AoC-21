#!/usr/bin/env python3

import sys
import math
import json
import itertools


graph = {}
big_caves = []
small_caves = ['start', 'end']

for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]

    path_from, path_to = line.split('-')
    graph.setdefault(path_from, []).append(path_to)
    graph.setdefault(path_to, []).append(path_from)

    for p in (path_from, path_to):
        if p.lower() == p:
            if p not in small_caves:
                small_caves.append(p)
        else:
            if p not in big_caves:
                big_caves.append(p)

print(big_caves)
print(small_caves)
print(graph)

def get_paths(path, visited, used_small, length):
    # print('!!!', length, path, visited)
    for possible_next in graph[path[-1]]:
        if possible_next == 'end':
            yield path + [possible_next], length + 1
            continue

        if possible_next in visited:
            if not used_small and possible_next != 'start':
                for result in get_paths(path + [possible_next], visited, True, length + 1):
                    yield result
            continue

        visited_next = visited
        if possible_next in small_caves:
            visited_next = visited + [possible_next]
        for result in get_paths(path + [possible_next], visited_next, used_small, length + 1):
            yield result

# paths = []
# cnt = 0
# for path, length in get_paths(['start'], ['start'], False, 0):
#     if (path, length) in paths:
#         continue
#     paths.append((path, length))
#     print(length, ','.join(path))
#     cnt += 1

# print(cnt)
paths = list(get_paths(['start'], ['start'], False, 0))
print(len(paths))

# paths_uniq = []
# for item in paths:
#     if item not in paths_uniq:
#         paths_uniq.append(item)

# print(len(paths_uniq))

for path, length in paths:
    print(length, ','.join(path))

print(len(paths))
