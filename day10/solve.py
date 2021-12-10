import sys
import string
import math
import re
from statistics import median
from dataclasses import dataclass
from collections import defaultdict, namedtuple

inp = sys.stdin.read().strip().split("\n")
print("\n".join(inp))
print(len(inp))

score = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}


score2 = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

complement = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

s = 0
s2 = 0
validlines = []
linescores = []
for line in inp:
    stack = []
    ok = True
    linescore = 0
    for char in line:
        if char == "(" or char == "[" or char is "{" or char is "<":
            stack.append(char)
        else:
            openchar = stack.pop()
            if char != complement[openchar]:
                s += score[char]
                ok = False

            """
            if openchar == "(":
                if char != ")":
                    s += score[char]
                    ok = False
            if openchar == "[":
                if char != "]":
                    s += score[char]
                    ok = False
            if openchar == "{":
                if char != "}":
                    s += score[char]
                    ok = False
            if openchar == "<":
                if char != ">":
                    s += score[char]
                    ok = False
            """
    if ok:
        while stack:
            nchar = stack.pop()
            cc = complement[nchar]
            linescore = linescore * 5 + score2[cc]
        linescores.append(linescore)


print(s)
print(linescores)
print(len(linescores))
print(sorted(linescores)[24])
print(median(linescores))




