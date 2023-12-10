from __future__ import annotations

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
            MAP[str((x, y))] = value

    # print(MAP)
    # print(startpoint)
    # FIND startpoints
    stack = []
    for x in range(startpoint[0] - 1, startpoint[0] + 2):
        for y in range(startpoint[1] - 1, startpoint[1] + 2):
            if x >= 0 and y >= 0 and startpoint in MAP[str((x, y))]:
                stack.append((x, y))

    print(stack)
    stack1 = [startpoint]
    stack2 = [startpoint]
    stack1.append(stack[0])
    stack2.append(stack[1])
    steps = 1
    while stack1[-1] != stack2[-1]:
        roads = MAP[str(stack1[-1])]
        if roads[0] == stack1[-2]:
            stack1.append(roads[1])
        else:
            stack1.append(roads[0])
        roads = MAP[str(stack2[-1])]
        if roads[0] == stack2[-2]:
            stack2.append(roads[1])
        else:
            stack2.append(roads[0])
        steps += 1
    return steps


INPUT_S = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
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
