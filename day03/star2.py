
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    lines = s.splitlines()
    sum = 0
    stars = {}
    for y in range(0, len(lines)):
        line = lines[y]
        part_number = 0
        part_number_star = [-1, -1]
        for x in range(0, len(line)):
            if line[x].isdigit():
                part_number = part_number*10+int(line[x])
                for a in [x-1, x, x+1]:
                    for b in [y-1, y, y+1]:
                        if 0 <= a < len(line) and 0 <= b < len(lines) and lines[b][a] == '*':
                            part_number_star = [a, b]

            if (not line[x].isdigit() and part_number > 0) or (x == len(line)-1):
                # koniec numeru
                if part_number_star != [-1, -1]:
                    # print(part_number)
                    if str(part_number_star) not in stars.keys():
                        stars[str(part_number_star)] = []
                    stars[str(part_number_star)].append(part_number)
                part_number = 0
                part_number_star = [-1, -1]
    print(stars)
    for a in stars.keys():
        if len(stars[a]) == 2:
            sum = sum+stars[a][0]*stars[a][1]
    return sum


INPUT_S = '''\
12.......*..
+.........34
.......-12..
..78........
..*....60...
78..........
.......23...
....90*12...
............
2.2......12.
.*.........*
1.1.......56
'''
EXPECTED = 6756


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
