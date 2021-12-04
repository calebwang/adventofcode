import sys
import math

global v1, v2, v3

def fn1(v):
    global v1

def fn2(v):
    global v2

def fn3(v):
    global v2

fn_map = {
    "key1": lambda v: fn1(v),
    "key2": lambda v: fn2(v)
}

def genBinary(n):
    return [2 ** i for i in range(n - 1, -1, -1)]

def parseChunks(lines, size, start, every):
    num_chunks = math.floor((len(lines) - start + 1) / every)
    for i in range(num_chunks):
        yield lines[start + i*every : start + size + i*every]


class Board(object):
    def __init__(self, lines):
        self.rows = [
            line.split() for line in lines
        ]

    def __repr__(self):
        return "\n".join([
            " ".join(row)
            for row in self.rows
        ])

    def row(self, rowNum):
        return self.rows[rowNum]

    def col(self, colNum):
        return [
            row[colNum]
            for row in self.rows
        ]





lines = [l.strip() for l in sys.stdin]
for l in lines:
    pass
