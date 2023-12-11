from __future__ import annotations

import argparse
from os import walk
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def compute(s: str) -> int:
    lines = s.splitlines()

    dense_X = [r for r, row in enumerate(lines) if all(ch == "." for ch in row)]
    dense_Y = [c for c, col in enumerate(zip(*lines)) if all(ch == "." for ch in col)]
    galactics = [
        (r, c) for r, row in enumerate(lines) for c, ch in enumerate(row) if ch == "#"
    ]

    print(dense_X)
    print(dense_Y)
    print(galactics)
    total = 0
    scale = 2

    for i, (r1, c1) in enumerate(galactics):
        for r2, c2 in galactics[:i]:
            for r in range(min(r1, r2), max(r1, r2)):
                total += scale if r in dense_X else 1
            for c in range(min(c1, c2), max(c1, c2)):
                total += scale if c in dense_Y else 1

    return total


INPUT_S = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
EXPECTED = 374


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
