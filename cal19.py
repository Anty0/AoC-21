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

scanner_range = 1000
scanner_max_group_distance = scanner_range
scanner_min_in_range = 12

assert next(sys.stdin).startswith('---')

scanners = [[]]
for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]
    if len(line) == 0:
        scanners.append([])
        assert next(sys.stdin).startswith('---')
        continue
    scanners[-1].append(tuple(int(v) for v in line.split(',')))

print('Reading done!')
print('Scanners', len(scanners))


def all_combinations(beacons, min_len, max_len, start=0, depth=1):
    if depth > max_len or len(beacons) - start < min_len - depth:
        return

    for i in range(start, len(beacons)):
        # print(depth, start, i)
        if depth >= min_len:
            yield (beacons[i], )
        
        for points in all_combinations(beacons, min_len, max_len, i + 1, depth + 1):
            yield beacons[i], *points

def all_groups(beacons, length):
    combinations_cnt = length-1
    for i in range(len(beacons)):
        beacon = beacons[i]
        other_beacons = beacons[:i] + beacons[i+1:]
        for combination in all_combinations(other_beacons, combinations_cnt, combinations_cnt):
            yield (
                (
                    beacon,
                    *combination
                ),
                tuple(
                    tuple(
                        combination[j][n] - beacon[n]
                        for n in range(3)
                    )
                    for j in range(len(combination))
                )
            )

# space_cube = 2000 ** 3
# combination_hashes = {}

# for i, scanner in enumerate(scanners):
#     # print(len(scanner))
#     # print(scanner)
#     cnts = [0 for _ in range(len(scanner)+1)]
#     cnt = 0
#     for combination in all_combinations(scanner, 3, 3):
#         # print(len(combination))
#         # print(combination)
#         cnt += 1
#         cnts[len(combination)] += 1
#         print(cnt, '\t', cnts, '\t', len(combination))
#     exit()

# def gen_coord_view(beacons, coord):
#     return [v[coord] for v in beacons]

# def gen_xyz_views(beacons):
#     return [
#         gen_coord_view(beacons, c)
#         for c in range(3)
#     ]

valid_rotation_switch_mapping = tuple(
    (x, y, z)
    for x in range(3)
    for y in range(3)
    for z in range(3)
    if x != y and x != z and y != z
)

# print(valid_rotation_switch_mapping)

valid_rotation_sign_mapping = (
    (1, 1, 1),
    (1, -1, -1),
    (-1, 1, -1),
    (-1, -1, 1),

    (-1, 1, 1),
    (1, -1, 1),
    (1, 1, -1),

    (-1, -1, -1),
)

# z:
# xy
# y-x
# -x-y
# -yx
#
# -z:
# xy
# y-x
# -x-y
# -yx
#
#

def gen_rotations(beacons):
    # xyz
    # x-y-z
    # -xy-z
    # -z-yz
    return [
        [
            tuple(
                beacon[rotation[i]] * signs[i]
                for i in range(3)
            )
            for beacon in beacons
        ]
        for rotation in valid_rotation_switch_mapping
        for signs in valid_rotation_sign_mapping
    ]

def calc_hash(points):
    # points: ((x, y, z), ...)
    # return hash(points)
    return ','.join(':'.join(str(n) for n in point) for point in points)

def gen_hashes(beacons):
    hashed = {}
    for orig, diff in all_groups(beacons, 3):
        if any(any(abs(v) > scanner_max_group_distance for v in beacon_diff) for beacon_diff in diff):
            # Beacons too far away
            continue

        for orig2, diff2 in (
            (orig, diff),
            (tuple(reversed(orig)), tuple(reversed(diff)))
        ):
            h = calc_hash(diff2)
            assert h not in hashed
            hashed[h] = (orig2, diff2)
    return hashed

def precompute_scanner(orig, n):
    print('Prepare scanner', n)

    rotations = gen_rotations(orig)
    # views = [gen_xyz_views(beacons) for beacons in rotations]
    hashes = [gen_hashes(beacons) for beacons in rotations]
    return {
        'n': n,
        'orig': orig,
        'rotations': rotations,
        # 'views': views,
        'hashes': hashes,
    }

def point_diff(p1, p2):
    return tuple(
        p1[i] - p2[i]
        for i in range(3)
    )

def translate_beacons(beacons, translation_vector):
    return [
        tuple(
            beacon[n] - translation_vector[n]
            for n in range(3)
        )
        for beacon in beacons
    ]

