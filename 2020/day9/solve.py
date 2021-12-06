import sys

nums = [int(l.strip()) for l in sys.stdin]

window = set()
for i, n in enumerate(nums):
    window.add(n)
    if i >= 25:
        ok = False
        for w in window:
            if (n - w) in window:
                ok = True
        if not ok:
            print(n, window)
            break
        window.remove(nums[i - 25])


magic = 133015568
for i, n in enumerate(nums):
    s = set()
    for k in nums[i:]:
        s.add(k)
        if len(s) > 1 and sum(s) == magic:
            print(min(s) + max(s))
        if sum(s) > magic:
            break
