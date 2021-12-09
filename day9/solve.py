import sys
import string
import math
import re
from dataclasses import dataclass
from collections import defaultdict, namedtuple

inp = sys.stdin.read().strip().split("\n")

s = 0
lowpoints = set()
for r, row in enumerate(inp):
    for c, char in enumerate(row):
        if (r == 0 or int(inp[r-1][c]) > int(char)) \
            and (r == len(inp) - 1 or int(inp[r+1][c]) > int(char)) and \
            (c == len(row) - 1 or int(inp[r][c+1]) > int(char)) and \
            (c == 0 or int(inp[r][c-1]) > int(char)):
            s += int(char) + 1
            lowpoints.add((r, c))

def bfs(r, c):
    queue = [(r, c)]
    ans = 0
    visited = set()
    while queue:
        r1, c1 = queue.pop()
        if inp[r1][c1] == "9":
            continue
        if (r1, c1) in visited:
            continue

        ans += 1
        visited.add((r1, c1))
        if r1 < len(inp) - 1:
            queue.append((r1+1, c1))
        if r1 > 0:
            queue.append((r1-1, c1))
        if c1 < len(inp[0]) - 1:
            queue.append((r1, c1+1))
        if c1 > 0:
            queue.append((r1, c1-1))
    return ans


print(s)

sizes = []
for lowpoint in lowpoints:
    size = bfs(lowpoint[0], lowpoint[1])
    sizes.append(size)

print(sizes)
p = 1
for e in sorted(sizes)[-3:]:
    p *= e
print(p)