def update_map(old_map, add_beacons):
    new_map = [*old_map]
    for beacon in add_beacons:
        if beacon not in new_map:
            new_map.append(beacon)

    return {
        'orig': new_map,
        'rotations': [new_map],
        # 'views': [gen_xyz_views(new_map)],
        'hashes': [gen_hashes(new_map)],
    }

print('Prepare map')
beacons_map = update_map(scanners.pop(0), [])

print('Prepare scanners')
scanners = [precompute_scanner(scanner, i+1) for i, scanner in enumerate(scanners)]
scanners_results = [{
    'n': 0,
    'translation_vector': (0,0,0)
}]

# print(final_map_hashes)

# print(scanners[0]['n'])
# print(scanners[0]['orig'])
# for i in range(6, 14):
#     print(scanners[0]['rotations'][i], i)
# print(beacons_map['orig'])
# print(scanners[0]['hashes'][38])
# print(beacons_map['hashes'][0])
# exit()
# scanners[1]['rotations'] = [scanners[1]['rotations'][41]]
# scanners[1]['hashes'] = [scanners[1]['hashes'][41]]

print('Setup done!')

while len(scanners) > 0:
    print('Check for mergeable scanners. Remaining: ', len(scanners))
    for i in range(len(scanners)):
        print('Test scanner ', scanners[i]['n'])
        # Try to map this scanner to final_map
        valid_merges = {}
        for ri, rhashes, key in ((ri, rhashes, key) for ri, rhashes in enumerate(scanners[i]['hashes']) for key in rhashes.keys()):
            similar_group = beacons_map['hashes'][0].get(key)
            if similar_group is None:
                continue
            sbeacon = rhashes[key][0][0]
            mbeacon = similar_group[0][0]
            # print('Found similar group ', similar_group[1], mbeacon, sbeacon)

            translation_vector_to_scanner = point_diff(mbeacon, sbeacon)
            mbeacons = [
                beacon
                for beacon in translate_beacons(beacons_map['orig'], translation_vector_to_scanner)
                if all(-scanner_range < v < scanner_range for v in beacon)
            ]
            
            # print('In range: ', len(mbeacons), '/', len(beacons_map['orig']))

            if len(mbeacons) < scanner_min_in_range:
                # print('Skip - not enough in range')
                continue

            sbeacons = scanners[i]['rotations'][ri]
            if not all((beacon in sbeacons) for beacon in mbeacons):
                # print('Skip - overlapping parts does not match')
                # for beacon in mbeacons:
                #     if beacon not in sbeacons:
                #         print(beacon)
                # print(sbeacons)
                # print(beacons_map['orig'])
                # print(scanners[i]['n'])
                # print(ri)
                # print(translation_vector_to_scanner)
                continue

            translation_vector_to_map = point_diff(sbeacon, mbeacon)
            translation_key = calc_hash((translation_vector_to_map, (ri,)))
            if translation_key in valid_merges:
                # print('Translation already in mergable. Current: ', len(valid_merges))
                continue

            sbeacons = translate_beacons(sbeacons, translation_vector_to_map)
            valid_merges[translation_key] = (translation_vector_to_map, sbeacons)
            print('Add to mergable', translation_vector_to_map,'. Current: ', len(valid_merges))
            # break


        if len(valid_merges) != 1:
            print('Skipping merge. Available merges', len(valid_merges))
            continue

        translation_vector, sbeacons = tuple(v for v in valid_merges.values())[0]

        print('Merging scanner into map. Available merges', len(valid_merges))
        beacons_map = update_map(beacons_map['orig'], sbeacons)
        scanners_results.append({
            'n': scanners[i]['n'],
            'translation_vector': translation_vector
        })
        scanners.pop(i)
        print('Merge done!')
        print('Current beacons count', len(beacons_map['orig']))
        break

# for k in beacons_map['hashes'][0].keys():
#     print(k)

# print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

# for hrot in scanners[0]['hashes']:
#     for k in hrot.keys():
#         print(k)

print('Beacons count', len(beacons_map['orig']))

max_scanner_distance = max(
    (
        (r1['n'], r2['n'], sum(abs(v) for v in point_diff(r1['translation_vector'], r2['translation_vector'])))
        for r1 in scanners_results
        for r2 in scanners_results
    ),
    key=lambda v: v[2]
)
print('Max scanner distance', max_scanner_distance)
