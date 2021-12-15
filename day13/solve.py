import sys
import string
import math
import re
from statistics import median, mean
from collections import defaultdict, namedtuple

inp = sys.stdin.read().strip()
lines = inp.split("\n")
print(inp)
print(len(lines))

dts, instrs = inp.split("\n\n")
dts = dts.split("\n")
instrs = instrs.split("\n")

dots = set()

for ln in dts:
    x, y = ln.split(",")
    dots.add((int(x), int(y)))


inst = list()
for ln in instrs:
    z = ln[11:]
    axis, amt = z.split("=")
    inst.append((axis, amt))

print(inst)


def fold(paper, axis, amt):
    nset = set()
    if axis == "x":
        for dot in paper:
            dx, dy = dot
            if dx == amt:
                continue
            if dx > amt:
                nset.add((amt - (dx - amt), dy))
            else:
                nset.add((dx, dy))
    if axis == "y":
        for dot in paper:
            dx, dy = dot
            if dy == amt:
                continue
            if dy > amt:
                nset.add((dx, amt - (dy - amt)))
            else:
                nset.add((dx, dy))
    return nset

nset = dots
for i in inst:
    axis, amt = i
    nset = fold(nset, axis, int(amt))
    print(len(nset))


xs = set()
ys = set()

for x, y in nset:
    xs.add(x)
    ys.add(y)

for y in range(max(ys) + 1):
    print("".join([
        " * " if (x, y) in nset else " _ "
        for x in range(max(xs) + 1)
    ]))
