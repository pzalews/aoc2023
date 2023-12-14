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
            if (
                line.count("O") > 0
                and (dy != -1 or y > 0)
                and (dy != 1 or y < len(lines) - 1)
            ):
                for x, c in enumerate(line):
                    if (dx != -1 or x > 0) and (dx != 1 or x < len(line) - 1):
                        if c == "O" and lines[y + dy][x + dx] == ".":
                            lines[y + dy][x + dx] = "O"
                            lines[y][x] = "."
                            modified += 1
    return lines


CACHE = {}


def rotate_cycle(lines):
    lines = rotate(lines, DIRECT["N"])
    lines = rotate(lines, DIRECT["W"])
    lines = rotate(lines, DIRECT["S"])
    lines = rotate(lines, DIRECT["E"])
    return lines


def compute(s: str) -> int:
    lines = s.splitlines()
    lines = [list(r) for r in lines]
    w = []
    finded = 0
    index = 0
    cache_mechanizm_off = True
    cache_mechanizm_off = False
    for a in range(1000000000):
        # for a in range(100):
        if finded == 0 or cache_mechanizm_off:
            lines = rotate_cycle(lines)
            w_now = calc_weight(lines)
            w.append(w_now)
            indices = [i for i, x in enumerate(w) if x == w_now]
            # print(str(a) + "=" + str(w_now))
            if len(indices) > 5:
                if (
                    indices[-1] - indices[-2]
                    == indices[-2] - indices[-3]
                    == indices[-3] - indices[-4]
                    == indices[-4] - indices[-5]
                ):
                    index = indices[-1] - indices[-2]
                    finded = len(w) - 1 - index
                    print("For " + str(w_now) + " repeat from " + str(finded))
                    print(
                        str(w_now) + " " + str(w[finded]) + " " + str(w[finded - index])
                    )
                    zostalo = 1000000000 - a

                    return w[finded + zostalo % index - 1]
        else:
            pass

    return 0


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
EXPECTED = 64


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
