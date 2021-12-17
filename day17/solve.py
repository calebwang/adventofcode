import sys
import string
import math
import re
from statistics import median, mean
from collections import defaultdict, namedtuple, Counter

inp = sys.stdin.read().strip()
lines = inp.split("\n")

print(inp)
print(len(lines))

line = lines[0]
match = re.search("x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", line)
start_x, end_x, start_y, end_y = match.groups()
start_x, end_x, start_y, end_y = int(start_x), int(end_x), int(start_y), int(end_y)


def simulate(x_vel, y_vel):
    positions = set()
    x, y = 0, 0
    while True:
        x += x_vel
        y += y_vel
        positions.add((x, y))
        if x_vel > 0:
            x_vel -= 1
        y_vel -= 1

        if x_vel == 0 and x < start_x:
            break
        if x >= start_x and x <= end_x and y >= start_y and y <= end_y:
            return positions
        if x > end_x:
            break
        if y < min(start_y, end_y):
            break
    return False

maxy = 0
count = 0
for xv in range(0, 233):
    for yv in range(-125, 5000):
        positions = simulate(xv, yv)
        if positions:
            count += 1
            max_y_position = max([p[1] for p in positions])
            maxy = max(max_y_position, maxy)

print(count)
print(maxy)

