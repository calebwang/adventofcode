import sys

lines = (l.strip() for l in sys.stdin)
vals = list(int(l) for l in lines)
window_sums = [
    sum(vals[i:i+3])
    for i in range(len(vals) - 2)
]

print(window_sums)
print(len(window_sums))

counter = 0
for i, val in enumerate(window_sums):
    if i > 0 and val > window_sums[i - 1]:
        counter += 1

print(counter)
