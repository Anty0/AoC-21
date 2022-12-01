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
from heapq import heappop, heappush
import numpy as np
import tkinter as tk

register_names = ('w', 'x', 'y', 'z')

cmd_operation_char = {
    'add': '+',
    'mul': '*',
    'div': '//',
    'mod': '%',
    'eql': '==',
}

def cmd_div(a, b):
    assert b != 0
    return operator.floordiv(a, b)

def cmd_mod(a, b):
    assert a >= 0
    assert b > 0
    return operator.mod(a, b)

def cmd_eql(a, b):
    return 1 if operator.eq(a, b) else 0

cmd_operation_fnc = {
    'add': operator.add,
    'mul': operator.mul,
    'div': cmd_div,
    'mod': cmd_mod,
    'eql': cmd_eql,
}

program_input = []
# program_input_values = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, None]
program_input_values = [None, None, None, None, None, None, None, None, None, None, None, None, None, None]
program = []

rename_table = {}

var_all_names = []

def var_rename_source():
    i = 0
    while True:
        var_name = f'var{i:05d}'
        var_all_names.append(var_name)
        yield var_name
        i += 1

# var_unused = {}
var_rename = var_rename_source()

def rename_source(var):
    if type(var) == int:
        # Constant - don't rename
        return var

    if var is None:
        # No argument - skip
        return var

    if var not in register_names:
        raise Exception('Invalid register name: %s' % var)

    if var in rename_table:
        var_name, use_cnt = rename_table[var]
        rename_table[var] = (var_name, use_cnt + 1)
        return var_name

    # Default stating value of register
    return 0

def rename_target(var):
    if var not in register_names:
        raise Exception('Invalid register name: %s' % var)

    # if var in rename_table:
    #     var_name, use_cnt = rename_table[var]
    #     if use_cnt == 0:
    #         var_unused[var_name] = True

    var_name = next(var_rename)
    rename_table[var] = (var_name, 0)
    return var_name


for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]

    cmd = line.split(' ')
    if len(cmd) >= 3 and cmd[2] not in register_names:
        cmd[2] = int(cmd[2])
    while len(cmd) < 3:
        cmd.append(None)

    cmd, a, b = cmd

    t = a # Keep 'a' temporarily in var 't', since source must be renamed before target
    b = rename_source(b)
    a = rename_source(a)
    t = rename_target(t)

    if cmd == 'inp':
        # a = None
        program_input.append(t)
    else:
        program.append((cmd, t, a, b))

def filter_unused(program, result_vars):
    var_usage = {}
    for var_name in var_all_names:
        var_usage[var_name] = 0 if var_name not in result_vars else 1

    for cmd, t, a, b in program:
        for var in (a, b):
            if type(var) is str:
                var_usage[var] += 1
    
    new_program = list(filter(lambda cmd: var_usage[cmd[1]] > 0, program))
    return new_program, len(program) != len(new_program)

def propagate_results(program):
    var_val = {}
    for i, t in enumerate(program_input):
        v = program_input_values[i]
        if v is not None:
            var_val[t] = v

    changed = False
    for i, (cmd, t, a, b) in enumerate(program):
        vals = tuple(var_val[v] if v in var_val else v for v in (a, b))
        a2, b2 = vals
        if all(type(v) is int for v in vals):
            var_val[t] = cmd_operation_fnc[cmd](*vals)
        elif cmd == 'add':
            if a2 == 0:
                var_val[t] = b2
            elif b2 == 0:
                var_val[t] = a2
        elif cmd == 'mul':
            if a2 == 0 or b2 == 0:
                var_val[t] = 0
            elif a2 == 1:
                var_val[t] = b2
            elif b2 == 1:
                var_val[t] = a2
        elif cmd == 'div':
            if a2 == 0:
                var_val[t] = 0
            elif b2 == 1:
                var_val[t] = a2
        elif cmd == 'mod':
            if a2 == 0 or b2 == 1:
                var_val[t] = 0
        elif cmd == 'eql':
            if (
                (a in program_input and type(b2) is int and (b2 >= 10 or b2 < 0)) or
                (b in program_input and type(a2) is int and (a2 >= 10 or a2 < 0))
            ):
                var_val[t] = 0

        if a2 != a or b2 != b:
            changed = True
            program[i] = (cmd, t, a2, b2)
    return changed


