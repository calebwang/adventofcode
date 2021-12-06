import sys

groups = sys.stdin.read().split("\n\n")

c = 0
for group in groups:
    gset = set()
    mems = group.split("\n")
    for mem in mems:
        for ans in mem:
            if all([ans in mem for mem in mems]):
                gset.add(ans)
    c += len(gset)
print(c)


