import sys
import re

lines = [line.strip() for line in sys.stdin]

bag_map = {}
inv_bm = {}
for line in lines:
    m = re.match("(.*) bags contain (.*).", line)
    color, innerm = m.groups()

    if innerm == "no other bags":
        color = line.split(" bags")[0]
        bag_map[color] = set()
        continue

    inners = innerm.split(", ")
    innercolors = set()
    inner_colormap = {}
    for inner in inners:
        m1 = re.match(r"([0-9]+) (.*) bag(s?)", inner)
        inc = m1.group(2)
        innercolors.add(m1.group(2))
        inner_colormap[inc] = int(m1.group(1))
        if inc not in inv_bm:
            inv_bm[inc] = set()
        inv_bm[inc].add(color)
    bag_map[color] = inner_colormap


visited = set()
def dfs(color):
    visited.add(color)
    if color not in inv_bm:
        return
    print(color, inv_bm[color])
    for c in inv_bm[color]:
        dfs(c)

# dfs("shiny gold")
# print(len(visited) - 1)

def idfs(color):
    count = 1
    if color not in bag_map:
        return 1
    for c in bag_map[color]:
        print(bag_map[color])
        icount = bag_map[color][c]
        count += icount * idfs(c)
    return count

print(idfs("shiny gold"))





