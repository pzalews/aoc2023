from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def hash(s):
    odp = 0
    for c in s:
        odp += ord(c)
        odp *= 17
        odp = odp % 256
    return odp


def compute(s: str) -> int:
    assert hash("rn=1") == 30
    assert hash("cm-") == 253
    assert hash("qp=3") == 97
    s = s.replace("\n", "")
    H = 0
    for part in s.split(","):
        H += hash(part)
    return H


INPUT_S = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""
EXPECTED = 1320


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
