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


def big(node):
    return node.lower() != node

edges = defaultdict(list)
for line in lines:
    match = re.match("(.*)-(.*)", line)
    node1, node2 = match.groups()
    edges[node1].append(node2)
    edges[node2].append(node1)


print(edges)
def dfs(node, visited, visitedSmall, path):
    if node == "end":
        return 1

    if node in visited:
        if node == "start":
            return 0
        elif visitedSmall:
            return 0
        elif not visitedSmall:
            visitedSmall = True

    if not big(node):
        visited.add(node)

    s = 0
    for edgenode in edges[node]:
        s += dfs(edgenode, visited.copy(), visitedSmall, path[:] + [edgenode])
    return s

print(dfs("start", set(), True, ["start"]))
print(dfs("start", set(), False, ["start"]))
