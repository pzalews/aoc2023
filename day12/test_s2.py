from __future__ import annotations

import argparse
import os.path

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

cache = {}


def iterate(pattern, groups, flag=False):
    key = (pattern, groups, flag)
    if key in cache:
        return cache[key]

    result = 0
    if pattern == "":
        result = 1 if sum(groups) == 0 else 0

    elif sum(groups) == 0:
        result = 0 if "#" in pattern else 1

    elif pattern[0] == "#":
        if flag and groups[0] == 0:
            result = 0
        else:
            result = iterate(pattern[1:], (groups[0] - 1, *groups[1:]), True)

    elif pattern[0] == ".":
        if flag and groups[0] > 0:
            result = 0
        else:
            result = iterate(
                pattern[1:], groups[1:] if groups[0] == 0 else groups, False
            )

    elif flag:
        if groups[0] == 0:
            result = iterate(pattern[1:], groups[1:], False)
        else:
            result = iterate(pattern[1:], (groups[0] - 1, *groups[1:]), True)
    else:
        result = iterate(pattern[1:], groups, False) + iterate(
            pattern[1:], (groups[0] - 1, *groups[1:]), True
        )

    if key not in cache:
        cache[key] = result
    return result


def compute(s: str) -> int:
    lines = s.splitlines()
    assert 10 == iterate("?###????????", (3, 2, 1))
    assert 1 == iterate("?#?#?#?#?#?#?#?", (1, 3, 1, 6))
    assert 1 == iterate("???.###", (1, 1, 3))
    assert 4 == iterate(".??..??...?##.", (1, 1, 3))
    res = 0
    for line in lines:
        word, regex = line.split(" ")
        word = word + "?" + word + "?" + word + "?" + word + "?" + word
        regex = regex + "," + regex + "," + regex + "," + regex + "," + regex
        print(word)
        print(regex)
        regex = [int(x) for x in regex.split(",")]
        res += iterate(word, tuple(regex))
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
