from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    b = 0
    lines = s.splitlines()
    start = (0, 0)
    points = []
    points.append(start)
    for line in lines:
        d, size, _ = line.split(" ")
        x, y = start
        if d == "R":
            start = (x + int(size), y)
        elif d == "D":
            start = (x, y + int(size))
        elif d == "L":
            start = (x - int(size), y)
        elif d == "U":
            start = (x, y - int(size))
        else:
            assert False, "strange direction"
        b += int(size)
        points.append(start)

    print(points)
    print(b)
    A = (
        abs(
            sum(
                points[i][0] * (points[i - 1][1] - points[(i + 1) % len(points)][1])
                for i in range(len(points))
            )
        )
        // 2
    )
    print(A)
    i = A - b // 2 + 1
    print(i + b)
    return i + b


INPUT_S = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""
EXPECTED = 62


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
