#!/usr/bin/env python3

import enum
import functools


class Cmp(enum.Enum):
    LEFT = 0
    EQ = 1
    RIGHT = 2


def compare(left, right):
    print(left, right)
    if isinstance(left, int) and isinstance(right, int):
        return left == right and Cmp.EQ or (Cmp.LEFT if left < right else Cmp.RIGHT)
    elif isinstance(left, list) and isinstance(right, list):
        for ll, rr in zip(left, right):
            res = compare(ll, rr)
            if res in (Cmp.RIGHT, Cmp.LEFT):
                return res
        return (
            len(left) == len(right)
            and Cmp.EQ
            or (Cmp.LEFT if len(left) < len(right) else Cmp.RIGHT)
        )
    else:
        if isinstance(left, int):
            left = [left]
        if isinstance(right, int):
            right = [right]
        return compare(left, right)


def cmp(left, right):
    res = compare(left, right)
    if res == Cmp.RIGHT:
        return 1
    elif res == Cmp.LEFT:
        return -1
    else:
        return 0


if __name__ == "__main__":
    with open("input") as f:
        data = f.read().strip()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data
    pairs = []
    pair = []
    for line in lines:
        if not line:
            pairs.append(pair)
            pair = []
        else:
            pair.append(eval(line))
    if pair:
        pairs.append(pair)
    res = sum(
        i
        for i, res in enumerate((compare(pair[0], pair[1]) for pair in pairs), start=1)
        if res == Cmp.LEFT
    )
    print(res)
    signals = [[[2]], [[6]]]
    for line in lines:
        if not line:
            continue
        signals.append(eval(line))

    ss = sorted(signals, key=functools.cmp_to_key(cmp))
    print(ss)
    print((ss.index([[2]]) + 1) * (ss.index([[6]]) + 1))
