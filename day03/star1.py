
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    lines = s.splitlines()
    sum = 0
    for y in range(0, len(lines)):
        line = lines[y]
        part_number = 0
        part_number_check = False
        for x in range(0, len(line)):
            if line[x].isdigit():
                part_number = part_number*10+int(line[x])
                for a in [x-1, x, x+1]:
                    for b in [y-1, y, y+1]:
                        if 0 <= a < len(line) and 0 <= b < len(lines) and lines[b][a] != '.' and not lines[b][a].isdigit():
                            part_number_check = True

            if (not line[x].isdigit() and part_number > 0) or (x == len(line)-1):
                # koniec numeru
                if part_number_check:
                    print(part_number)
                    sum = sum+part_number
                part_number = 0
                part_number_check = False

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
EXPECTED = 413


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
