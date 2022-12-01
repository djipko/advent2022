#!/usr/bin/env python3

from dataclasses import dataclass, field

@dataclass
class Elf:
    calories: list[int] = field(default_factory=list)

    def total(self):
        return sum(self.calories)

if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data
    elves = []
    elf = Elf()
    for line in lines:
        if not line:
            elves.append(elf)
            elf = Elf()
        else:
            elf.calories.append(int(line))
    
    print(max(elf.total() for elf in elves))
    print(sum(sorted((elf.total() for elf in elves), reverse=True)[:3]))
        