from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

MAP = {"x": 0, "m": 1, "a": 2, "s": 3}


def compute(s: str) -> int:
    rules, parts = s.split("\n\n")
    RULES = {}
    for line in rules.strip().splitlines():
        name, workflow = line.split("{")
        workflows = workflow[:-1].split(",")
        RULES[name] = workflows
    print(RULES)

    odp = 0
    for part in parts.splitlines():
        p = [int(w.split("=")[1]) for w in part[1:-1].split(",")]
        print(p)
        work_name = "in"
        while work_name != "A" or work_name != "R":
            print(work_name)
            if work_name == "A" or work_name == "R":
                break
            for r in RULES[work_name]:
                print(r)
                if ">" in r or "<" in r:
                    cond, dest = r.split(":")
                    c_var = cond[0]
                    c_op = cond[1]
                    c_thres = cond[2:]

                    if (c_op == ">" and p[MAP[c_var]] > int(c_thres)) or (
                        c_op == "<" and p[MAP[c_var]] < int(c_thres)
                    ):
                        work_name = dest
                        break
                else:
                    work_name = r
                    break
        if work_name == "A":
            odp += sum(p)
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
EXPECTED = 19114


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
