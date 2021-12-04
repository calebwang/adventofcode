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

numbers = [int(v, 2) for v in lines]
pos = 0 # up to 12

for p in range(11, -1, -1):
    v = 2 ** p
    one_set = set()
    zero_set = set()

    for n in numbers:
        if (n & v) > 0:
            one_set.add(n)
        else:
            zero_set.add(n)

    if len(one_set) < len(zero_set):
        numbers = one_set
    else:
        numbers = zero_set
    print(numbers)


print(numbers)

