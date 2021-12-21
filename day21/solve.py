import sys
import string
import math
import re
from statistics import median, mean
import itertools
from collections import defaultdict, namedtuple, Counter

inp = sys.stdin.read().strip()
lines = inp.split("\n")
print(inp)
print(len(lines))


p1_pos = int(lines[0][-2:])
p2_pos = int(lines[1][-2:])

print(p1_pos)
print(p2_pos)


p1_score = 0
p2_score = 0


def part1():
    rolls = 0
    def roll():
        global rolls
        while True:
            for i in range(100):
                rolls += 1
                yield i + 1

    player = '1'
    dice = roll()

    print("start")
    while True:
        moves = next(dice) + next(dice) + next(dice)
        if player == '1':
            p1_pos = (p1_pos + moves - 1) % 10 + 1
            print('1', moves)
            p1_score += p1_pos
            player = '2'
            if p1_score >= 1000:
                print(p2_score * rolls)
                break
        elif player == '2':
            print('2', moves)
            p2_pos = (p2_pos + moves - 1) % 10 + 1
            p2_score += p2_pos
            player = '1'

            if p2_score >= 1000:
                print(p1_score * rolls)
                break

def part2():
    def roll():
        return Counter(map(lambda x: x[0] + x[1] + x[2], itertools.product(
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
        )))

    roll_outcomes = roll()
    memo = {}
    def outcomes(p1_data, p2_data, player):
        p1_pos, p1_score = p1_data
        p2_pos, p2_score = p2_data

        if p1_score >= 21:
            return (1, 0)
        if p2_score >= 21:
            return (0, 1)

        tup = (p1_pos, p1_score, p2_pos, p2_score, player)
        if tup in memo:
            return memo[tup]

        if player == '1':
            s = (0, 0)
            for roll_total, count in roll_outcomes.items():
                next_p1_pos = (p1_pos + roll_total - 1) % 10 + 1
                next_p1_score = p1_score + next_p1_pos
                p1_wins, p2_wins = outcomes((next_p1_pos, next_p1_score), p2_data, '2')
                s = (s[0] + count *  p1_wins, s[1] + count * p2_wins)
            memo[tup] = s
            return s
        elif player == '2':
            s = (0, 0)
            for roll_total, count in roll_outcomes.items():
                next_p2_pos = (p2_pos + roll_total - 1) % 10 + 1
                next_p2_score = p2_score + next_p2_pos
                p1_wins, p2_wins = outcomes(p1_data, (next_p2_pos, next_p2_score), '1')
                s = (s[0] + count *  p1_wins, s[1] + count * p2_wins)
            memo[tup] = s
            return s



    print(outcomes((p1_pos, 0), (p2_pos, 0), '1'))




"""
