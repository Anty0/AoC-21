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

variable_names = ('w', 'x', 'y', 'z')

program = []

for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]
    cmd = line.split(' ')
    if len(cmd) >= 3 and cmd[2] not in variable_names:
        cmd[2] = int(cmd[2])
    while len(cmd) < 3:
        cmd.append(None)
    program.append(cmd)

print(program)

expected_input = []

memory = {
    'w': None,
    'x': None,
    'y': None,
    'z': '0',
}

program_counter = len(program) - 1

def inverse_inp(a, b):
    assert b is None
    # inp = a
    expected_input.append(memory[a])
    # print(program_counter+1, ': Read expect', memory[a])
    memory[a] = None

def inverse_add(a, b):
    v1 = memory[a]
    if v1 is None:
        # add ? ? = ?
        # We don't need any specific value
        return

    v2 = b if type(b) is int else memory[b]
    if v2 is None:
        # add ? ? = v1
        # add (v1 - b) (v1 - a) = v1
        memory[a] = '(%s - %s%i)' % (v1, b, program_counter+1)
        memory[b] = '(%s - %s%i)' % (v1, a, program_counter+1)
        return

    # add ? v2 = v1
    # add (v1 - v2) v2 = v1
    memory[a] = '(%s - %s)' % (v1, v2)

def inverse_mul(a, b):
    v1 = memory[a]
    if v1 is None:
        # mul ? ? = ?
        # We don't need any specific value
        return

    v2 = b if type(b) is int else memory[b]
    if v2 is None:
        # mul ? ? = v1
        # mul (v1 / b) (v1 / a) = v1
        memory[a] = '(%s / %s%i)' % (v1, b, program_counter+1)
        memory[b] = '(%s / %s%i)' % (v1, a, program_counter+1)
        return


    # mul ? v2 = v1
    # mul (v1 / v2) v2 = v1
    memory[a] = '(%s / %s)' % (v1, v2)

def inverse_div(a, b):
    v1 = memory[a]
    v2 = b if type(b) is int else memory[b]
    if v1 is None:
        # div ? ?[!=0] = ?
        # We don't need any specific value
        # but we need to constrain b to !=0
        if v2 is None:
            memory[b] = '(?[!=0])'
        elif type(b) is int:
            if b == 0:
                raise 'Invalid instruction'
        else:
            memory[b] = '(%s[!=0])' % v2
        return

    if v2 is None:
        # div ? ?[!=0] = v1
        # div (b * v1) (a / v1)[!=0] = v1
        memory[a] = '(%s%i * %s)' % (b, program_counter+1, v1)
        memory[b] = '(%s%i * %s)[!=0]' % (a, program_counter+1, v1)
        return

    # div ? v2[!=0] = v1
    # div (v1 * v2) v2[!=0] = v1
    memory[a] = '(%s * %s)' % (v1, v2)
    if type(b) is int:
        if b == 0:
            raise 'Invalid instruction'
    else:
        memory[b] = '(%s[!=0])' % v2

def inverse_mod(a, b):
    v1 = memory[a]
    v2 = b if type(b) is int else memory[b]
    if v1 is None:
        # mod ?[>=0] ?[>0] = ?
        # We don't need any specific value
        # but we need to constrain b to >0 and a to >=0
        memory[a] = '(?[>=0])'
        if v2 is None:
            memory[b] = '(?[>0])'
        elif type(b) is int:
            if b <= 0:
                raise 'Invalid instruction'
        else:
            memory[b] = '(%s[>0])' % v2
        return

    if v2 is None:
        # mod ?[>=0] ?[>0] = v1
        # mod (n * b + v1)[>=0] (? > v1)[>0] = v1
        memory[a] = '(n * %s%i + %s)[>=0]' % (b, program_counter+1, v1)
        memory[b] = '(? > %s)[>0]' % v1
        return

    # mod ?[>=0] v2[>0] = v1
    # mod (n * v2 + v1)[>=0] v2[>0] = v1
    memory[a] = '(n * %s + %s)[>=0]' % (v2, v1)
    if type(b) is int:
        if b <= 0:
            raise 'Invalid instruction'
    else:
        memory[b] = '(%s[>0])' % v2

def inverse_eql(a, b):
    v1 = memory[a]
    if v1 is None:
        # eql ? ? = ?
        # We don't need any specific value
        return

    v2 = b if type(b) is int else memory[b]
    if v2 is None:
        memory[a] = '(?[!=%s%i])' % (b, program_counter+1)
        memory[a] = '(?[!=%s%i])' % (a, program_counter+1)
        return

    if v1 == 0:
        # eql ?[!=v2] v2 = 1
        memory[a] = '(?[!=%s])' % v2
        return

    # eql v2 v2 = 1
    memory[a] = v2


inverse_command = {
    'inp': inverse_inp, # a - Read an input value and write it to variable a.
    'add': inverse_add, # a b - Add the value of a to the value of b, then store the result in variable a.
    'mul': inverse_mul, # a b - Multiply the value of a by the value of b, then store the result in variable a.
    'div': inverse_div, # a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
    'mod': inverse_mod, # a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
    'eql': inverse_eql, # a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.

}

while program_counter >= 0:
    command, a, b = program[program_counter]

    print('Invert command:', command, a, b)

    inverse_command[command](a, b)

    print(memory)
    print()

    program_counter -= 1

# print(memory)

print('Expected input')
while len(expected_input) != 0:
    print(expected_input.pop())
