#!/usr/bin/env python3

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
import functools
from operator import attrgetter
from typing import Callable


tests = [3, 11, 19, 5, 2, 7, 17, 13]
max = functools.reduce(lambda n, t: t * n, tests, 1)


@dataclass
class Item:
    value: int

    def add_x(self, x):
        self.value += x
        self.value = self.value % max

    def mul_x(self, x):
        self.value *= x
        self.value = self.value % max


@dataclass
class Monkey:
    items: list[Item]
    # op: Callable[[int], int]
    op: tuple[str, int]
    test: int
    if_true: int
    if_false: int
    inspected: int = 0

    def __post_init__(self):
        self.items = [Item(val) for val in self.items]

    def do_round(self, monkeys: list[Monkey]):
        for current in self.items:
            self.inspected += 1
            op, val = self.op
            getattr(current, f"{op}_x")(val or current.value)
            if current.value % self.test == 0:
                monkeys[self.if_true].items.append(current)
            else:
                monkeys[self.if_false].items.append(current)
        self.items = []


monkeys = [
    Monkey(
        [76, 88, 96, 97, 58, 61, 67],
        # lambda old: old * 19,
        ("mul", 19),
        3,
        2,
        3,
    ),
    Monkey(
        [93, 71, 79, 83, 69, 70, 94, 98],
        # lambda old: old + 8,
        ("add", 8),
        11,
        5,
        6,
    ),
    Monkey(
        [50, 74, 67, 92, 61, 76],
        # lambda old: old * 13,
        ("mul", 13),
        19,
        3,
        1,
    ),
    Monkey(
        [76, 92],
        # lambda old: old + 6,
        ("add", 6),
        5,
        1,
        6,
    ),
    Monkey(
        [74, 94, 55, 87, 62],
        # lambda old: old + 5,
        ("add", 5),
        2,
        2,
        0,
    ),
    Monkey(
        [59, 62, 53, 62],
        # lambda old: old * old,
        ("mul", None),
        7,
        4,
        7,
    ),
    Monkey(
        [62],
        # lambda old: old + 2,
        ("add", 2),
        17,
        5,
        7,
    ),
    Monkey(
        [85, 54, 53],
        # lambda old: old + 3,
        ("add", 3),
        13,
        4,
        0,
    ),
]

if __name__ == "__main__":
    for i in range(10000):
        for monkey in monkeys:
            monkey.do_round(monkeys)

    m1, m2, *_ = sorted(monkeys, key=attrgetter("inspected"), reverse=True)
    print(m1.inspected * m2.inspected)
