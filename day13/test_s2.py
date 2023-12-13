from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def diff_lines(line1, line2):
    errors = 0
    for c in range(len(line1)):
        if line1[c] != line2[c]:
            errors += 1
    return errors


def compare_between(lines, y0, y1):
    errors = 0
    a1 = min(y0, y1)
    a2 = max(y0, y1)
    if (a2 - a1) % 2 == 0:
        return False
    # print("compare between " + str((a1, a2)))
    for y in range((a2 - a1) // 2 + 1):
        print(y)
        print(lines[a1 + y])
        print(lines[a2 - y])
        errors += diff_lines(lines[a1 + y], lines[a2 - y])
    if errors == 1:
        return True
    return False


def get_column(lines, col):
    return "".join([line[col] for line in lines])


def get_columns(lines, start, end):
    return [get_column(lines, y) for y in range(start, end)]


def compute(s: str) -> int:
    patterns = s.split("\n\n")
    vertical_mirrors = 0
    horizontal_mirrors = 0
    for pattern in patterns:
        print("")
        print(pattern)
        lines = pattern.splitlines()
        for y0, line in enumerate([lines[0], lines[-1]]):
            for y1, line2 in enumerate(lines[1:-1]):
                if diff_lines(line, line2) < 2:
                    y1 += 1
                    if y0 == 1:
                        y0 = len(lines) - 1
                    print("Find" + str((y0, y1)))
                    print(line)
                    print(line2)
                    if compare_between(lines, y0, y1):
                        mirror = min(y0, y1) + abs(y0 - y1) // 2 + 1
                        horizontal_mirrors += mirror
                        print("mirror at " + str(mirror))

        lines_rev = get_columns(lines, 0, len(lines[0]))
        print("rev:")
        print("\n".join(lines_rev))
        for y0, line in enumerate([lines_rev[0], lines_rev[-1]]):
            for y1, line2 in enumerate(lines_rev[1:-1]):
                if diff_lines(line, line2) < 2:
                    y1 += 1
                    if y0 == 1:
                        y0 = len(lines_rev) - 1
                    # print(str(y0) + ":" + str(line))
                    # print(str(y1) + ":" + str(line2))
                    print("Find" + str((y0, y1)))
                    if compare_between(lines_rev, y0, y1):
                        mirror = min(y0, y1) + abs(y0 - y1) // 2 + 1
                        vertical_mirrors += mirror
                        print("mirror at " + str(mirror))

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
EXPECTED = 400
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
