from __future__ import annotations

import argparse
import os.path

import pytest

import support
import re

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
    r = re.compile(r"^..A")

    spots = [x for x in MAP.keys() if r.search(x)]
    print(spots)
    print(path)
    while len(re.findall("..Z", " ".join(spots))) < len(spots):
        direction = path[counter % len(path)]
        for a in range(len(spots)):
            if direction == "L":
                spots[a] = MAP[spots[a]][0]
            else:
                spots[a] = MAP[spots[a]][1]
        counter += 1
        print(spots)

    return counter


INPUT_S = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
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
