#!/usr/bin/env python3

import sys
import math
import json
import traceback
import itertools
import operator
import collections

from queue import LifoQueue
import numpy as np
import tkinter as tk


for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]

    print('Processing: ', line)
    print('Bits: ', ''.join(list(bit for ch in line for bit in "{0:04b}".format(int(ch, 16)))))

    version_sum = 0

    pos_bits = 0
    bits_read = (bit for ch in line for bit in "{0:04b}".format(int(ch, 16)))

    def read_padding():
        # global pos_bits
        # n = 0
        # while pos_bits != 0:
        #     take(1)
        #     n += 1
        # return n
        return 0

    def take(bites, n):
        global pos_bits
        bits = ''.join(list(itertools.islice(bites, n)))
        print(n, bits)
        assert len(bits) == n
        pos_bits = (pos_bits + n) % 4
        return bits

    def takei(bites, n):
        bits = int(take(bites, n), 2)
        print(n, bits)
        return bits

    def read_packet(bites):
        global version_sum

        packet_len = 6

        print('version')
        version = takei(bites, 3)
        version_sum += version

        print('type_id')
        type_id = takei(bites, 3)
        if type_id == 4:
            print('literal')
            val = ''
            while takei(bites, 1):
                val += take(bites, 4)
                packet_len += 5
            val += take(bites, 4)
            packet_len += 5
            print('padding')
            return packet_len + read_padding(), int(val, 2), int(val, 2)
        else:
            print('operator')
            data = []
            vals = []
            if takei(bites, 1):
                print('packet_limit')
                packet_limit = takei(bites, 11)
                subpacket_len = 0
                try:
                    for i in range(packet_limit):
                        l, d, v = read_packet(bites)
                        print('step', v, l, d)
                        subpacket_len += l
                        data.append(d)
                        vals.append(v)
                except Exception:
                    print("!!!OWERFLOW")
                    traceback.print_exc()
                    pass
                packet_len += 1 + subpacket_len
            else:
                print('len_limit')
                len_limit = takei(bites, 15)
                subpacket_len = 0
                bites_lim = itertools.islice(bites, len_limit)
                try:
                    while subpacket_len < len_limit:
                        l, d, v = read_packet(bites_lim)
                        print('step', v, l, d)
                        subpacket_len += l
                        data.append(d)
                        vals.append(v)
                        print('len_limit', subpacket_len, len_limit)
                    assert subpacket_len == len_limit
                except Exception:
                    print("!!!OWERFLOW")
                    traceback.print_exc()
                    pass
                packet_len += 1 + subpacket_len
            
            type_name = 'unknown'
            val = vals[0] if len(vals) > 0 else 0
            if type_id == 0:
                type_name = 'sum'
                val = sum(vals)
            elif type_id == 1:
                type_name = 'product'
                val = collections.deque(itertools.accumulate(vals, operator.mul), maxlen=1).pop()
            elif type_id == 2:
                type_name = 'min'
                val = min(vals)
            elif type_id == 3:
                type_name = 'max'
                val = max(vals)
            elif type_id == 5:
                type_name = 'greater than'
                # assert len(vals) == 2
                val = 1 if len(vals) == 2 and vals[0] > vals[1] else 0
            elif type_id == 6:
                type_name = 'less than'
                # assert len(vals) == 2
                val = 1 if len(vals) == 2 and vals[0] < vals[1] else 0
            elif type_id == 7:
                type_name = 'equal to'
                # assert len(vals) == 2
                val = 1 if len(vals) == 2 and vals[0] == vals[1] else 0

            return packet_len + read_padding(), (type_name, val, data), val

    l, d, v = read_packet(bits_read)
    print(version_sum, v, l, d)
