import sys

lines = (l.strip() for l in sys.stdin)
vals = list(int(l) for l in lines)
counter = 0
for i, val in enumerate(vals):
    if i > 0 and val > vals[i - 1]:
        counter += 1

print(counter)
