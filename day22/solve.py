import sys
import string
import math
import re
from statistics import median, mean
from collections import defaultdict, namedtuple, Counter

inp = sys.stdin.read().strip()
lines = inp.split("\n")

instructions = []
for line in lines:
    inst, _coords = line.split(" ")
    xs, ys, zs = _coords.split(",")
    linecoords = []
    for i, p in enumerate([xs, ys, zs]):
        p = p[2:]
        lower, upper = p.split("..")
        linecoords.append((int(lower), int(upper)))
    instructions.append((inst, tuple(linecoords)))

def inbound(coord):
    x, y, z = coord
    return x >= -50 and x <= 50 and y >= -50 and y <= 50 and z >= -50 and z <= 50


def part1():
    onlights = set()
    for i, (inst, bounds) in enumerate(instructions):
        if int(upper) < -50 or int(lower) > 50:
            ok = False
        xs, ys, zs = bounds
        ok = True
        for coords in [xs, ys, zs]:
            if max(coords) < -50 or min(coords) > 50:
                ok = False
        if not ok:
            continue
        for x in range(xs[0], xs[1] + 1):
            for y in range(ys[0], ys[1] + 1):
                for z in range(zs[0], zs[1] + 1):
                    c = (x, y, z)
                    if inbound((x, y, z)):
                        if inst == 'on':
                            onlights.add(c)
                        if inst == 'off' and c in onlights:
                            onlights.remove(c)
    print(len(onlights))

class Node(object):
    def __init__(self, minval, maxval):
        self.value = minval
        self.left = None
        if maxval is not None:
            self.right = Node(maxval, None)

class RangeTree(object):
    def __init__(self, root):
        self.root = root

class Coord(object):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y and self.z > other.z

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y and self.z < other.z

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y and self.z >= other.z

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y and self.z <= other.z

    def __getitem__(self, axis):
        if axis == 0:
            return self.x
        elif axis == 1:
            return self.y
        elif axis == 2:
            return self.z

    def __setitem__(self, axis, value):
        if axis == 0:
            self.x = value
        elif axis == 1:
            self.y = value
        elif axis == 2:
            self.z = value

    def __repr__(self):
        return "Coord" + str((self.x, self.y, self.z))

    def __hash__(self):
        return hash(str(self))


class Region(object):
    def __init__(self, start, end):
        # Assume start < end
        assert(start <= end)
        self.start = start
        self.end = end

    def __repr__(self):
        return "Region" + str((self.start, self.end))

    @staticmethod
    def split(region, axis, splitline):
        if splitline <= region.start[axis]:
            return [None, region]
        if splitline > region.end[axis]:
            return [region, None]
        # splitline will be included in the new region
        return [
            Region(region.start, Coord(*tuple(splitline - 1 if i == axis else region.end[i] for i in range(3)))),
            Region(Coord(*tuple(splitline if i == axis else region.start[i] for i in range(3))), region.end)
        ]

    def overlaps(self, other):
        return self.start <= other.end and self.end >= other.start

    def size(self):
        product = 1
        for axis in range(3):
            product = product * (self.end[axis] - self.start[axis] + 1)
        return product

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash(str(self))

    def contains(self, other):
        return self.start < other.start and self.end > other.end

    @staticmethod
    def partition(region1, region2):
        if not region1.overlaps(region2):
            return [None, [region1], [region2]]

        overlapping_region = Region(
            Coord(*(max(region1.start[i], region2.start[i]) for i in range(3))),
            Coord(*(min(region1.end[i], region2.end[i]) for i in range(3))),
        )
        regions = []
        for region in [region1, region2]:
            regions_from_current_region = []
            working_region = region
            # create up to 7 regions per input region; could be up to 27 regions without optimization
            for axis in range(3):
                # optimization: r1 and r3 do not need to be split further
                r1, _r2 = Region.split(working_region, axis, overlapping_region.start[axis])
                r2, r3 = Region.split(_r2, axis, overlapping_region.end[axis] + 1)

                for r in [r1, r3]:
                    if r is not None:
                        regions_from_current_region.append(r)
                working_region = r2

            regions.append(regions_from_current_region)
        return (overlapping_region, regions[0], regions[1])


r = Region(Coord(1, 1, 1), Coord(10, 10, 10))
print(r.size())
r1 = Region(Coord(5, 5, 5), Coord(7, 7, 7))
print(r.overlaps(r1))


def process_instruction(lit_regions, new_bit, new_region):
    result = []
    for region in lit_regions:
        if region.contains(new_region) and new_bit:
            # Turning on a subset of a lit region
            # We can just return the input
            return lit_regions

        if new_region.contains(region):
            # Region contained in new region, let new region override
            continue

        # Identify overlaps with the new region
        _, old_subregions, _ = Region.partition(region, new_region)

        # Non-overlapping areas from the old region are safe to add to the result.
        for r in old_subregions:
            result.append(r)

    # Add the new region if the instruction is 'on'
    if new_bit:
        result.append(new_region)
    return result

def part2():
    def make_region(bounds):
        pts = tuple(zip(*bounds))
        return Region(Coord(*pts[0]), Coord(*pts[1]))

    def parity(inst):
        return 1 if inst == "on" else 0

    lit_regions = []
    i = 0
    for _bit, _region in instructions:
        bit, region = parity(_bit), make_region(_region)
        if bit:
            lit_regions.append(region)
            break
        i += 1

    for inst, bounds in instructions[i + 1:]:
        new_region = make_region(bounds)
        new_bit = parity(inst)

        lit_regions = process_instruction(lit_regions, new_bit, new_region)

    s = 0
    for r in lit_regions:
        s += r.size()
    print(s)
    return lit_regions

part2()



