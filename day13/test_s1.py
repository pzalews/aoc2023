from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compare_between(lines, y0, y1):
    a1 = min(y0, y1)
    a2 = max(y0, y1)
    if (a2 - a1) % 2 == 0:
        return False
    # print("compare between " + str((a1, a2)))
    for y in range((a2 - a1) // 2 + 2):
        # print(y)
        # print(lines[a1 + y])
        # print(lines[a2 - y])
        if lines[a1 + y] != lines[a2 - y]:
            return False
    return True


def check_pattern(lines):
    for y0, line in enumerate([lines[0], lines[-1]]):
        for y1, line2 in enumerate(lines[1:-1]):
            if line == line2:
                y1 += 1
                if y0 == 1:
                    y0 = len(lines) - 1
                print("Find" + str((y0, y1)))
                if compare_between(lines, y0, y1):
                    mirror = min(y0, y1) + abs(y0 - y1) // 2 + 1
                    print("mirror at " + str(mirror))
                    return mirror
    return 0


def compute(s: str) -> int:
    patterns = s.split("\n\n")
    vertical_mirrors = 0
    horizontal_mirrors = 0
    for pattern in patterns:
        print("")
        print(pattern)
        lines = pattern.splitlines()
        horizontal_mirrors += check_pattern(lines)

        lines_rev = ["".join(l) for l in list(zip(*lines))]  # noqa: E741
        print(lines_rev)
        print("rev:")
        print("\n".join(lines_rev))
        vertical_mirrors += check_pattern(lines_rev)

    return 100 * horizontal_mirrors + vertical_mirrors


INPUT_S = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
# INPUT_S = """\
# .####.#...##.#.
# ...###.##.#.#..
# ...###.##.#.#..
# .####.#...#..#.
# ..##......#..#.
# #.#...#.##...##
# .#.#.#..##..##.
# #..##...#####.#
# .#.#.#.#..##.#.
# .....###.#.#..#
# .....###.#.#..#
# """
# INPUT_S = """\
# #.##.##
# .####.#
# #.##.##
# #....##
# ##..##.
# ..##..#
# .####..
# #....#.
# #...###
# .#..#.#
# .#..#.#
# """
EXPECTED = 405
# EXPECTED = 1000


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
