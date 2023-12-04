
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def edigit(s: str):
    digits = []
    for a in range(0, len(s)):
        if s[a].isdigit():
            digits.append(int(s[a]))
        elif s[a:].startswith('one'):
            digits.append(1)
        elif s[a:].startswith('two'):
            digits.append(2)
        elif s[a:].startswith('three'):
            digits.append(3)
        elif s[a:].startswith('four'):
            digits.append(4)
        elif s[a:].startswith('five'):
            digits.append(5)
        elif s[a:].startswith('six'):
            digits.append(6)
        elif s[a:].startswith('seven'):
            digits.append(7)
        elif s[a:].startswith('eight'):
            digits.append(8)
        elif s[a:].startswith('nine'):
            digits.append(9)
        elif s[a:].startswith('zero'):
            digits.append(0)
    return digits


def compute(s: str) -> int:
    lines = s.splitlines()
    sum = 0
    for line in lines:
        print(line)
        a = edigit(line)
        print(str(a))
        b = a[0]*10+a[-1]
        sum = sum+b
    return sum


INPUT_S = '''\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''
EXPECTED = 281


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
