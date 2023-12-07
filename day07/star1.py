
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

values_of_cards = ['A', 'K', 'Q', 'J', 'T',
                   '9', '8', '7', '6', '5', '4', '3', '2']

values_of_cards.reverse()


def calculate_value(c: str) -> int:
    cards = [*c]
    r = []
    v = 0
    for a in values_of_cards:
        r.append(cards.count(a))
    if r.count(5) == 1:
        v = 7
    elif r.count(4) == 1:
        v = 6
    elif r.count(3) == 1 and r.count(2) == 1:
        v = 5
    elif r.count(3) == 1:
        v = 4
    elif r.count(2) == 2:
        v = 3
    elif r.count(2) == 1:
        v = 2
    elif r.count(1) == 5:
        v = 1
    v = v*100
    for card in cards:
        v = v+values_of_cards.index(card)+1
        v = v*100
    return v


def compute(s: str) -> int:
    cards = {}
    lines = s.splitlines()
    for line in lines:
        c, b = line.split()
        i = calculate_value(c)
        cards[i] = int(b)
    cards = dict(sorted(cards.items()))
    sum = 0
    keys = cards.keys()
    for pos, k in enumerate(keys):
        sum = sum+cards[k]*(pos+1)
    return sum


INPUT_S = '''\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''
EXPECTED = 6440


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
