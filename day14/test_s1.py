from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def calc_weight(map):
    weight = 0
    for rx, r in enumerate(map):
        rrx = len(map) - rx
        weight += r.count("O") * rrx
    return weight


DIRECT = {"N": [0, -1], "S": [0, 1], "W": [-1, 0], "E": [1, 0]}


def rotate(lines, direction):
    modified = 1
    [dx, dy] = direction
    while modified > 0:
        modified = 0
        for y, line in enumerate(lines):
            # print(y)
            # print(line)
            if line.count("O") > 0 and y > 0:
                for x, c in enumerate(line):
                    if c == "O" and lines[y + dy][x + dx] == ".":
                        lines[y + dy][x + dx] = "O"
                        lines[y][x] = "."
                        modified += 1
    return lines


def compute(s: str) -> int:
    lines = s.splitlines()
    lines = [list(r) for r in lines]
    print(calc_weight(lines))
    lines = rotate(lines, DIRECT["N"])
    return calc_weight(lines)


INPUT_S = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
EXPECTED = 136


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
