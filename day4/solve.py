import sys


lines = [l.strip() for l in sys.stdin]
global v1, v2, v3

def fn1(v):
    global v1

def fn2(v):
    global v2

def fn3(v):
    global v2

fn_map = {
    "key1": lambda v: fn1(v),
    "key2": lambda v: fn2(v)
}
order = lines[0].split(",")


class Board(object):
    def __init__(self, lines):
        self.rows = [
           line.split() for line in  lines
        ]
        self.win = False

    def __repr__(self):
        return "\n".join([
            " ".join(row) for row in self.rows
        ])

    def mark(self, number):
        for row in self.rows:
            for i, val in enumerate(row):
                if val == number:
                    row[i] = "X"

    def check(self):
        for row in self.rows:
            if all(map(lambda el: True if el is "X" else False, row)):
                return True

        for col in range(0, 5):
            if all(map(lambda rows: True if rows[col] is "X" else False, self.rows)):
                return True

        return False

    def sum(self):
        s = 0
        for row in self.rows:
            for el in row:
                if el != "X":
                    s += int(el)

        return s

boards = []
for i in range(100):
    board = Board(lines[2 + i*6 : 7 + i*6])
    boards.append(board)


def main():
    won = 0
    for entry in order:
        for i, board in enumerate(boards):
            if not board.win:
                board.mark(entry)
                if (board.check()):
                    board.win = True
                    won += 1
                    print(board)
                    print(board.sum())
                    print(entry)

main()
