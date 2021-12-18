import sys
import string
import math
import re
from statistics import median, mean
from collections import defaultdict, namedtuple, Counter
import json

inp = sys.stdin.read().strip()
lines = inp.split("\n")

class Node:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

def nodify(sn):
    if type(sn) == int:
        return Node(sn)
    return [nodify(e) for e in sn]

sns = []
for line in lines:
    sns.append(nodify(json.loads(line)))

def add(sn1, sn2):
    result = [sn1, sn2]
    go = True
    while go:
        go = process(result)
    return result

def process(sn):
    if explode(sn):
        return True
    _, has_split = split(sn)
    if has_split:
        return True
    return False

def explode(sn):
    inorder = list()
    exploded_info, _ = _explode(sn, inorder)
    if not exploded_info:
        return False

    idx, lval, rval = exploded_info
    if idx - 1 >= 0:
        inorder[idx - 1].value += lval
    if idx + 1 < len(inorder):
        inorder[idx + 1].value += rval

    return True

def _explode(sn, inorder, depth=0, explode_info=None):
    already_exploded = explode_info is not None
    if not isinstance(sn, Node):
        if not already_exploded and depth >= 4:
            # about to add 0 at the next index
            return (len(inorder), sn[0].value, sn[1].value), True

        just_exploded = False
        for i in [0, 1]:
            explode_info, just_exploded = _explode(sn[i], inorder, depth + 1, explode_info)
            if just_exploded:
                node = Node(0)
                sn[i] = node
                inorder.append(node)
                just_exploded = False

        return explode_info, False
    else:
        inorder.append(sn)
        return explode_info, False

def split(sn, has_split=False):
    if isinstance(sn, Node):
        if sn.value >= 10 and not has_split:
            return [Node(math.floor(sn.value / 2)), Node(math.ceil(sn.value / 2))], True
        return None, has_split
    else:
        for i in [0, 1]:
            val, has_split = split(sn[i], has_split)
            if val:
                sn[i] = val

        return None, has_split

def mag(sn):
    if isinstance(sn, Node):
        return sn.value
    return 3 * mag(sn[0]) + 2 * mag(sn[1])

def part1():
    result = sns[0]
    for sn in sns[1:]:
        result = add(result, sn)
    print(result)
    print(mag(result))

part1()


