import sys
import string
import math
import re
from statistics import median, mean
from collections import defaultdict, namedtuple, Counter

inp = sys.stdin.read().strip()
lines = inp.split("\n")




print(inp)

s = 0
pkt = int(lines[0], 16)
raw_bp = bin(pkt)[2:]
bp = "0" * (len(raw_bp) % 4) + raw_bp

print(bp)

def parse_pkt(binpkt):
    global s
    print(binpkt)
    version = int(binpkt[:3], 2)
    s += version
    ptype = int(binpkt[3:6], 2)
    print("v, ptype", version, ptype)
    if ptype == 4:
        pos = 6
        val = ""
        while int(binpkt[pos], 2) == 1:
            val += binpkt[pos + 1: pos + 5]
            pos += 5
        val += binpkt[pos + 1: pos + 5]
        val = int(val, 2)
        print("val", val)
        return val, pos + 5
    else:
        tlenid = int(binpkt[6], 2)
        subpkts = []
        pktlen = 0
        print("tlenid: " + str(tlenid))
        if tlenid == 0:
            total_subpkts_len = int(binpkt[7:7+15], 2)
            readlen = 0
            while readlen < total_subpkts_len:
                subpkt, subpkt_len = parse_pkt(binpkt[22 + readlen: 22 + total_subpkts_len])
                readlen += subpkt_len
                subpkts.append(subpkt)
            pktlen = 22 + readlen
        elif tlenid == 1:
            num_subpkts = int(binpkt[7:7+11], 2)
            read_subpkts = 0
            readlen = 0
            print("nsubpkts", num_subpkts)
            while read_subpkts < num_subpkts:
                subpkt, subpkt_len = parse_pkt(binpkt[18 + readlen:])
                readlen += subpkt_len
                read_subpkts += 1
                subpkts.append(subpkt)
            pktlen = readlen + 18

        if ptype == 0:
            return sum(subpkts), pktlen
        if ptype == 1:
            product = 1
            for v in subpkts:
                product *= v
            return product, pktlen
        if ptype == 2:
            return min(subpkts), pktlen
        if ptype == 3:
            return max(subpkts), pktlen
        if ptype == 5:
            v = 1 if subpkts[0] > subpkts[1] else 0
            return v, pktlen
        if ptype == 6:
            v = 1 if subpkts[0] < subpkts[1] else 0
            return v, pktlen
        if ptype == 7:
            v = 1 if subpkts[0] == subpkts[1] else 0
            return v, pktlen
    return

print(parse_pkt(bp))
print(s)
