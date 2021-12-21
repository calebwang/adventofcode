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

def cos(amt):
    if amt % 4 == 0:
        return 1
    if amt % 4 == 1:
        return 0
    if amt % 4 == 2:
        return -1
    if amt % 4 == 3:
        return 0

def sin(amt):
    if amt % 4 == 0:
        return 0
    if amt % 4 == 1:
        return 1
    if amt % 4 == 2:
        return 0
    if amt % 4 == 3:
        return -1

def transpose(mat):
    result = []
    for c in range(3):
        result.append([r[c] for r in mat])
    return result

def matmult(mat1, mat2):
    result = []
    for r in range(3):
        result.append([])
        for c in range(3):
            mat2col = [r[c] for r in mat2]
            mat1row = mat1[r]
            val = sum([mat1row[i] * mat2col[i] for i in range(3)])
            result[r].append(val)
    return result

def dot(m, c):
    return tuple(
        sum(
            row[i] * c[i]
            for i in range(3)
        )
        for row in m
    )

def difference(c1, c2):
    return tuple(c1[i] - c2[i] for i in range(3))

def add(c, vector):
    return tuple(c[i] + vector[i] for i in range(3))


memo = dict()
def rotmat(axis, amt):
    if (axis, amt) in memo:
        return memo[(axis, amt)]
    rotation_vals = [[cos(amt), -sin(amt)], [sin(amt), cos(amt)]]
    mat = []
    k = 0
    for i in range(3):
        row = []
        if i != axis:
            row = rotation_vals[k]
            row.insert(axis, 0)
            k += 1
        else:
            row = [1 if j == axis else 0 for j in range(3)]
        mat.append(row)
    if axis == 1:
        mat = transpose(mat)

    memo[(axis, amt)] = mat
    return mat

def rotate(matrix, coord):
    return dot(matrix, coord)

def _rotation_matrices():
    matrices = []

    results = set()
    testcoord = (1, 2, 3)
    for amt1 in range(4):
        for amt2 in range(4):
            for amt3 in range(4):
                arr1 = rotmat(0, amt1)
                arr2 = rotmat(1, amt2)
                arr3 = rotmat(2, amt3)

                rotation_matrix = matmult(matmult(arr1, arr2), arr3)
                r = rotate(rotation_matrix, testcoord)
                if r not in results:
                    matrices.append(rotation_matrix)
                    results.add(r)

    return matrices

rotation_matrices = _rotation_matrices()
print(len(rotation_matrices))


def match(scanner1, scanner2):
    s1_set = set(scanner1)
    for m in rotation_matrices:
        rotated_s2 = [
            rotate(m, c) for c in scanner2
        ]

        difference_counts = defaultdict(int)
        for s1c in scanner1:
            for rs2c in rotated_s2:
                d = difference(s1c, rs2c)
                difference_counts[d] += 1
                if difference_counts[d] >= 12:
                    print(d)
                    return lambda c: add(rotate(m, c), d), d

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
