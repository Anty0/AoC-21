#!/usr/bin/env python3

import sys

# x = 0
# y = 0
# a = 0

all_nums = []

for line in sys.stdin:
    if line[-1] == "\n":
        line = line[:-1]
    all_nums.append(line)


def calc_num(nums):
    num = []
    for l in nums:
        while len(num) < len(l):
            num.append(0)
        for i, ch in enumerate(l):
            if ch == "1":
                num[i] += 1
            elif ch == "0":
                num[i] -= 1
            else:
                print("invalid char", ch)
    return num


num = calc_num(all_nums)

print(num)

gamma = int("".join(map(lambda x: "1" if x > 0 else "0", num)), base=2)
print(gamma)
epsilon = int("".join(map(lambda x: "1" if x < 0 else "0", num)), base=2)
print(epsilon)
print(gamma * epsilon)

all_nums_tmp = all_nums
num_tmp = num
for i in range(len(num_tmp)):
    if len(all_nums_tmp) <= 1:
        break
    all_nums_tmp = list(
        filter(lambda s: s[i] == "1" if num_tmp[i] >= 0 else s[i] == "0", all_nums_tmp)
    )
    print(all_nums_tmp)
    num_tmp = calc_num(all_nums_tmp)
    print(num_tmp)

oxygen = int(all_nums_tmp[0], base=2)
print(oxygen)

all_nums_tmp = all_nums
num_tmp = num
for i in range(len(num_tmp)):
    if len(all_nums_tmp) <= 1:
        break
    all_nums_tmp = list(
        filter(lambda s: s[i] == "0" if num_tmp[i] >= 0 else s[i] == "1", all_nums_tmp)
    )
    print(all_nums_tmp)
    num_tmp = calc_num(all_nums_tmp)
    print(num_tmp)

co2 = int(all_nums_tmp[0], base=2)
print(co2)

life = oxygen * co2
print(life)
