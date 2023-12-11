from __future__ import annotations

import argparse
import os.path
from collections import deque
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def fast_check(s, regex):
    strict = True
    if "?" in s:
        s = s[0 : s.index("?")]
        strict = False
    count = 0
    countg = 0
    for c in s:
        if c == "#":
            count += 1
        elif c == ".":
            if count > 0:
                if countg >= len(regex) or regex[countg] != count:
                    return False
                countg += 1
                count = 0

    if count > 0:
        if countg >= len(regex) or regex[countg] < count:
            return False
        if strict and regex[countg] != count:
            return False
        countg += 1
    if strict and countg != len(regex):
        return False

    return True


def calculate(s: str, regex: list[int]):
    a = deque()
    # print(s)
    a.append((s, regex))
    odp = 0
    while len(a) != 0:
        word, regex = a.pop()
        # print(word)
        # print(regex)
        if "?" in word:
            if fast_check(word, regex):
                a.append((word.replace("?", ".", 1), regex))
                a.append((word.replace("?", "#", 1), regex))
        else:
            # print(word)
            # print(regex)
            # print(regex2)
            if fast_check(word, regex):
                # print(word)
                # print(regex)
                odp += 1
    print(odp)
    return odp


def compute(s: str) -> int:
    lines = s.splitlines()
    assert 10 == calculate("?###????????", [3, 2, 1])
    assert 1 == calculate("?#?#?#?#?#?#?#?", [1, 3, 1, 6])
    assert 1 == calculate("???.###", [1, 1, 3])
    assert 4 == calculate(".??..??...?##.", [1, 1, 3])
    assert fast_check("##..##?", [1, 2]) is False
    res = 0
    for line in lines:
        word, regex = line.split(" ")
        word = word + "?" + word + "?" + word + "?" + word + "?" + word
        regex = regex + "," + regex + "," + regex + "," + regex + "," + regex
        print(word)
        print(regex)
        regex = [int(x) for x in regex.split(",")]
        res += calculate(word, regex)
    return res


INPUT_S = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
# EXPECTED = 21
EXPECTED = 525152


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
