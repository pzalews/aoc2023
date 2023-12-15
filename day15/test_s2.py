from __future__ import annotations

import argparse
import os.path

import pytest
import support

from collections import deque

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def hash(s):
    odp = 0
    for c in s:
        odp += ord(c)
        odp *= 17
        odp = odp % 256
    return odp


boxes = []
for a in range(256):
    boxes.append(dict())


def compute(s: str) -> int:
    s = s.strip().replace("\n", "")
    H = 0
    for part in s.split(","):
        label = part.split("=")[0].split("-")[0]
        operation = part[len(label)]
        box_id = hash(label)
        if operation == "=":
            boxes[box_id][label] = part[len(label) + 1]
        elif operation == "-":
            boxes[box_id].pop(label, "cos")

    for e, box in enumerate(boxes):
        print(str(e) + " " + str(box))
        for l, lens in enumerate(box.values()):
            H += (e + 1) * (l + 1) * int(lens)

    return H


INPUT_S = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""
EXPECTED = 145


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
