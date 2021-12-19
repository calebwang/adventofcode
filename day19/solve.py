import sys
import string
import math
import re
from statistics import median, mean
from collections import defaultdict, namedtuple, Counter
import itertools

inp = sys.stdin.read().strip()

scanners_inp = inp.split("\n\n")

scanners = []
for s in scanners_inp:
    pts = s.split("\n")[1:]
    coords = [tuple(map(int, pt.split(","))) for pt in pts]
    scanners.append(coords)

def rot(coord, axis, amt):
    if amt == 0:
        return coord
    if amt < 0:
        amt = amt % 4

    other_axes = list(set(range(3)) - set([axis]))
    nc = list(coord)
    nc[other_axes[0]], nc[other_axes[1]] = -1 * nc[other_axes[1]], nc[other_axes[0]]
    return rot(tuple(nc), axis, amt - 1)

def _rotators():
    def get_rotator(a1, a2, a3):
        return lambda coord: rot(rot(rot(coord, 0, a1), 1, a2), 2, a3)

    result_set = set()
    t = (1, 2, 3)
    rotators = []

    for amt1 in range(4):
        for amt2 in range(4):
            for amt3 in range(4):
                rotator = get_rotator(amt1, amt2, amt3)
                result = rotator(t)
                if result not in result_set:
                    rotators.append(get_rotator(amt1, amt2, amt3))
                    result_set.add(result)

    return rotators

rotators = _rotators()

def orientations(coord):
    return [r(coord) for r in _rotators]

def transpose(coord, vector):
    return (coord[0] + vector[0], coord[1] + vector[1], coord[2] + vector[2])

def difference(coord1, coord2):
    return tuple( coord1[i] - coord2[i] for i in range(3) )

def match(scanner1, scanner2):
    best_rotator = None
    s1_set = set(scanner1)
    for rotator in rotators:
        for s1c in scanner1:
            for start_s2c in scanner2:
                matches = 0
                start_rs2c = rotator(start_s2c)
                d = difference(s1c, start_rs2c)
                f = lambda c: transpose(rotator(c), d)

                for i, s2c in enumerate(scanner2):
                    if len(scanner2) - i < 12 - matches:
                        break
                    if f(s2c) in s1_set:
                        matches += 1
                if matches >= 12:
                    print(d)
                    return f, d
    return None, None


def part1():
    oriented_scanners = [None] * len(scanners)
    scanner_tranposes = [None] * len(scanners)
    queue = [scanners[0]]
    oriented_scanners[0] = scanners[0]
    scanner_tranposes[0] = (0, 0, 0)
    while queue:
        s = queue.pop(0)
        for i, s2 in enumerate(scanners):
            if oriented_scanners[i] is None:
                print("match", i)
                f, d = match(s, s2)
                if f:
                    oriented_scanners[i] = [f(c) for c in s2]
                    scanner_tranposes[i] = d
                    queue.append(oriented_scanners[i])

    print(scanner_tranposes)
    pts = set()
    for s in oriented_scanners:
        for pt in s:
                pts.add(pt)
    print(len(pts))


def part2():
    scanners = [(0, 0, 0), (-2340, 45, 2245), (62, 83, 1085), (85, 1284, -8), (1283, 26, 1043), (-4699, 2391, -178), (-2268, 2335, 1210), (-2405, 1208, 2353), (140, -1224, 2275), (-1097, -1125, 2394), (-1132, 1145, 1047), (-1116, 54, 2257), (-3514, -71, -1303), (-11, -1141, 1124), (-5870, 1170, -9), (-3448, -14, -69), (-13, -2341, 1101), (-2245, -1238, 2243), (8, -1116, 3605), (-2303, 1234, 1201), (-3437, 1132, -84), (1285, -1180, 2362), (-1120, 73, -57), (-4639, -75, -58), (-2277, -1225, 1187), (-2352, -32, -1202), (-4827, 1225, -61), (-1065, -43, -2540), (-1164, 75, -1298), (1299, -1266, 1187), (-1163, -1113, 1084), (-2363, -14, -95), (68, 72, -1227), (-2373, -94, 1157), (-2373, -96, 3436), (1198, -1288, 3594)]

    best = 0
    for s1 in scanners:
        for s2 in scanners:
            dist = sum([ abs(s1[i] - s2[i]) for i in range(3)])
            best = max(dist, best)
    print(best)

part1()
part2()
