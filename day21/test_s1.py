from __future__ import annotations

import argparse
import os.path

import pytest

import support
from collections import deque

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
STEPS = 64


def compute(s: str) -> int:
    grid = s.splitlines()
    start = (0, 0)
    for n, line in enumerate(grid):
        if "S" in line:
            x = line.find("S")
            start = (x, n)
    print("Start point" + str(start))
    q = deque()
    q.append((*start, 0))
    n = 0
    while n < STEPS + 1:
        x, y, n = q.popleft()
        if n > STEPS - 1:
            q.append((x, y, n))
            break
        for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            nx = x + dx
            ny = y + dy
            nn = n + 1
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                if grid[ny][nx] in ".S" and (nx, ny, nn) not in q:
                    q.append((nx, ny, nn))
                    print(nx, ny, nn)
    print(q)
    return len(q)


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
