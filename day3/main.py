#!/usr/bin/env python3
from string import ascii_lowercase, ascii_uppercase

from more_itertools import chunked


def priority(item):
    if (prio := ascii_lowercase.find(item)) != -1:
        return prio + 1
    elif (prio := ascii_uppercase.find(item)) != -1:
        return prio + 27
    else:
        raise RuntimeError(f"Can't calc priority for lettert {item}")


def rucksack_common(rucksack: str) -> str:
    l = len(rucksack)
    fst, snd = rucksack[: l // 2], rucksack[l // 2 :]
    common = set(fst) & set(snd)
    assert len(common) == 1
    return str(*common)


def rucksack_common_2(*rucksacks: str) -> str:
    common = set.intersection(*(set(r) for r in rucksacks))
    assert len(common) == 1
    return str(*common)


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data
    print(sum(priority(rucksack_common(line)) for line in lines if line))
    print(
        sum(
            priority(rucksack_common_2(*group))
            for group in chunked((line for line in lines if line), 3)
        )
    )
