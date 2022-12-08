#!/usr/bin/env python3

from heapq import heapify, heappush
from itertools import takewhile


tree_map = []


def visible_from_horizontal(y, w, side="left"):
    seen = []
    visible = set()
    line = tree_map[y] if side == "left" else reversed(tree_map[y])

    for x, tree in enumerate(line):
        if not seen or -seen[0] < tree:
            visible.add((x if side == "left" else w - 1 - x, y))
        heappush(seen, -tree)
    return visible


def visible_from_vertical(x, h, side="top"):
    seen = []
    visible = set()
    tree_iter = [row[x] for row in tree_map]
    line = tree_iter if side == "top" else reversed(tree_iter)

    for y, tree in enumerate(line):
        if not seen or -seen[0] < tree:
            visible.add((x, y if side == "top" else h - 1 - y))
        heappush(seen, -tree)
    return visible


def scenic_score_horizontal(y, from_x, side="left"):
    line = (
        tree_map[y][from_x:]
        if side == "left"
        else list(reversed(tree_map[y][: from_x - 1]))
    )
    me = tree_map[y][from_x - 1]
    if not line:
        return 0

    return min(len(line), len([tree for tree in takewhile(lambda t: t < me, line)]) + 1)


def scenic_score_vertical(x, from_y, side="top"):
    tree_iter = [
        row[x]
        for row in (tree_map[from_y:] if side == "top" else tree_map[: from_y - 1])
    ]
    line = tree_iter if side == "top" else list(reversed(tree_iter))
    me = tree_map[from_y - 1][x]
    if not line:
        return 0

    return min(len(line), len([tree for tree in takewhile(lambda t: t < me, line)]) + 1)


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data
    for line in lines:
        if not line:
            continue
        tree_map.append([int(tree) for tree in line])
    h, w = len(tree_map), len(tree_map[0])
    seen = set()
    for side in ("left", "right"):
        for y in range(h):
            seen |= visible_from_horizontal(y, w, side)
    for side in ("top", "bottom"):
        for x in range(w):
            seen |= visible_from_vertical(x, h, side)
    print(len(seen))
    scenic_scores = {}
    for x in range(0, w):
        for y in range(0, h):
            scenic_scores[(x, y)] = (
                scenic_score_horizontal(y, x + 1, "left")
                * scenic_score_horizontal(y, x + 1, "right")
                * scenic_score_vertical(x, y + 1, "top")
                * scenic_score_vertical(x, y + 1, "bottom")
            )
    print(max(scenic_scores.values()))
