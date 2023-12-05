
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def afind(a, seed):
    x = seed
    for mapname in ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light', 'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']:
        for dest, src, r in a[mapname]:
            if src <= x < src+r:
                x = dest+x-src
                break

    # print("for seed="+str(seed)+" "+mapname+" location="+str(x))
    print("for seed="+str(seed)+" location="+str(x))
    return x


def compute(s: str) -> int:
    seeds = []
    a = {}
    lines = s.splitlines()
    mapname = ""
    for line in lines:
        if line.startswith("seeds:"):
            _, x = line.split(": ")
            seeds = [int(y) for y in x.split()]
            print(seeds)
        if "map:" in line:
            mapname, _ = line.split()
            a[mapname] = []
        if len(line) > 0 and line[0].isdigit():
            dest, src, r = [int(x) for x in line.split()]
            a[mapname].append([dest, src, r])
    print(a)
    distance = [afind(a, seed) for seed in seeds]

    return min(distance)


INPUT_S = '''\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

'''
EXPECTED = 35


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
