import sys


lines = (l.strip() for l in sys.stdin)
x, d = 0, 0

def incr_x(v):
    global x
    x += v

def incr_d(v):
    global d
    d += v

fn_map = {
    "forward": lambda v: incr_x(int(v)),
    "down": lambda v: incr_d(int(v)),
    "up": lambda v: incr_d(-int(v)),
}
for l in lines:
    command, v = l.split(" ")
    fn_map[command](v)

print("{}, {}".format(x, d))
