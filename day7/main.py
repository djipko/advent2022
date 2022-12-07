#!/usr/bin/env python3
#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, field
from operator import attrgetter
import operator
import pprint
import re


@dataclass
class Dir:
    name: str
    parent: Dir | None
    dirs: dict[str, File] = field(default_factory=dict)
    files: dict[str, Dir] = field(default_factory=dict)

    def iter_parents(self):
        if self.parent:
            yield self.parent
            yield from self.parent.iter_parents()

    @property
    def size(self):
        files = sum(f.size for f in self.files.values())
        dirs = sum(d.size for d in self.dirs.values())
        return files + dirs

    def iter_tree(self):
        for f in self.files.values():
            yield f
        for d in self.dirs.values():
            yield d
            yield from d.iter_tree()


@dataclass
class File:
    name: str
    size: int
    dir: Dir


FILE_RE = re.compile(r"(\d+) ([\w\.]+)")


def parse(commands, current_dir=None):
    while cmd := next(commands, None):
        if cmd == "$ ls":
            continue
        elif cmd.startswith("dir"):
            _, name = cmd.split()
            current_dir.dirs[name] = Dir(name, current_dir)
        elif match := FILE_RE.match(cmd):
            new_f = File(match[2], int(match[1]), current_dir)
            current_dir.files[new_f.name] = new_f
        elif cmd.startswith("$ cd"):
            *_, dirname = cmd.split()
            if dirname == "/":
                assert current_dir is None
                new_current = current_dir = Dir(dirname, None)
            elif dirname == "..":
                parse(commands, current_dir.parent)
            else:
                new_current = current_dir.dirs.get(dirname)
                parse(commands, new_current)
    return current_dir


def iter_under(root: Dir, under=100000):
    dirs = (node for node in root.iter_tree() if isinstance(node, Dir))
    return (d for d in dirs if d.size <= under)


def delete_smallest(root: Dir, space_needed=30000000, total=70000000):
    dirs = [node for node in root.iter_tree() if isinstance(node, Dir)]
    used = root.size
    candidates = sorted(
        [d for d in dirs if total - used + d.size >= space_needed],
        key=operator.attrgetter("size"),
    )
    return candidates[0]


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n") if line.strip()]
    # do stuff with data
    root = parse(iter(lines))
    # pprint.pprint(root)
    print(sum(d.size for d in iter_under(root)))
    print(delete_smallest(root).size)
