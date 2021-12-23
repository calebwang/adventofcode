import sys
import string
import math
import re
from statistics import median, mean
from collections import defaultdict, namedtuple, Counter
import heapq

inp = sys.stdin.read().strip()
lines = inp.split("\n")

print(inp)
print(len(lines))

def append_row(rooms, line):
    i = 0
    for c in line:
        if c != " " and c != "#":
            rooms[i].append(c)
            i += 1


def parse1():
    hallway_spots = [None] * 11
    rooms = [[] for i in range(4)]

    append_row(rooms, lines[2])
    append_row(rooms, lines[3])
    _board = (hallway_spots, rooms)
    return _board

def parse2():
    hallway_spots = [None] * 11
    rooms = [[] for i in range(4)]

    append_row(rooms, lines[2])
    append_row(rooms, "DCBA")
    append_row(rooms, "DBAC")
    append_row(rooms, lines[3])

    _board = (hallway_spots, rooms)
    return _board


cost = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

roomforc = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3
}

cforroom = { v: k for k, v in roomforc.items() }

def room_hallway_idx(roomidx):
    return (roomidx + 1) * 2

def isroom(pos):
    return pos[0] != "hallway"

def roomidx(pos):
    assert(isroom(pos))
    return int(pos[0][-1]) - 1

def get(board, pos):
    hallway, rooms = board
    area, idx = pos
    if isroom(pos):
        return rooms[roomidx(pos)][idx]
    return hallway[idx]

def setc(board, pos, c):
    hallway, rooms = board
    area, idx = pos
    if isroom(pos):
        rooms[roomidx(pos)][idx] = c
    else:
        hallway[idx] = c

def move(board, start_pos, end_pos):
    assert(is_move_valid(board, start_pos, end_pos))
    start_area, start_idx = start_pos
    end_area, end_idx = end_pos
    hallway, rooms = board

    hallway_start_idx = room_hallway_idx(roomidx(start_pos)) if isroom(start_pos) else start_idx
    hallway_end_idx = room_hallway_idx(roomidx(end_pos)) if isroom(end_pos) else end_idx
    hallway_dist = abs(hallway_end_idx - hallway_start_idx)

    start_room_dist = start_idx + 1 if isroom(start_pos) else 0
    end_room_dist = end_idx + 1 if isroom(end_pos) else 0

    dist = hallway_dist + start_room_dist + end_room_dist

    c = get(board, start_pos)
    setc(board, start_pos, None)
    setc(board, end_pos, c)
    return cost[c] * dist

def is_move_valid(board, start_pos, end_pos):
    hallway, rooms = board
    start_area, start_idx = start_pos
    end_area, end_idx = end_pos

    if start_pos == end_pos:
        return False
    c = get(board, start_pos)
    if not c:
        return False
    if get(board, end_pos):
        return False

    if isroom(start_pos):
        # check for blockage
        rn = roomidx(start_pos)
        for i, el in enumerate(rooms[rn]):
            if el != None and i < start_idx:
                return False
        if isroom(end_pos) and roomidx(start_pos) == roomidx(end_pos):
            # no point moving within a room
            return False

        if roomforc[c] == roomidx(start_pos) and all([el == None or el == c for el in rooms[rn]]):
            # we're in the right room, don't move
            return False

    if not isroom(start_pos):
        if not isroom(end_pos):
            # If in hallway, must move to room.
            # Check for end validity is later
            return False

    hallway_start_idx = room_hallway_idx(roomidx(start_pos)) if isroom(start_pos) else start_idx
    hallway_end_idx = room_hallway_idx(roomidx(end_pos)) if isroom(end_pos) else end_idx

    # Check hallway blockages
    for i in range(min(hallway_start_idx, hallway_end_idx), max(hallway_start_idx, hallway_end_idx) + 1):
        if not isroom(start_pos) and i == start_idx:
            continue
        if hallway[i] is not None:
            return False

    if isroom(end_pos):
        rn = roomidx(end_pos)
        room = rooms[rn]
        # Check for blockage
        expected_c = cforroom[rn]
        for i, el in enumerate(room):
            # Move is blocked
            if el != None and i < end_idx:
                return False

            # Must move to the end, if possible
            if el == None and i > end_idx:
                return False

            # Cannot contain any other elements
            if el != expected_c and el != None:
                return False

        # Should be the correct room
        if roomforc[c] != rn:
            return False
    else:
        # Banned hallway positions
        if end_idx > 1 and end_idx < 9 and end_idx % 2 == 0:
            return False

    return True


