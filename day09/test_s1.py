from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    lines = s.splitlines()
    riddles = []
    for line in lines:
        r = [int(x) for x in line.split()]
        riddles.append(r)
    odp = []
    for riddle in riddles:
        next = 0
        while not all(x == 0 for x in riddle):
            next = next + riddle[-1]
            riddle = [j - i for i, j in zip(riddle[:-1], riddle[1:])]
        odp.append(next)
    return sum(odp)


INPUT_S = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
EXPECTED = 114


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
