import sys


lines = (l.strip() for l in sys.stdin)
global v1, v2, v3

def fn1(v):
    global v1

def fn2(v):
    global v2

def fn3(v):
    global v2

fn_map = {
    "key1": lambda v: fn1(v),
    "key2": lambda v: fn2(v),
    "key3": lambda v: fn3(v)
}

gamma = 0
epsilon = 0

numbers = [int(v, 2) for v in lines]
pos = 0 # up to 12

for p in range(11, -1, -1):
    v = 2 ** p
    one_count = 0
    zero_count = 0
    print(v)
    for n in numbers:
        if (n & v) > 0:
            one_count += 1
        else:
            zero_count += 1

    if one_count > zero_count:
        gamma += v
    else:
        epsilon += v


print(gamma * epsilon)

