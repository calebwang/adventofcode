import sys
import math
import re
from collections import defaultdict

fish = list(map(int ,sys.stdin.read().strip().split(",")))

counts = defaultdict(int)
for fish in fish:
    counts[fish] += 1

for i in range(256):
    new_counts = defaultdict(int)
    new_counts[6] = counts[0] + counts[7]
    new_counts[5] = counts[6]
    new_counts[4] = counts[5]
    new_counts[3] = counts[4]
    new_counts[2] = counts[3]
    new_counts[1] = counts[2]
    new_counts[0] = counts[1]
    new_counts[8] = counts[0]
    new_counts[7] = counts[8]
    counts = new_counts

print(sum(counts.values()))


"""
print(fish)
for i in range(256):
    new_fish = []
    for i in range(len(fish)):
        if fish[i] == 0:
            fish[i] = 6
            new_fish.append(8)
        else:
            fish[i] -= 1
    fish.extend(new_fish)
"""

print(len(fish))

