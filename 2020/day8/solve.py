import sys

lines = sys.stdin.read().split("\n")



def tryrun(lns):
    pos = 0
    acc = 0
    def incr(i):
        nonlocal acc
        nonlocal pos
        acc += i
        pos += 1

    def noop():
        nonlocal pos
        pos += 1

    def jmp(i):
        nonlocal pos
        pos += i

    funmap = {
        "acc": lambda v: incr(v),
        "nop": lambda v: noop(),
        "jmp": lambda v: jmp(v),
    }

    seen = set()
    while True:
        if pos in seen:
            break
        if pos >= len(lns):
            print(acc)
            break
        seen.add(pos)
        instr, arg = lns[pos].split()
        funmap[instr](int(arg))


for i, line in enumerate(lines):
    if line.split()[0] == "jmp":
        cpy = lines[:]
        cpy[i] = line.replace("jmp", "nop")
        tryrun(cpy)
    elif line.split()[0] == "nop":
        cpy = lines[:]
        cpy[i] = line.replace("nop", "jmp")
        tryrun(cpy)
