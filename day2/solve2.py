import sys


lines = (l.strip() for l in sys.stdin)
x, a, d = 0, 0, 0

def move(v):
    global x, a, d
    x += v
    d += (a * v)

def incr_a(v):
    global a
    a += v

fn_map = {
    "forward": lambda v: move(int(v)),
    "down": lambda v: incr_a(int(v)),
    "up": lambda v: incr_a(-int(v)),
}
for l in lines:
    command, v = l.split(" ")
    fn_map[command](v)

print("{}, {}".format(x, d))
