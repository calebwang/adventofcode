import sys
import re
from collections import defaultdict

lines = sys.stdin.read().split("\n")



vents = set()
for line in lines:
    if not line:
        continue
    m = re.match("(\d+),(\d+) -> (\d+),(\d+)", line)
    x1, y1, x2, y2 = map(int, m.groups())
    vents.add((x1, y1, x2, y2))


points = defaultdict(lambda: 0)

for vent in vents:
    x1, y1, x2, y2 = vent
    if x1 == x2:
        if y2 > y1:
            for i in range(y1, y2+1):
                points[(x1, i)] += 1
        else:
            for i in range(y2, y1+1):
                points[(x1, i)] += 1

    elif y1 == y2:
        if x2 > x1:
            for i in range(x1, x2+1):
                points[(i, y1)] += 1
        else:
            for i in range(x2, x1+1):
                points[(i, y1)] += 1
    else:
        if x1 > x2:
            if y1 > y2:
                for i in range(x1 - x2 + 1):
                    points[(x1 - i, y1 - i)] += 1
            else:
                for i in range(x1 - x2 + 1):
                    points[(x1 - i, y1 + i)] += 1
        else:
            if y1 > y2:
                for i in range(x2 - x1 + 1):
                    points[(x1 + i, y1 - i)] += 1
            else:
                for i in range(x2 - x1 + 1):
                    points[(x1 + i, y1 + i)] += 1

n = 0
for pt in points:
    if points[pt] >= 2:
        n += 1
print(n)




