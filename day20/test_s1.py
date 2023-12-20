from __future__ import annotations

import argparse
import os.path

import pytest

import support
from collections import deque

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
MAP = {}


def button_pushed():
    high, low = (0, 0)
    q = deque()
    q.append(("broadcaster", 0, "button"))
    while q:
        dst, signal, src = q.popleft()
        print(src, signal, dst)
        if signal == 0:
            low += 1
        else:
            high += 1
        if dst not in MAP.keys():
            continue
        device = MAP[dst]
        if device["type"] == "ff":
            if signal == 0:
                sig = 0 if device["state"] == 1 else 1
                MAP[dst]["state"] = sig
                for d in device["dst"]:
                    q.append((d, sig, dst))

        elif device["type"] == "con":
            device["state"][src] = signal
            sig = 0 if all(device["state"].values()) else 1
            for d in device["dst"]:
                q.append((d, sig, dst))
        else:
            for d in device["dst"]:
                q.append((d, signal, dst))
    return (high, low)


def compute(s: str) -> int:
    lines = s.splitlines()
    for line in lines:
        source, output = line.strip().split("-")
        type = "None"
        state = 0
        if source[0] == "%":
            type = "ff"
            source = source[1:]
        elif source[0] == "&":
            type = "con"
            source = source[1:]
            state = {}
        dst = [s.strip() for s in output[1:].split(",")]
        MAP[source.strip()] = {"type": type, "dst": dst, "state": state}

    for name, device in MAP.items():
        if device["type"] == "con":
            for k, v in MAP.items():
                if name in v["dst"]:
                    device["state"][k] = 0

    print(MAP)
    shigh, slow = (0, 0)
    for a in range(1000):
        high, low = button_pushed()
        print(high, low)
        shigh += high
        slow += low
    return slow * shigh


INPUT_S = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""
EXPECTED = 32000000


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
