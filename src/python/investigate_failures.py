#!/usr/bin/env python3

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

FAILURES = {
    "scored_0597": 3,
    "scored_0798": 15,
    "scored_0931": 5,
}


def load_csv(filename):
    with (DATA / filename).open(
        newline="", encoding="utf-8"
    ) as f:
        return {
            row["id"]: row
            for row in csv.DictReader(f)
        }


puzzles = load_csv("puzzles.csv")
submissions = load_csv("sample_submission.csv")

for puzzle_id, missing_target in FAILURES.items():
    puzzle = puzzles[puzzle_id]
    submission = submissions[puzzle_id]

    initial = json.loads(puzzle["starting_values"])
    targets = json.loads(puzzle["targets"])
    program = json.loads(submission["program"])

    registers = [None] * int(puzzle["registers"])

    for i, value in enumerate(initial):
        registers[i] = value

    produced = []
    target_hits = []

    for pc, (op, a, b, dest) in enumerate(program):
        left = registers[a]
        right = registers[b]

        if op == "+":
            result = left + right
        elif op == "-":
            result = left - right
        elif op == "*":
            result = left * right
        elif op == "/":
            result = left // right
        else:
            raise ValueError(op)

        registers[dest] = result
        produced.append(result)

        if result == missing_target:
            target_hits.append(pc)

    print("\n" + "=" * 65)
    print("PUZZLE:", puzzle_id)
    print("=" * 65)

    print("Starting values:", initial)
    print("Missing target:", missing_target)
    print("Target count:", len(targets))
    print("Program instructions:", len(program))

    print("Missing target initially present:",
          missing_target in initial)

    print("Missing target appears in targets:",
          missing_target in targets)

    print("Missing target generated at instructions:",
          target_hits)

    print("Missing target in final registers:",
          missing_target in registers)

    print("\nFirst 12 instructions:")
    for pc, instruction in enumerate(program[:12]):
        print(f"  {pc:4}: {instruction}")

    print("\nLast 12 instructions:")
    start = max(0, len(program) - 12)
    for pc in range(start, len(program)):
        print(f"  {pc:4}: {program[pc]}")

    print("\nFinal register values:")
    print(registers)
