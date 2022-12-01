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
import numpy as np
import tkinter as tk


def shape_size(sx, ex, sy, ey, sz, ez):
    x, y, z = abs(ex - sx), abs(ey - sy), abs(ez - sz)
    return x*y*z

shape_space_indices = tuple(
    (x, y, z)
    for x in range(3)
    for y in range(3)
    for z in range(3)
    if x != 1 or y != 1 or z != 1
)

def shapes_merge(shapes):
    change = True
    while change:
        change = False
        for i, j in (
            (i, j)
            for i in range(len(shapes))
            for j in range(len(shapes))
        ):
            if i == j:
                continue
            # (isx, iex), (isy, iey), (isz, iez) = shapes[i]
            # (jsx, jex), (jsy, jey), (jsz, jez) = shapes[j]
            # print(shapes[i], shapes[j])
            # for k in range(3):
            #     print((
            #         shapes[i][k][0] == shapes[j][k][1] and
            #         all(
            #             shapes[i][l][0] == shapes[j][l][0] and
            #             shapes[i][l][1] == shapes[j][l][1]
            #             for l in itertools.chain(range(0, k), range(k+1, 3))
            #         ),
            #         tuple(shapes[i][m] if m != k else (shapes[j][m][0], shapes[i][m][1]) for m in range(3))
            #     ))
            k = next(
                (
                    tuple(shapes[i][m] if m != k else (shapes[j][m][0], shapes[i][m][1]) for m in range(3))
                    for k in range(3)
                    if shapes[i][k][0] == shapes[j][k][1] and
                    all(
                        shapes[i][l][0] == shapes[j][l][0] and
                        shapes[i][l][1] == shapes[j][l][1]
                        for l in itertools.chain(range(0, k), range(k+1, 3))
                    )
                ),
                None
            )

            if k is not None:
                print('Merge shapes', shapes[i], '+', shapes[j], '=>', k)
                for n in sorted((i, j), reverse=True):
                    shapes.pop(n)
                shapes.append(k)
                change = True
                break


shapes = []

for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]

    print('Processing:', line)
    
    target, line = line.split(' ')
    target_value = False if target == 'off' else True
    new_shape = tuple(
        tuple(sorted(int(s) for s in r.split('..')))
        for _, r in (
            v.split('=') for v in line.split(',')
        )
    )
    new_shape = tuple((m, v+1) for m, v in new_shape)
    print(new_shape)

    # (csx, cex), (csy, cey), (csz, cez) = new_shape
    # (sx, ex), (sy, ey), (sz, ez)
    new_shapes = []
    for shape in shapes:
        print('Check shape:', shape)
        shape_split = tuple(
            (
                min(max(s, cs), e),
                max(min(e, ce), s),
            )
            for (s, e), (cs, ce) in zip(shape, new_shape)
        )
        print(shape_split)
        (msx, mex), (msy, mey), (msz, mez) = shape_split
        (sx, ex), (sy, ey), (sz, ez) = shape
        
        shape_space = ((sx, msx, mex, ex), (sy, msy, mey, ey), (sz, msz, mez, ez))

        shape_try_list = tuple(
            tuple(
                (shape_space[i][c], shape_space[i][c+1])
                for i, c in enumerate(shape_indice)
            )
            for shape_indice in shape_space_indices
        )
        shape_try_filtered = list(
            ((sx, ex), (sy, ey), (sz, ez))
            for (sx, ex), (sy, ey), (sz, ez) in shape_try_list
            if sx != ex and sy != ey and sz != ez
        )
        shapes_merge(shape_try_filtered)

        for shape_try in shape_try_filtered:
            print('Split shape', shape_try)
            new_shapes.append(shape_try)

        # for shape_try in (
        #     (sx, msx), (sy, msy), (sz, msz),
        #     (msx, mex), (sy, msy), (sz, msz),
        #     (mex, ex), (sy, msy), (sz, msz),
        # ):
        #     pass
        # if csx != msx and csy != msy and csz != msz:
        #     print('Split shape', ((csx, msx), (csy, msy), (csz, msz)))
        #     new_shapes.append(((csx, msx), (csy, msy), (csz, msz)))
        #     # if 
        # if mex != cex and mey != cey and mez != cez:
        #     print('Split shape', ((mex, cex), (mey, cey), (mez, cez)))
        #     new_shapes.append(((mex, cex), (mey, cey), (mez, cez)))

    # to_remove = 
    # for i in range(len(shapes)):
    #     for j in range(len(shapes)):
    #         if i == j:
    #             continue
    #         if 


    if target_value:
        new_shapes.append(new_shape)
    # shapes_merge(new_shapes)
    shapes = new_shapes

        # if (
        #     (csx <= sx and cex >= ex) or
        #     (csx <= ex and cex >= sx)
#     left = max(r1.left, r2.left);
# right = min(r1.right, r2.right);
# top = max(r1.top, r2.top);
# bottom = min(r1.bottom, r2.bottom);
    print('Processing of line done!')
    print()

print(sum(shape_size(sx, ex, sy, ey, sz, ez) for (sx, ex), (sy, ey), (sz, ez) in shapes))
