from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

MAP = {"x": 0, "m": 1, "a": 2, "s": 3}


def count(R, ranges, work_name="in") -> int:
    if work_name == "R":
        return 0
    if work_name == "A":
        odp = 1
        for a1, a2 in ranges:
            odp = odp * (a2 - a1 + 1)
        return odp

    total = 0
    for r in R[work_name]:
        if ">" in r or "<" in r:
            cond, dest = r.split(":")
            c_var = cond[0]
            c_op = cond[1]
            c_thres = int(cond[2:])
            lo, hi = ranges[MAP[c_var]]
            if c_op == "<":
                T = (lo, c_thres - 1)
                F = (c_thres, hi)
            else:
                T = (c_thres + 1, hi)
                F = (lo, c_thres)
            if T[0] <= T[1]:
                copy = ranges.copy()
                copy[MAP[c_var]] = T
                total += count(R, copy, dest)
            if F[0] <= F[1]:
                ranges = ranges.copy()
                ranges[MAP[c_var]] = F

        else:
            total += count(R, ranges, r)

    return total


def compute(s: str) -> int:
    rules, _ = s.split("\n\n")
    RULES = {}
    for line in rules.strip().splitlines():
        name, workflow = line.split("{")
        workflows = workflow[:-1].split(",")
        RULES[name] = workflows
    print(RULES)

    odp = count(RULES, [(1, 4000), (1, 4000), (1, 4000), (1, 4000)])
    # while work_name != "A" or work_name != "R":
    #     print(work_name)
    #     if work_name == "A" or work_name == "R":
    #         break
    #     for r in RULES[work_name]:
    #         print(r)
    #         if ">" in r or "<" in r:
    #             cond, dest = r.split(":")
    #             c_var = cond[0]
    #             c_op = cond[1]
    #             c_thres = cond[2:]
    #
    #             if (c_op == ">" and p[MAP[c_var]] > int(c_thres)) or (
    #                 c_op == "<" and p[MAP[c_var]] < int(c_thres)
    #             ):
    #                 work_name = dest
    #                 break
    #         else:
    #             work_name = r
    #             break
    # if work_name == "A":
    #     odp += sum(p)
    return odp


INPUT_S = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""
EXPECTED = 167409079868000


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
