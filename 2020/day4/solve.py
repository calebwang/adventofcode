import sys
import re

e = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
passports = sys.stdin.read().split("\n\n")
count = 0


f = {
    "byr": lambda v: re.match("[0-9]{4}", v) and int(v) >= 1920 and int(v) <= 2002,
    "iyr": lambda v: re.match("[0-9]{4}", v) and int(v) >= 2010 and int(v) <= 2020,
    "eyr": lambda v: re.match("[0-9]{4}", v) and int(v) >= 2020 and int(v) <= 2030,
    "hgt": lambda v: (
        re.match("([0-9]{3}cm|[0-9]{2}in)", v) and
        (("cm" in v and int(v.strip("cm")) >= 150 and int(v.strip("cm")) <= 193) or
        ("in" in v and int(v.strip("in")) >= 59 and int(v.strip("in")) <= 76))
    ),
    "hcl": lambda v: re.match("\#([0-9a-f]){6}$", v),
    "ecl": lambda v: re.match("amb|blu|brn|gry|grn|hzl|oth", v),
    "pid": lambda v: re.match("^[0-9]{9}$", v)
}
for passport in passports:
    s = set()
    m = {}
    lines = passport.split("\n")
    for line in lines:
        parts = line.split()
        for part in parts:
            k, v = part.split(":")
            s.add(part.split(":")[0])
            m[k] = v
    print(m)
    if s.issuperset(e):
        good = True
        for k in e:
            print(k, f[k](m[k]))
            if not f[k](m[k]):
                good = False
                break
        if good:
            print("GOOD")
            count += 1
        print("")

print(count)


