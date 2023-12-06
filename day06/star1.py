
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    times = []
    distances = []
    lines = s.splitlines()
    for line in lines:
        if line.startswith("Time"):
            times = [int(x) for x in line.split(":")[
                1].split() if x.isdecimal()]
        if line.startswith("Distance"):
            distances = [int(x) for x in line.split(":")[
                1].split() if x.isdecimal()]
    # TODO: implement solution here!
    print(times)
    print(distances)

    odp = []
    for x in range(0, len(times)):
        odp.append(0)
        time = times[x]
        for t in range(0, time):
            d = (time-t)*t
            if d > distances[x]:
                odp[x] = odp[x]+1
        print(odp)
    result = 1
    for x in odp:
        result = result*x
    return result


INPUT_S = '''\
Time:      7  15   30
Distance:  9  40  200
'''
EXPECTED = 288


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
