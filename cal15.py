#!/usr/bin/env python3

import sys
import math
import json
import itertools

from queue import LifoQueue
import numpy as np
import tkinter as tk


grid = []

for line in sys.stdin:
    if line[-1] == '\n':
        line = line[:-1]
    grid.append([int(ch) for ch in line])

multiplier = 5

def mod(v):
    return v % 9 if v > 9 else v

for y in range(len(grid)):
    tmp = list(grid[y])
    for m in range(1, multiplier):
        tmp += [mod(v + m) for v in grid[y]]
    grid[y] = tmp
leny = len(grid)
for m in range(1, multiplier):
    for y in range(leny):
        grid.append([mod(v + m) for v in grid[y]])

grid = np.array(grid)


min_val = min(min(l) for l in grid)
max_path = sum(sum(l) for l in grid)
print('Min value:', min_val)
print('Max path:', max_path)

adjacent = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def find_adjacent(x, y, l):
    ly = len(l)
    lx = len(l[0]) if ly != 0 else 0
    for xd, yd in adjacent:
        xr, yr = x + xd, y + yd
        if xr < lx and xr >= 0 and yr < ly and yr >= 0:
            yield xr, yr

ty, tx = len(grid) - 1, len(grid[-1]) - 1
print('Target: ', tx, ty)

def print_in_color(txt_msg,fore_tupple,back_tupple):
    #prints the text_msg in the foreground color specified by fore_tupple with the background specified by back_tupple 
    #text_msg is the text, fore_tupple is foregroud color tupple (r,g,b), back_tupple is background tupple (r,g,b)
    rf,gf,bf=fore_tupple
    rb,gb,bb=back_tupple
    msg='{0}{1}{2}'
    mat='\33[38;2;' + str(rf) +';' + str(gf) + ';' + str(bf) + ';48;2;' + str(rb) + ';' +str(gb) + ';' + str(bb) +'m' 
    print(msg.format(mat, txt_msg, '\33[0m'), end='')
    # print() # returns default print color to back to black

# print_in_color(msg, (0,255,255),(0,127,127))

def print_grid(grid, path):
    print()
    val_max = max(max(l) for l in grid)
    for y, l in enumerate(grid):
        for x, v in enumerate(l):
            # if :
            #     print_in_color(, (255, 255, 255), (255, 255, 0))
            # else:
            # print(int(v / cost_max * 9), end='')
            # val = int(v / cost_max * 255 * 4)
            # r = max(0, min(255, val - 255*3))
            # g = max(0, min(255, 255 - val))
            # b = max(0, min(255, val - 255*1, 255*3 - val))
            #'{0}{1}{2}'.format(hex(r), hex(g), hex(b))
            val = int(v / val_max * 255)
            r = val
            g = 0
            b = 0
            print_in_color('+' if (x, y) in path else ' ', (255, 255, 255), (r, g, b))
        print()
    print()

# print_grid(grid, [])


width, height = 500, 500

root = tk.Tk()
root.title("Grid")

frame = tk.Frame()
frame.pack()

canvas = tk.Canvas(frame, width=width, height=height)
rows, cols = grid.shape
rect_width, rect_height = width // rows, height // cols

def draw_grid(grid, path):
    val_max = max(max(l) for l in grid)
    canvas.delete('all')
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            x0, y0 = x * rect_width, y * rect_height
            x1, y1 = x0 + rect_width-1, y0 + rect_height-1
            color = "#%02x%02x%02x" % (int(val / val_max * 255), 0, 0)
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color, width=0)
            if (x, y) in path:
                canvas.create_line(x0, y0, x1, y1, fill='white')
                canvas.create_line(x0, y1, x1, y0, fill='white')
    
    root.update_idletasks()
    root.update()

canvas.pack()

# root.mainloop()

draw_grid(grid, [(0,0), (tx,ty)])

# costs = [[max_path for _ in range(len(grid[-1]))] for _ in range(len(grid))]
costs = np.empty(grid.shape)  
costs.fill(max_path)
costs[0][0] = 0 # Start position

def range2d(l):
    ly = len(l)
    lx = len(l[0]) if ly != 0 else 0
    return ((x, y) for x in range(lx) for y in range(ly))

grid_range = tuple((x, y, xi, yi) for x, y in range2d(grid) for xi, yi in find_adjacent(x, y, grid))
print('Per cycle: ', len(grid_range))

i = 0
change = True
while change:
    change = False
    print('-', end='', flush=True)
    i += 1

    for x, y, xi, yi in grid_range:
        cost_old = costs[y][x]
        cost = costs[yi][xi] + grid[y][x]
        if cost < cost_old:
            change = True
            costs[y][x] = cost
    
print()

draw_grid(costs, [])

print('Target cost: ', costs[ty][tx])
print('Iterations: ', i)

draw_grid(costs, [])

# path = [(tx, ty)]

path = LifoQueue()
path.put((0, 0, []))
results = []

# cx, xy = tx, ty
# while cx != 0 or cy != 0:
i = 0
while not path.empty():
# for _ in range(3):
    x, y, previous = path.get()
    # print(x, y, cost, path[:5])

    if x == tx and y == ty:
        results.append(previous + [(x, y)])
        break
        # continue

    for xi, yi in find_adjacent(x, y, grid):
        if costs[yi][xi] == costs[y][x] + grid[yi][xi]:
            path.put((xi, yi, previous + [(x, y)]))
    
    i = (i + 1) % 1000000
    if i == 0:
        print(path.qsize())
        draw_grid(costs, [(x, y)] + [(x, y) for x, y in previous])

print('Available paths: ', len(results))

draw_grid(costs, results[0])
# print_grid(costs, results[0])

root.mainloop()