def print_program_as_equations():
    for t in program_input:
        print('%s = ?' % t)

    for cmd, t, a, b in program:
        print('%s = %s %s %s' % (t, a, cmd_operation_char[cmd], b))


# Try to define rules for this variable to be this value
target_variable = rename_source('z')
target_value = 0

print('Target:')
print(target_variable, '=', target_value)
print()


print('Optimizing program...')

changed = True
iterations = 0
while changed:
    changed = False
    program, changed1 = filter_unused(program, [target_variable])
    changed2 = propagate_results(program)
    changed = changed1 or changed2
    iterations += 1
    print(iterations, ': Program equation:')
    print_program_as_equations()

print('Took %i iterations to optimize program' % iterations)
print()

print('Program:')
print(program_input)
print(program)
print()

print('Equations:')
print_program_as_equations()
print()

# def try_cmd_operation_fnc(cmd, a, b):
#     try:
#         return cmd_operation_fnc[cmd](a, b)
#     except Exception:
#         return None

# def cmp_sr(sr1, sr2):
#     for val in program_input:
#         vs1 = val in sr1
#         vs2 = val in sr2

#         if not vs1 and not vs2:
#             continue

#         if vs2 and not vs1:
#             return True
#         if vs1 and not vs2:
#             return False

#         if vs1 and vs2:
#             vv1 = sr1[val]
#             vv2 = sr2[val]
#             if vv1 == vv2:
#                 continue
#             if vv1 > vv2:
#                 return False
#             if vv1 < vv2:
#                 return False

def possible_values(program_input, program):
    val_map = {}
    for t in program_input:
        val_map[t] = {}
        for i in range(1, 10):
            val_map[t][i] = [{t: i}]
    
    for i, (cmd, t, a, b) in enumerate(program):
        ra = {a: [{}]} if type(a) == int else val_map[a]
        rb = {b: [{}]} if type(b) == int else val_map[b]
        print(i, cmd, a, b, len(ra), len(rb))

        rv = {}
        for va, sal in ra.items():
            for vb, sbl in rb.items():
                try:
                    val = cmd_operation_fnc[cmd](va, vb)
                except Exception:
                    continue

                for sa in sal:
                    for sb in sbl:

                        # if val > 10000000 or val < -5000000:
                        #     continue

                        sr = {}
                        invalid = False
                        for st, sv in itertools.chain(sa.items(), sb.items()):
                            if st not in sr:
                                sr[st] = sv
                            elif sr[st] != sv:
                                invalid = True
                                break
                        if invalid:
                            continue

                        if val not in rv: #or cmp_sr(sr, rv[val]):
                            rv[val] = [sr]
                        elif sr not in rv[val]:
                            rv[val].append(sr)
                        #     for st, sv in sr.items():
                        #         if st not in rv[val] or rv[val][st] < sv:
                        #             rv[val][st] = sv

        val_map[t] = rv

    return val_map


val_map = possible_values(program_input, program)
# print(val_map)

print('Possible values:')
for v, s in val_map[target_variable].items():
    print(target_variable, '=', v)
    for option in s:
        print(option)
print('Target:')
print(target_variable, '=', target_value)
for option in val_map[target_variable][0]:
    print(option)

# var_map = {}
# for t in program_input:
#     var_map[t] = None

# for cmd, t, a, b in program:
#     assert t not in var_map
#     var_map[t] = (cmd, a, b)


# def print_var_map_as_equations():
#     for t, r in var_map.items():
#         if r is None:
#             print('%s = ?' % t)
#         else:
#             cmd, a, b = r
#             print('%s = %s %s %s' % (t, a, cmd_operation_char[cmd], b))

# print('Var map:')
# print_var_map_as_equations()
# print()

# def collect_equation(var):
#     if type(var) is int:
#         return var

#     r = var_map[var]
#     if r is None:
#         return chr(ord('a') + program_input.index(var))
    
#     cmd, a, b = r
#     return f'({collect_equation(a)} {cmd_operation_char[cmd]} {collect_equation(b)})'

# print('Target equation:')
# print(target_variable, '=', collect_equation(target_variable))
# print()
# print('Target:')
# print(target_variable, '=', target_value)
