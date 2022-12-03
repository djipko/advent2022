#!/usr/bin/env python3

import enum
import functools
from dataclasses import dataclass, field


class MoveT(enum.Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


def parse_move(c):
    if c in "AX":
        return MoveT.ROCK
    if c in "BY":
        return MoveT.PAPER
    if c in "CZ":
        return MoveT.SCISSORS


@dataclass
@functools.total_ordering
class Move:
    move: MoveT

    def __eq__(self, other):
        return self.move == other.move

    def __lt__(self, other):
        if self.move == MoveT.ROCK and other.move == MoveT.PAPER:
            return True
        elif self.move == MoveT.PAPER and other.move == MoveT.SCISSORS:
            return True
        elif self.move == MoveT.SCISSORS and other.move == MoveT.ROCK:
            return True
        else:
            return False


def find_my_move(elf, me):
    for my_move in (Move(m) for m in MoveT):
        if elf > my_move and me == "X":
            return my_move
        elif elf < my_move and me == "Z":
            return my_move
        elif elf == my_move and me == "Y":
            return my_move
    raise RuntimeError(f"Can't parse move {me}")


def play_round(elf: Move, me: Move) -> int:
    if me > elf:
        return int(me.move.value) + 6
    elif me == elf:
        return int(me.move.value) + 3
    return int(me.move.value)


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data
    score = 0
    for line in lines:
        if not line:
            continue
        elf, me = [Move(parse_move(m)) for m in line.split(" ")]
        score += play_round(elf, me)
    print(score)
    score = 0
    for line in lines:
        if not line:
            continue
        elf, me = line.split(" ")
        elf = Move(parse_move(elf))
        me = find_my_move(elf, me)
        score += play_round(elf, me)
    print(score)
