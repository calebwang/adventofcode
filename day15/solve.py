import sys
import string
import math
import re
from statistics import median, mean
from collections import defaultdict, namedtuple, Counter

inp = sys.stdin.read().strip()
lines = inp.split("\n")

board = [
    [int(c) for c in line]
    for line in lines
]
boardmap = {
    (r, c): int(score)
    for r, line in enumerate(lines)
    for c, score in enumerate(line)
}

memo = defaultdict(int)
def dfs(board, pos, visited):
    if pos in memo:
        return memo[pos]

    if pos in visited:
        return float("inf")

    r, c = pos
    if r < 0 or c < 0 or r >= len(board) or c >= len(board[0]):
        return float("inf")

    posrisk = board[r][c]
    if r == len(board) - 1 and c == len(board[0]) - 1:
        print(visited)
        return posrisk

    nvisited = visited.copy().union(set([pos]))
    minrisk = min([
        dfs(board, (r+1, c), nvisited),
        dfs(board, (r, c+1), nvisited),
        dfs(board, (r-1, c), nvisited),
        dfs(board, (r, c-1), nvisited),
    ])

    memo[pos] = minrisk + posrisk
    return minrisk + posrisk

def neighbors(pos):
    r, c = pos
    return [
        (r + 1, c),
        (r, c + 1),
        (r - 1, c),
        (r, c - 1),
    ]

def board_getter(board, mult):
    def contains(pos):
        r, c = pos
        return r >= 0 and c >= 0 and r < len(board) * mult and c < len(board[0]) * mult

    def get(pos):
        if not contains(pos):
            raise Error("fail")
        r, c = pos
        r_adder = math.floor(r / len(board))
        c_adder = math.floor(c / len(board[0]))
        adder = r_adder + c_adder
        modval = (board[r % len(board)][c % len(board[0])] + adder) % 9
        if modval == 0:
            return 9
        return modval


    return get, contains


def djikstras(board, mult):
    get, contains = board_getter(board, 5)
    queue = {(0, 0): 0}
    visited = set()
    while queue:
        pos = min(queue, key=lambda k: queue[k])
        score = queue[pos]
        del queue[pos]
        visited.add(pos)

        if pos == (len(board) * mult - 1, len(board[0]) * mult - 1):
            return score

        for n in neighbors(pos):
            if contains(n) and n not in visited:
                nextscore = score + get(n)
                if n not in queue or nextscore < queue[n]:
                    queue[n] = nextscore



# print(dfs(board, (0, 0), set()) - board[0][0])
print(djikstras(board, 5))
