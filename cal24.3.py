#!/usr/bin/env python3

import functools
import operator

# W = [   4,   5,   9,   8,   9,   9,   2,   9,   9,   4,   6,   1,   9,   9] # Max
W = [   1,   1,   9,   1,   2,   8,   1,   4,   6,   1,   1,   1,   5,   6] # Min
Z = [   1,   1,   1,   1,  26,   1,  26,   1,   1,  26,  26,  26,  26,  26]
X = [  11,  14,  15,  13, -12,  10, -15,  13,  10, -13, -13, -14,  -2,  -9]
Y = [  14,   6,   6,  13,   8,   8,   7,  10,   8,  12,  10,   8,   8,   7]

# 1 11 14
# 1 14 6
# 1 15 6
# 1 13 13
# 26 -12 8
# 1 10 8
# 26 -15 7
# 1 13 10
# 1 10 8
# 26 -13 12
# 26 -13 10
# 26 -14 8
# 26 -2 8
# 26 -9 7

MZ = [functools.reduce(operator.mul, Z[i+1:], 1) - 1 for i in range(14)]

def run():
    w = 0
    x = 0
    y = 0
    z = 0

    s = []

    print("{i}\t{W[i]}\t{Z[i]}\t{X[i]}\t{Y[i]}\t{z_add}\t{x}\t{sv}\t{z > MZ[i]}\t{MZ[i]}\t{z}\t{z % 26}\t{s}")

    for i in range(14):
        x = (z % 26) + X[i]
        z //= Z[i]

        sv = s[-1] if len(s) != 0 else 0
        if Z[i] != 1:
            s.pop()


        z_add = x != W[i]
        if x != W[i]:
            z *= 26
            z += W[i] + Y[i]
            s.append(W[i] + Y[i])
            

        print(f"{i}\t{W[i]}\t{Z[i]}\t{X[i]}\t{Y[i]}\t{z_add}\t{x}\t{sv}\t{z > MZ[i]}\t{MZ[i]}\t{z}\t{z % 26}\t{s}")

    return z

print(run())
print(W)
print(''.join(str(w) for w in W))

# n = 99989999999999
# while n > 0:
#     sn = str(n)
#     n -= 1
#     if sn.count('0') != 0:
#         continue
#     W = tuple(int(ch) for ch in str(n))

#     z = run()

#     print(z, W)
#     if z == 0:
#         break

    # w = W[i]
    # x *= 0
    # x += z
    # x %= 26
    # z /= Z[i]
    # x += X[i]
    # x = 1 if x == w else 0
    # x = 1 if x == 0 else 0
    # y *= 0
    # y += 25
    # y *= x
    # y += 1
    # z *= y
    # y *= 0
    # y += w
    # y += Y[i]
    # y *= x
    # z += y

# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 15
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 6
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 13
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 13
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -12
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 8
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 10
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 8
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -15
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 7
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 13
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 10
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 10
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 8
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -13
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 12
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -13
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 10
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -14
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 8
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -2
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 8
# mul y x
# add z y
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -9
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 7
# mul y x
# add z y