#!/usr/bin/env python3

import json
from collections import defaultdict
from pathlib import Path

from validator import load_csv, parse_puzzle, validate_program


ROOT = Path(__file__).resolve().parents[2]
PRACTICE_FILE = ROOT / "data" / "practice_puzzles.csv"


def find_instruction(target, available, destination, limit):

    for left, left_reg in available:
        for right, right_reg in available:

            operations = [
                ("+", left + right),
                ("-", left - right),
                ("*", left * right),
            ]

            if right != 0 and left % right == 0:
                operations.append(("/", left // right))

            for operation, result in operations:

                if result == target and 0 < result <= limit:
                    return [operation, left_reg, right_reg, destination]

    return None


def solve(puzzle):

    initial = puzzle["starting_values"]
    targets = set(puzzle["targets"])
    limit = puzzle["value_limit"]
    register_count = puzzle["registers"]

    available = [
        (value, index)
        for index, value in enumerate(initial)
    ]

    missing = targets - set(initial)

    program = []
    next_register = len(initial)

    while missing:

        if next_register >= register_count:
            break

        selected = None
        instruction = None

        for target in sorted(missing):

            candidate = find_instruction(
                target,
                available,
                next_register,
                limit,
            )

            if candidate is not None:
                selected = target
                instruction = candidate
                break

        if instruction is None:
            break

        program.append(instruction)
        available.append((selected, next_register))

        missing.remove(selected)
        next_register += 1

    return program, missing


def main():

    rows = load_csv(PRACTICE_FILE)

    completed = 0
    total_targets = 0
    generated_targets = 0
    total_instructions = 0

    family_stats = defaultdict(
        lambda: {
            "puzzles": 0,
            "completed": 0,
            "targets": 0,
            "generated": 0,
            "instructions": 0,
        }
    )

    incomplete = []
    validation_errors = []

    for row in rows:

        puzzle = parse_puzzle(row)
        family = row["family"]

        program, missing = solve(puzzle)

        required = len(
            set(puzzle["targets"]) -
            set(puzzle["starting_values"])
        )

        generated = required - len(missing)

        total_targets += required
        generated_targets += generated
        total_instructions += len(program)

        stats = family_stats[family]
        stats["puzzles"] += 1
        stats["targets"] += required
        stats["generated"] += generated
        stats["instructions"] += len(program)

        if not missing:

            valid, details = validate_program(
                puzzle,
                program,
                raw_program=json.dumps(program),
            )

            if valid:
                completed += 1
                stats["completed"] += 1

            else:
                validation_errors.append(
                    (puzzle["id"], details)
                )

        else:

            if len(incomplete) < 15:
                incomplete.append({
                    "id": puzzle["id"],
                    "family": family,
                    "generated": generated,
                    "required": required,
                    "remaining": len(missing),
                })

    print("=" * 76)
    print("TARGET DEPENDENCY CLOSURE — GREEDY BASELINE")
    print("=" * 76)

    print(f"Practice puzzles:       {len(rows)}")
    print(f"Completely solved:      {completed}")
    print(f"Incomplete:             {len(rows) - completed}")
    print(f"Required targets:       {total_targets:,}")
    print(f"Generated targets:      {generated_targets:,}")
    print(f"Target coverage:        {100 * generated_targets / total_targets:.2f}%")
    print(f"Instructions generated: {total_instructions:,}")

    print("\nBY FAMILY")
    print("-" * 76)

    for family in sorted(family_stats):

        s = family_stats[family]

        coverage = (
            100 * s["generated"] / s["targets"]
            if s["targets"] else 100
        )

        print(
            f"{family:16}"
            f"{s['completed']:3}/{s['puzzles']:<3} "
            f"coverage={coverage:7.2f}% "
            f"instructions={s['instructions']:7,}"
        )

    print("\nVALIDATION ERRORS")
    print("-" * 76)

    for puzzle_id, error in validation_errors:
        print(puzzle_id, error)

    print("\nINCOMPLETE EXAMPLES")
    print("-" * 76)

    for item in incomplete:
        print(
            f"{item['id']} | {item['family']} | "
            f"{item['generated']}/{item['required']} "
            f"generated | remaining={item['remaining']}"
        )

    print("\n" + "=" * 76)

    if completed == len(rows) and not validation_errors:
        print("SUCCESS: ALL PRACTICE PUZZLES SOLVED.")
    else:
        print("EXPERIMENT COMPLETE: TARGET-ONLY CLOSURE HAS LIMITS.")

    print("=" * 76)


if __name__ == "__main__":
    main()
