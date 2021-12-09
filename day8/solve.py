import sys
import math
import re
import string
from dataclasses import dataclass
from collections import defaultdict, namedtuple


def letter_to_num(l):
    return string.ascii_lowercase.index(l)


def solve(inputs):
    s = set(inputs)
    ans = {}
    nums = [None] * 10
    wires = { k: "" for k in string.ascii_lowercase[:7] }
    for dig in inputs:
        l = len(dig)
        if l == 2:
            ans[dig] = 1
            nums[1] = dig
        if l == 3:
            ans[dig] = 7
            nums[7] = dig
        if l == 4:
            ans[dig] = 4
            nums[4] = dig
        if l == 7:
            ans[dig] = 8
            nums[8] = dig

    awire = set(nums[7]).difference(set(nums[1]))
    wires["a"] = list(awire)[0]

    cf_candidates = set(nums[1])
    bd_candidates = set(nums[4]).difference(set(nums[1]))
    eg_candidates = set("abcdefg").difference(set(nums[4])).difference(set(nums[7]))

    two_three_five = [
        dig for dig in inputs
        if len(dig) == 5
    ]
    zero_six_nine_candidates = [
        dig for dig in inputs
        if len(dig) == 6
    ]

    three = [ dig for dig in two_three_five if len(set(dig).intersection(cf_candidates)) == 2 ][0]
    ans[three] = 3
    nums[3] = three

    two = [ dig for dig in two_three_five if len(set(dig).intersection(eg_candidates)) == 2][0]
    ans[two] = 2
    nums[2] = two

    five = [ dig for dig in two_three_five if dig is not two and dig is not three ][0]
    ans[five] = 5
    nums[5] = five


    for dig in zero_six_nine_candidates:
        if len(set(dig).intersection(cf_candidates.union(eg_candidates))) == 4:
            ans[dig] = 0
            nums[0] = dig
        elif len(set(dig).intersection(cf_candidates)) == 2:
            ans[dig] = 9
        else:
            ans[dig] = 6

    print(ans)
    def lookup(key):
        for k, v in ans.items():
            if sorted(k) == sorted(key):
                return str(v)
    return lookup

lines = [ln for ln in sys.stdin.read().strip().split("\n")]
s = 0
for line in lines:
    inp, out = line.split(" | ")
    inputs = inp.split()
    outs = out.split()
    anskey = solve(inputs)
    print(out)
    ans = int("".join([anskey(k) for k in outs]))
    print(ans)
    s += ans
print(s)

