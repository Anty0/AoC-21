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


def print_program_as_equations():
    for t in program_input:
        print('%s = ?' % t)

    for cmd, t, a, b in program:
        print('%s = %s %s %s' % (t, a, cmd_operation_char[cmd], b))

target_variable = rename_source('z')

def program_real_input_gen_fnc():
    yield tuple(int(ch) for ch in str(99999999999999))
    yield tuple(int(ch) for ch in str(11111111111111))
    # yield tuple(int(ch) for ch in '00001700514060')
    # yield tuple(int(ch) for ch in '1121')
    # yield tuple(int(ch) for ch in '9998')
    # yield tuple(int(ch) for ch in '1118')
    # n = 99999999999999
    # while n > 0:
    #     yield tuple(int(ch) for ch in str(n))
    #     n -= 1


program_real_input_gen = program_real_input_gen_fnc()

print('Program:')
print(program_input)
print(program)
print()

print('Equations:')
print_program_as_equations()
print()

while True:
    try:
        program_real_input = next(program_real_input_gen, None)
        if program_real_input is None:
            break
        print(program_real_input)
        memory = {}

        for i, t in enumerate(program_input):
            memory[t] = program_real_input[i]

        for cmd, t, a, b in program:
            a, b = (v if type(v) == int else memory[v] for v in (a, b))
            memory[t] = cmd_operation_fnc[cmd](a, b)

        # print(memory)

        # print()
        # print('Target:')
        print('Result:', target_variable, '=', memory[target_variable])
        if memory[target_variable] == 0:
            break
    except Exception as e:
        print('Skip: Exception:', e)
