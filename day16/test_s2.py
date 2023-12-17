from __future__ import annotations

import argparse
import os.path

import pytest
from collections import deque
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def calc(grid, r, c, dr, dc):
    # r, c, dr, dc
    a = [(r, c, dr, dc)]
    seen = set()
    q = deque(a)

    while q:
        r, c, dr, dc = q.popleft()

        r += dr
        c += dc

        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
            continue

        ch = grid[r][c]

        if ch == "." or (ch == "-" and dc != 0) or (ch == "|" and dr != 0):
            if (r, c, dr, dc) not in seen:
                seen.add((r, c, dr, dc))
                q.append((r, c, dr, dc))
        elif ch == "/":
            dr, dc = -dc, -dr
            if (r, c, dr, dc) not in seen:
                seen.add((r, c, dr, dc))
                q.append((r, c, dr, dc))
        elif ch == "\\":
            dr, dc = dc, dr
            if (r, c, dr, dc) not in seen:
                seen.add((r, c, dr, dc))
                q.append((r, c, dr, dc))
        else:
            for dr, dc in [(1, 0), (-1, 0)] if ch == "|" else [(0, 1), (0, -1)]:
                if (r, c, dr, dc) not in seen:
                    seen.add((r, c, dr, dc))
                    q.append((r, c, dr, dc))

    coords = {(r, c) for (r, c, _, _) in seen}

    return len(coords)


def compute(s: str) -> int:
    grid = s.splitlines()
    # r, c, dr, dc
    max_val = 0

    for r in range(len(grid)):
        max_val = max(max_val, calc(grid, r, -1, 0, 1))
        max_val = max(max_val, calc(grid, r, len(grid[0]), 0, -1))

    for c in range(len(grid[0])):
        max_val = max(max_val, calc(grid, -1, c, 1, 0))
        max_val = max(max_val, calc(grid, len(grid), c, -1, 0))
    return max_val


INPUT_S = """\
.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....
"""
EXPECTED = 51


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
