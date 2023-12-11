from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

MAX = 1000000


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def compute(s: str) -> int:
    lines = s.splitlines()
    y = 0
    dense_X = []
    dense_Y = []
    galactics = []
    x = 0
    y = 0
    for line in lines:
        if "#" not in line:
            dense_Y.append(y + len(dense_Y) * (MAX - 1))
        y += 1
    for c in range(len(lines[0])):
        count = 0
        for line in lines:
            if line[c] == "#":
                count += 1
        if count == 0:
            dense_X.append(c + len(dense_X) * (MAX - 1))
    x = 0
    y = 0
    print(dense_X)
    for line in lines:
        x = 0
        for c in line:
            if "#" == c:
                galactics.append((x, y))
            elif x in dense_X:
                x += MAX - 1
            x += 1
        if y in dense_Y:
            y += MAX - 1
        y += 1
    print(galactics)
    odl = []
    # assert distance(galactics[0], galactics[6]) == 15
    # assert distance(galactics[2], galactics[5]) == 17
    # assert distance(galactics[7], galactics[8]) == 5
    for i, g1 in enumerate(galactics):
        for g2 in galactics[i + 1 :]:
            r = distance(g1, g2)
            odl.append(r)
    print(len(odl))
    return sum(odl)


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
EXPECTED = 8410


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
