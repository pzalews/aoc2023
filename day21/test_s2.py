from __future__ import annotations

import argparse
import os.path
import numpy as np
import pytest

import support
from collections import deque

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
STEPS = 6

grid = []


def go(xs, ys, steps):
    q = deque()
    q.append((xs, ys, steps))
    n = 0
    odp = set()
    seen = set()
    while q:
        x, y, n = q.popleft()
        if n == 0:
            odp.add((x, y))
            continue
        if (x, y) in seen:
            continue
        for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            nx = x + dx
            ny = y + dy
            nn = n - 1
            if (
                grid[ny % len(grid)][nx % len(grid[0])] in ".S"
                and (nx, ny, nn) not in q
            ):
                q.append((nx, ny, nn))
        seen.add((x, y))
        if n % 2 == 0:
            odp.add((x, y))
    return len(odp)


def compute(s: str) -> int:
    global grid
    grid = s.splitlines()
    start = (0, 0)
    for n, line in enumerate(grid):
        if "S" in line:
            x = line.find("S")
            start = (x, n)

    print("Start point" + str(start))
    width = len(grid)
    print("Width=" + str(width))
    X = [0, 1, 2]
    Y = []
    for i in X:
        Y.append(go(*start, i * len(grid) + len(grid) // 2))
    print(Y)
    poly = np.rint(np.polynomial.polynomial.polyfit(X, Y, 2)).astype(int).tolist()
    # poly=[a,b,c] for y=a*x^2+b*x+c
    print(poly)
    target = (26501365 - width // 2) // width
    y = poly[0] + poly[1] * target + poly[2] * target**2
    return y


INPUT_S = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""
EXPECTED = 16


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
