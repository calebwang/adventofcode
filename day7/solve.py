import sys
import math
import re
from dataclasses import dataclass
from collections import defaultdict, namedtuple

crabs = list(map(int, sys.stdin.read().strip().split(",")))
print(crabs)
def f(n):
    return n * (n + 1) / 2

pos = 0
best = float('inf')
for test in range(max(crabs) + 1):
    s = 0
    for crab in crabs:
        s += f(abs(crab - test))
    if s < best:
        best = s
print(best)


sumup = {}

