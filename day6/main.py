#!/usr/bin/env python3

from collections import deque


def detect_marker(stream, marker_len):
    buffer = deque([], marker_len)
    for cnt, nxt in enumerate(stream, 1):
        buffer.append(nxt)
        if len(buffer) == marker_len and len(set(buffer)) == marker_len:
            return cnt


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    stream = lines[0]
    # do stuff with data
    print(detect_marker(stream, 4))
    print(detect_marker(stream, 14))
