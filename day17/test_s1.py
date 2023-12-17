from __future__ import annotations

import argparse
import os.path

import pytest

import support
from heapq import heappop, heappush

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    lines = s.splitlines()
    grid = [list(map(int, line.strip())) for line in lines]

    seen = set()

    queue = []
    heappush(queue, (0, 0, 0, 1, 0, 0))

    while queue:
        hl, x, y, dx, dy, n = heappop(queue)

        if (x, y) == (len(grid[0]) - 1, len(grid) - 1):
            print((hl, x, y, dx, dy, n))
            print(grid[y][x])
            return hl

        if (x, y, dx, dy, n) in seen:
            continue
        seen.add((x, y, dx, dy, n))

        for ndx, ndy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if 0 <= x + ndx < len(grid[0]) and 0 <= y + ndy < len(grid):
                if (ndx, ndy) == (dx, dy):
                    if n < 3:
                        heappush(
                            queue,
                            (
                                hl + grid[y + ndy][x + ndx],
                                x + ndx,
                                y + ndy,
                                dx,
                                dy,
                                n + 1,
                            ),
                        )
                    else:
                        continue
                elif (ndx, ndy) != (-dx, -dy):
                    heappush(
                        queue,
                        (hl + grid[y + ndy][x + ndx], x + ndx, y + ndy, ndx, ndy, 1),
                    )

    return -1


INPUT_S = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""
EXPECTED = 102


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
