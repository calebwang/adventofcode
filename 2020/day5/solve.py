import sys
import math

lines = [line.strip() for line in sys.stdin]
best = 0
ids = set()
for line in lines:
    lrow = 0
    hrow = 127
    lcol = 0
    hcol = 7

    for ch in line:
        if ch == "F":
            hrow = math.floor((hrow + lrow)/ 2)
        elif ch == "B":
            lrow = math.ceil((hrow + lrow) / 2)
        elif ch == "R":
            lcol = math.ceil((hcol + lcol) / 2)
        elif ch == "L":
            hcol = math.floor((hcol + lcol) / 2)

    print(lrow, hrow, lcol, hcol)
    assert(lrow == hrow)
    assert(lcol == hcol)
    ids.add(lrow * 8 + lcol)
    if lrow * 8 + lcol > best:
        best = lrow * 8 + lcol


for id in ids:
    if (id + 1) not in ids and (id + 2) in ids:
        print(id + 1)



