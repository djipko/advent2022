#!/usr/bin/env python3


from string import ascii_uppercase
import re


def parse_stacks(lines):
    stacks = {i: [] for i in range(1, 10)}
    stack_lines = []
    idxs = {}
    for line in lines:
        if "".join(line.split()) == "123456789":
            for i in "123456789":
                idxs[int(i)] = line.find(i)
            break
        else:
            stack_lines.append(line)

    for line in reversed(stack_lines):
        for i in range(1, 10):
            if (crate := line[idxs[i]]) in ascii_uppercase:
                stacks[i].append(crate)
    return stacks


def execute_move_1(stacks, qty, frm, to):
    for _ in range(qty):
        stacks[to].append(stacks[frm].pop())


def execute_move_2(stacks, qty, frm, to):
    chunk = []
    for _ in range(qty):
        chunk.append(stacks[frm].pop())
    chunk.reverse()
    stacks[to].extend(chunk)


def execute(stacks, lines, execute_fn):
    move_re = re.compile(r"move (\d+) from (\d+) to (\d+)")
    for line in lines:
        if match := move_re.match(line):
            execute_fn(stacks, int(match[1]), int(match[2]), int(match[3]))


def print_top(stacks):
    print(
        "".join(
            crate for _, crate in sorted((i, stack[-1]) for i, stack in stacks.items())
        )
    )


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line for line in data.split("\n")]
    # do stuff with data
    stacks = parse_stacks(lines)
    execute(stacks, lines, execute_move_1)
    print_top(stacks)
    stacks = parse_stacks(lines)
    execute(stacks, lines, execute_move_2)
    print_top(stacks)
