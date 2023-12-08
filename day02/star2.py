from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def extract_gems(s: str):
    [red, green, blue] = [0, 0, 0]
    for a in s.split(","):
        if a.split()[1] == "red":
            red = int(a.split()[0])
        elif a.split()[1] == "green":
            green = int(a.split()[0])
        elif a.split()[1] == "blue":
            blue = int(a.split()[0])
    return [red, green, blue]


def compute(s: str) -> int:
    lines = s.splitlines()
    games = []
    for line in lines:
        data = line.split(":")[1]
        maxs = [0, 0, 0]
        for s in data.split(";"):
            gems = extract_gems(s)
            for a in range(0, 3):
                if maxs[a] < gems[a]:
                    maxs[a] = gems[a]
        games.append(maxs)
    sum = 0
    print(games)
    for a in games:
        sum = sum + a[0] * a[1] * a[2]

    return sum


INPUT_S = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
EXPECTED = 2286


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
