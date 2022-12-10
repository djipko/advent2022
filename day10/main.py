#!/usr/bin/env python3

from dataclasses import dataclass, field
from typing import Iterator
from more_itertools import chunked


@dataclass
class Instruction:
    ins: str
    arg: int | None
    ticks: int


@dataclass
class CPU:
    program: Iterator[str]
    cycle: int = 0
    x: int = 1
    curr_ins: Instruction | None = None
    next_ins_at: int = 0
    halted: bool = False
    crt: list[str] = field(default_factory=list)

    def tick(self):
        if self.halted:
            return
        if not self.curr_ins:
            self.load_ins()
            return
        self.draw_pixel()
        self.cycle += 1
        if self.next_ins_at == self.cycle:
            self.execute()
            self.load_ins()

    def draw_pixel(self):
        if len(self.crt) % 40 in (self.x, self.x - 1, self.x + 1):
            self.crt.append("#")
        else:
            self.crt.append(".")

    def load_ins(self):
        new_ins = next(self.program, None)
        if not new_ins:
            self.halted = True
            return
        ins = self.parse_ins(new_ins)
        self.curr_ins = ins
        self.next_ins_at += ins.ticks

    def parse_ins(self, ins: str):
        if ins == "noop":
            return Instruction(ins, None, 1)
        elif ins.startswith("addx"):
            _, op = ins.split()
            return Instruction("addx", int(op), 2)
        else:
            raise RuntimeError(f"Unknown instruction {ins}")

    def execute(self):
        if self.curr_ins.ins == "noop":
            pass
        elif self.curr_ins.ins == "addx":
            self.x += self.curr_ins.arg
        else:
            raise RuntimeError(f"Executing unknown  {self.curr_ins}")
        self.curr_ins = 0


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n") if line.strip()]
    # do stuff with data
    cpu = CPU(iter(lines))
    check_cycles = (20, 60, 100, 140, 180, 220)
    do_check_at = set(map(lambda c: c - 1, check_cycles))
    strengths = []
    while not cpu.halted:
        cpu.tick()
        if cpu.cycle in do_check_at:
            strengths.append((cpu.cycle + 1) * cpu.x)
    print(sum(strengths))
    for row in chunked(cpu.crt, 40):
        print("".join(row))
