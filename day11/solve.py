import sys
import string
import math
import re
from statistics import median, mean
from collections import defaultdict, namedtuple

inp = sys.stdin.read().strip().split("\n")

board = [
    [ int(c) for c in line ]
    for line in inp
]

print(board)

def copy(board):
    return [row[:] for row in board]

def neighbors(r, c):
    result = []
    result.append((r, c+1))
    result.append((r, c-1))
    result.append((r+1, c))
    result.append((r+1, c+1))
    result.append((r+1, c-1))
    result.append((r-1, c))
    result.append((r-1, c+1))
    result.append((r-1, c-1))
    return [
        (r, c) for (r, c) in result
        if r >= 0 and c >= 0 and r < 10 and c < 10
    ]


s = 0
def step(board):
    global s
    board = copy(board)
    for r, row in enumerate(board):
        for c, e in enumerate(row):
            if e <= 9:
                board[r][c] += 1
    go = True
    flashed = set()

    while go:
        go = False
        nextboard = copy(board)
        for r, row in enumerate(board):
            for c, e in enumerate(row):
                if e > 9 and (r, c) not in flashed:
                    flashed.add((r, c))
                    s += 1
                    go = True
                    for (r1, c1) in neighbors(r, c):
                        if nextboard[r1][c1] < 10:
                            nextboard[r1][c1] += 1
        board = nextboard
    for (r, c) in flashed:
        board[r][c] = 0
    return board

def stepped(board, n):
    nextboard = [row[:] for row in board]
    for i in range(n):
        nextboard = step(nextboard)
    return nextboard

stepped(board, 100)
print(s)

i = 0
while True:
    ok = True
    testboard = stepped(board, i)
    for row in testboard:
        for e in row:
            if e != 0:
                ok = False
    if ok:
        print(i)
        break
    i += 1
