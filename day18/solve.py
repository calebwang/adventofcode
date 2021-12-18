import sys
import string
import math
import re
from statistics import median, mean
from collections import defaultdict, namedtuple, Counter
import json

inp = sys.stdin.read().strip()
lines = inp.split("\n")




sns = []
for line in lines:
    sns.append(json.loads(line))



def flatten(sn, depth=0):
    result = []
    result.append("*")
    for i, el in enumerate(sn):
        if type(el) == int:
            result.append((el, depth))
        else:
            result.extend(flatten(el, depth+1))
    return result


def hydrate(flat_sn):
    return _hydrate(flat_sn)[0]

def _hydrate(flat_sn):
    el = flat_sn[0]
    if el == "*":
        left, llen = _hydrate(flat_sn[1:])
        right, rlen = _hydrate(flat_sn[llen + 1:])
        return [left, right], llen + rlen + 1
    else:
        return el[0], 1


def add(fsn1, fsn2):
    result = ["*"] + [
        (el[0], el[1] + 1) if type(el) == tuple else "*"
        for el in fsn1
    ] + [
        (el[0], el[1] + 1) if type(el) == tuple else "*"
        for el in fsn2
    ]
    go = True
    while go:
        result, go = process(result)
    return result

def explode(fsn):
    exploded_idx = None
    exploded_depth = None
    lval, rval = None, None
    for i, el in enumerate(fsn):
        if el == "*":
            continue
        val, depth = el
        if depth >= 4:
            exploded_idx = i
            exploded_depth = depth
            lval = val
            rval = fsn[i + 1][0]
            break

    if not exploded_idx:
        return fsn, False

    right = fsn[exploded_idx + 2:]
    for i, el in enumerate(right):
        if el != "*":
            val, depth = el
            right[i] = (val + rval, depth)
            break

    left = fsn[:exploded_idx - 1]
    for i in range(len(left) - 1, -1, -1):
        el = left[i]
        if el != "*":
            val, depth = el
            left[i] = (val + lval, depth)
            break

    fsn = left + [(0, exploded_depth - 1)] + right
    return fsn, True

def split(fsn):
    for i, el in enumerate(fsn):
        if el == "*":
            continue
        val, depth = el
        if val >= 10:
            next_result = fsn[:i] + \
                ["*", (math.floor(val / 2), depth + 1), (math.ceil(val / 2), depth + 1)] + \
                fsn[i + 1:]
            return next_result, True
    return fsn, False

def process(sn):
    result, exploded = explode(sn)
    if exploded:
        return result, True
    result, was_split = split(sn)
    if was_split:
        return result, True
    return sn, False

def mag(sn):
    if type(sn) == int:
        return sn
    return 3 * mag(sn[0]) + 2 * mag(sn[1])

flat_sns = [flatten(sn) for sn in sns]

def part1():
    result = flat_sns[0]
    for sn in flat_sns[1:]:
        result = add(result, sn)
    print(hydrate(result))
    print(mag(hydrate(result)))

def part2():
    best = 0
    for i, fsn1 in enumerate(flat_sns):
        for j, fsn2 in enumerate(flat_sns):
            if i != j:
                best = max(
                    mag(hydrate(add(fsn1, fsn2))),
                    mag(hydrate(add(fsn2, fsn1))),
                    best
                )
    print(best)


part1()
part2()


