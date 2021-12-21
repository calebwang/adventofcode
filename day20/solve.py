import sys
import string
import math
import re
from statistics import median, mean
from collections import defaultdict, namedtuple, Counter

inp = sys.stdin.read().strip()
lines = inp.split("\n")

enhancement, _img = inp.split("\n\n")


img = _img.split("\n")

def get_pixel(image, r, c, d="."):
    if r >= 0 and r < len(image) and c >= 0 and c < len(image[0]):
        return image[r][c]
    return d

def area(r, c):
    result = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            result.append( (r + dr, c + dc) )
    return result

def area_lookup(image, r, c, d="."):
    pixels = [
        get_pixel(image, _r, _c, d) for (_r, _c) in
        area(r, c)
    ]

    pxs = "".join(pixels).replace("#", "1").replace(".", "0")
    idx = int(pxs, 2)

    return idx

def process(image, d="."):
    k = 1
    result = []
    for r in range(-k, len(image) + k):
        row = []
        for c in range(-k, len(image[0]) + k):
            idx = area_lookup(image, r, c, d)
            px_result = enhancement[idx]
            row.append(px_result)
        result.append(row)
    return result

def pprint(image):
    for row in image:
        print("".join(row))

def count(image):
    s = 0
    for row in image:
        for e in row:
            if e == "#":
                s += 1
    return s


pprint(process(img))
print("================")
result = process(process(img), "#")

print(count(result))

curr = img
for i in range(50):
    curr = process(curr, "#" if i % 2 == 1 else ".")
print(count(curr))
