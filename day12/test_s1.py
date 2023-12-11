from __future__ import annotations

import argparse
import os.path
from collections import deque
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def calculate(s: str):
    a = deque()
    a.append(s)
    odp = 0
    while len(a) != 0:
        w = a.pop()
        if "?" in w:
            a.append(w.replace("?", ".", 1))
            a.append(w.replace("?", "#", 1))
        else:
            word, regex = w.split(" ")
            regex = [int(x) for x in regex.split(",")]
            regex2 = []
            count = 0
            for c in word:
                if c == "#":
                    count += 1
                elif c == ".":
                    if count > 0:
                        regex2.append(count)
                        count = 0
                else:
                    assert False, c
            if count > 0:
                regex2.append(count)
            # print(word)
            # print(regex)
            # print(regex2)
            if regex == regex2:
                odp += 1
    return odp


def compute(s: str) -> int:
    lines = s.splitlines()
    assert 1 == calculate("???.### 1,1,3")
    assert 4 == calculate(".??..??...?##. 1,1,3")
    res = 0
    for line in lines:
        res += calculate(line)
    return res


INPUT_S = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
EXPECTED = 21


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