def _all_positions():
    for i in range(11):
        yield ("hallway", i)

    for i in range(4):
        # num rows goes here
        for j in range(4):
            yield ("room" + str(i + 1), j)

def copy(board):
    hallway, rooms = board
    return (hallway[:], [rm[:] for rm in rooms])

def win(board):
    _, rooms = board
    for i, rm in enumerate(rooms):
        for el in rm:
            if el != cforroom[i]:
                return False
    return True

def bhash(board):
    hallway, rooms = board
    return tuple(hallway) + tuple(tuple(rm) for rm in rooms)


all_positions = list(_all_positions())
print(all_positions)
def generate_moves(board, score):
    start_ps = []
    for p in all_positions:
        if get(board, p):
            start_ps.append(p)

    next_boards = []
    for sp in start_ps:
        for ep in all_positions:
            if is_move_valid(board, sp, ep):
                nb = copy(board)
                s = move(nb, sp, ep)
                next_boards.append((nb, score + s))
    return next_boards

def pprint(board):
    hallway, rooms = board
    print("#" * 13)
    print("#" + "".join(["." if el is None else el for el in hallway]) + "#")
    print("###" + "#".join(["." if rooms[i][0] is None else rooms[i][0] for i in range(4)]) + "#")
    print("  #" + "#".join(["." if rooms[i][1] is None else rooms[i][1] for i in range(4)]) + "#")
    if len(rooms[0]) > 2:
        print("  #" + "#".join(["." if rooms[i][2] is None else rooms[i][2] for i in range(4)]) + "#")
        print("  #" + "#".join(["." if rooms[i][3] is None else rooms[i][3] for i in range(4)]) + "#")
    print("#" * 13)

def djikstras(board):
    checks = 0
    score = 0
    bests = {bhash(board): 0}
    queue = [(0, bhash(board), board)]
    solved = False
    _id = 0
    while not solved:
        _score, _, _board = heapq.heappop(queue)

        checks += 1
        if checks % 10000 == 0:
            print(_score, checks)

        if win(_board):
            return _score
        for next_board, next_score in generate_moves(_board, _score):
            _id += 1
            _hash = bhash(next_board)
            if _hash in bests and bests[_hash] <= next_score:
                continue
            bests[_hash] = next_score
            heapq.heappush(queue, (next_score, _id, next_board))

def part1():
    board = parse1()
    s = 0
    pprint(board)

    print(djikstras(board))
    # print(dfs(board, set([bhash(board)]), 0))

def part2():
    board = parse2()
    s = 0
    pprint(board)

    print(djikstras(board))
    # print(dfs(board, set([bhash(board)]), 0))


def part1_manual():
    board = parse1()
    s = 0
    pprint(board)

    # print(dfs(board, set([bhash(board)]), 0))

    s += move(board, ("room3", 0), ("hallway", 7))
    pprint(board)
    s += move(board, ("room3", 1), ("hallway", 1))
    pprint(board)
    s += move(board, ("room2", 0), ("hallway", 3))
    pprint(board)
    s += move(board, ("hallway", 7), ("room3", 1))
    pprint(board)
    s += move(board, ("room2", 1), ("room3", 0))
    pprint(board)
    s += move(board, ("hallway", 3), ("room2", 1))
    pprint(board)
    s += move(board, ("room1", 0), ("room2", 0))
    pprint(board)
    s += move(board, ("room4", 0), ("hallway", 7))
    pprint(board)
    s += move(board, ("room4", 1), ("hallway", 9))
    pprint(board)
    s += move(board, ("hallway", 7), ("room4", 1))
    pprint(board)
    s += move(board, ("room1", 1), ("room4", 0))
    pprint(board)
    s += move(board, ("hallway", 9), ("room1", 1))
    pprint(board)
    s += move(board, ("hallway", 1), ("room1", 0))

    pprint(board)
    print(s)

part1_manual()
# part1()
# part2()

