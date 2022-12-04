#!/usr/bin/env python3


def parse(assignment):
    start, end = assignment.split("-")
    return set(range(int(start), int(end) + 1))


def fully_contained(fst, snd):
    return fst <= snd or snd <= fst


def overlap(fst, snd):
    return bool(fst & snd)


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    cnt_contained = 0
    cnt_overlap = 0
    for line in lines:
        if not line:
            continue
        fst, snd = line.split(",")
        if fully_contained(parse(fst), parse(snd)):
            cnt_contained += 1
        if overlap(parse(fst), parse(snd)):
            cnt_overlap += 1
    print(cnt_contained)
    print(cnt_overlap)
