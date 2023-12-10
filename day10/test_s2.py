from __future__ import annotations
import matplotlib.path as mplPath
import numpy as np
import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    lines = s.splitlines()
    MAP = {}
    startpoint = (0, 0)
    for y, line in enumerate(lines):
        MAP[y] = {}
        for x, pipe in enumerate(line):
            value = ()
            if pipe == "S":
                startpoint = (x, y)
            elif pipe == "-":
                value = ((x - 1, y), (x + 1, y))
            elif pipe == "|":
                value = ((x, y - 1), (x, y + 1))
            elif pipe == "7":
                value = ((x - 1, y), (x, y + 1))
            elif pipe == "J":
                value = ((x - 1, y), (x, y - 1))
            elif pipe == "L":
                value = ((x, y - 1), (x + 1, y))
            elif pipe == "F":
                value = ((x + 1, y), (x, y + 1))
            elif pipe == ".":
                pass
            else:
                assert False
            MAP[y][x] = value
    # print(MAP)
    # print(startpoint)
    # FIND startpoints
    stack = []
    for x in range(startpoint[0] - 1, startpoint[0] + 2):
        for y in range(startpoint[1] - 1, startpoint[1] + 2):
            if x >= 0 and y >= 0 and startpoint in MAP[y][x]:
                stack.append((x, y))

    stack1 = [startpoint]
    stack1.append(stack[0])
    while stack1[-1] != startpoint:
        p = stack1[-1]
        roads = MAP[p[1]][p[0]]
        if roads[0] == stack1[-2]:
            stack1.append(roads[1])
        else:
            stack1.append(roads[0])

    counter = 0
    bbPath = mplPath.Path(np.array(stack1))

    for y in MAP.keys():
        for x in MAP[y].keys():
            if bbPath.contains_point([x, y]) and (x, y) not in stack1:
                print((x, y))
                counter += 1
    return counter


INPUT_S = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""
EXPECTED = 8


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
