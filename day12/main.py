#!/usr/bin/env python3

import heapq
import math
from string import ascii_lowercase


def parse_fld(fld):
    if fld == "S":
        fld = "a"
    if fld == "E":
        fld = "z"
    return ascii_lowercase.index(fld)


def get_start_end(input):
    start = end = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "S":
                start = (x, y)
            if c == "E":
                end = (x, y)
    return start, end


def adj(terrain, x, y):
    w, h = len(terrain[0]), len(terrain)
    current = terrain[y][x]
    coord = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
    candidates = []
    for xx, yy in coord:
        if 0 <= xx < w and 0 <= yy < h and (xx, yy) != (x, y):
            if terrain[yy][xx] > current + 1:
                continue
            candidates.append((xx, yy))
    return sorted(
        candidates, key=lambda cand: terrain[cand[1]][cand[0]] - current, reverse=True
    )


def dijkstra(terrain, start):
    w, h = len(terrain[0]), len(terrain)
    unvisited = set((x, y) for x in range(w) for y in range(h))
    shortest = {c: math.inf for c in unvisited}
    frontier = []
    # previous = {}
    shortest[start] = 0
    heapq.heappush(frontier, (0, start))
    while unvisited and frontier:
        _dist, current_min = heapq.heappop(frontier)

        for nx, ny in adj(terrain, *current_min):
            if (nx, ny) not in unvisited:
                continue
            tentative = shortest[current_min] + 1
            if tentative < shortest[(nx, ny)]:
                shortest[(nx, ny)] = tentative
                heapq.heappush(frontier, (tentative, (nx, ny)))
                # previous[(nx, ny)] = current_min
        unvisited.discard(current_min)
    return shortest


if __name__ == "__main__":
    with open("input") as f:
        data = f.read().strip()
    lines = [line.strip() for line in data.split("\n")]

    start, end = get_start_end(lines)
    terrain = [list(map(parse_fld, l)) for l in lines]
    paths = dijkstra(terrain, start)
    print(paths[end])
    w, h = len(terrain[0]), len(terrain)
    starting_points = [(x, y) for y in range(h) for x in range(w) if terrain[y][x] == 0]
    path_lens = []
    for start in starting_points:
        paths = dijkstra(terrain, start)
        path_lens.append(paths[end])
    print(min(path_lens))
