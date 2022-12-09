#!/usr/bin/env python3

from dataclasses import dataclass, field


@dataclass(eq=True, unsafe_hash=True)
class Coord:
    x: int = 0
    y: int = 0


@dataclass
class Rope:
    head: Coord = field(default_factory=Coord)
    tail: Coord = field(default_factory=Coord)
    positions: set[Coord] = field(default_factory=lambda: set([Coord()]))

    def move(self, dir):
        if dir == "R":
            self.head.x = self.head.x + 1
        if dir == "L":
            self.head.x = self.head.x - 1
        if dir == "U":
            self.head.y = self.head.y + 1
        if dir == "D":
            self.head.y = self.head.y - 1
        self.move_tail()

    def move_head(self, new_head: Coord):
        self.head.x = new_head.x
        self.head.y = new_head.y
        self.move_tail()

    def is_touching(self):
        return self.tail.x in (
            self.head.x + 1,
            self.head.x,
            self.head.x - 1,
        ) and self.tail.y in (self.head.y + 1, self.head.y, self.head.y - 1)

    def move_tail(self):
        if self.is_touching():
            return
        if self.tail.x == self.head.x:
            self.tail.y = (
                self.tail.y + 1 if self.head.y > self.tail.y else self.tail.y - 1
            )
        elif self.tail.y == self.head.y:
            self.tail.x = (
                self.tail.x + 1 if self.head.x > self.tail.x else self.tail.x - 1
            )
        else:
            self.tail.y = (
                self.tail.y + 1 if self.head.y > self.tail.y else self.tail.y - 1
            )
            self.tail.x = (
                self.tail.x + 1 if self.head.x > self.tail.x else self.tail.x - 1
            )
        self.positions.add(Coord(self.tail.x, self.tail.y))

    def do_move(self, dir, count):
        for _ in range(count):
            self.move(dir)


class MultiRope:
    def __init__(self, knots):
        self.knots = []
        for _ in range(knots - 1):
            self.knots.append(Rope())

    def move(self, dir):
        head = prev = self.knots[0]
        head.move(dir)
        for k in self.knots[1:]:
            k.move_head(prev.tail)
            prev = k

    def do_move(self, dir, count):
        for _ in range(count):
            self.move(dir)


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data
    rope = Rope()
    for ins in lines:
        if not ins:
            continue
        dir, cnt = ins.split()
        rope.do_move(dir, int(cnt))
    print(len(rope.positions))
    mrope = MultiRope(10)
    for ins in lines:
        if not ins:
            continue
        dir, cnt = ins.split()
        mrope.do_move(dir, int(cnt))
    print(len(mrope.knots[-1].positions))
