from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    lines = s.splitlines()
    path = lines[0]
    MAP = {}
    for line in lines[2:]:
        spot, directions = line.split("=")
        left, right = (
            directions.replace("(", "").replace(",", "").replace(")", "").split()
        )
        MAP[spot.strip()] = (left, right)

    counter = 0
    spot = "AAA"
    while spot != "ZZZ":
        direction = path[counter % len(path)]
        if direction == "L":
            spot = MAP[spot][0]
        else:
            spot = MAP[spot][1]
        counter += 1

    print(path)

    return counter


INPUT_S = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""
EXPECTED = 6


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
