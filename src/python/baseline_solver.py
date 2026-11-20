#!/usr/bin/env python3

import json
from collections import defaultdict
from pathlib import Path

from validator import load_csv, parse_puzzle, validate_program


ROOT = Path(__file__).resolve().parents[2]
PRACTICE_FILE = ROOT / "data" / "practice_puzzles.csv"


def find_direct_instruction(target, available, destination):
    """
    Find one instruction that generates target from available registers.

    available contains tuples: (value, register_index).
    Returns an instruction or None.
    """

    for left, left_reg in available:
        for right, right_reg in available:

            # Addition
            if left + right == target:
                return ["+", left_reg, right_reg, destination]

            # Subtraction
            if left > right and left - right == target:
                return ["-", left_reg, right_reg, destination]

            # Multiplication
            if left * right == target:
                return ["*", left_reg, right_reg, destination]

            # Exact integer division
            if right != 0 and left % right == 0:
                if left // right == target:
                    return ["/", left_reg, right_reg, destination]

    return None


def solve_puzzle(puzzle):
    """
    Construct targets using direct arithmetic only.

    No intermediate values are deliberately generated.
    Every generated value is a required target.
    """

    initial = puzzle["starting_values"]
    targets = set(puzzle["targets"])
    register_count = puzzle["registers"]

    # Initial values occupy the first registers.
    available = [
        (value, index)
        for index, value in enumerate(initial)
    ]

    # Targets already available require no instructions.
    missing = targets - set(initial)

    program = []
    next_register = len(initial)

    while missing:

        if next_register >= register_count:
            break

        found_target = None
        found_instruction = None

        # Deterministic target selection.
        for target in sorted(missing):

            instruction = find_direct_instruction(
                target,
                available,
                next_register,
            )

            if instruction is not None:
                found_target = target
                found_instruction = instruction
                break

        # No remaining target can be generated directly.
        if found_instruction is None:
            break

        program.append(found_instruction)

        # Make the newly generated target available.
        available.append((found_target, next_register))

        missing.remove(found_target)
        next_register += 1

    return program, missing


def main():

    print("=" * 68)
    print("BASELINE SOLVER v0.1 — DIRECT ARITHMETIC CLOSURE")
    print("=" * 68)

    rows = load_csv(PRACTICE_FILE)

    total_puzzles = len(rows)
    completed = 0
    total_required = 0
    total_generated = 0
    total_lower_bound = 0
    total_instructions = 0
    validation_failures = []

    family_stats = defaultdict(
        lambda: {
            "puzzles": 0,
            "completed": 0,
            "required": 0,
            "generated": 0,
            "instructions": 0,
        }
    )

    incomplete_examples = []

    for row in rows:

        puzzle = parse_puzzle(row)
        family = row["family"]
        supplied_bound = int(row["lower_bound"])

        theoretical_bound = len(
            set(puzzle["targets"]) -
            set(puzzle["starting_values"])
        )

        if theoretical_bound != supplied_bound:
            raise ValueError(
                f"{puzzle['id']}: lower-bound mismatch "
                f"({theoretical_bound} != {supplied_bound})"
            )

        program, missing = solve_puzzle(puzzle)

        required = theoretical_bound
        generated = required - len(missing)

        total_required += required
        total_generated += generated
        total_lower_bound += theoretical_bound
        total_instructions += len(program)

        stats = family_stats[family]
        stats["puzzles"] += 1
        stats["required"] += required
        stats["generated"] += generated
        stats["instructions"] += len(program)

        if not missing:

            valid, details = validate_program(
                puzzle,
                program,
                raw_program=json.dumps(program),
            )

            if not valid:
                validation_failures.append(
                    (puzzle["id"], details)
                )
                continue

            completed += 1
            stats["completed"] += 1

            if details["instructions"] != theoretical_bound:
                raise AssertionError(
                    f"{puzzle['id']}: expected lower-bound "
                    "instruction count"
                )

        else:

            if len(incomplete_examples) < 10:
                incomplete_examples.append({
                    "id": puzzle["id"],
                    "family": family,
                    "generated": generated,
                    "required": required,
                    "remaining": len(missing),
                    "missing_preview": sorted(missing)[:5],
                })

    print("\nOVERALL RESULTS")
    print("-" * 68)
    print(f"Practice puzzles:       {total_puzzles}")
    print(f"Completely solved:      {completed}")
    print(f"Incomplete:             {total_puzzles - completed}")
    print(f"Required targets:       {total_required:,}")
    print(f"Generated targets:      {total_generated:,}")
    print(f"Target coverage:        "
          f"{100 * total_generated / total_required:.2f}%")
    print(f"Lower-bound total:      {total_lower_bound:,}")
    print(f"Instructions generated:{total_instructions:>10,}")

    print("\nBY FAMILY")
    print("-" * 68)

    for family in sorted(family_stats):

        stats = family_stats[family]

        coverage = (
            100 * stats["generated"] / stats["required"]
            if stats["required"] else 100
        )

        print(
            f"{family:16}"
            f"{stats['completed']:>4}/{stats['puzzles']:<4}"
            f"coverage={coverage:7.2f}%"
            f"instructions={stats['instructions']:>7,}"
        )

    print("\nVALIDATION")
    print("-" * 68)
    print(f"Validation failures: {len(validation_failures)}")

    if validation_failures:
        for puzzle_id, error in validation_failures:
            print(f"{puzzle_id}: {error}")

    print("\nINCOMPLETE EXAMPLES")
    print("-" * 68)

    for item in incomplete_examples:
        print(
            f"{item['id']} | {item['family']} | "
            f"{item['generated']}/{item['required']} generated | "
            f"remaining={item['remaining']} | "
            f"missing={item['missing_preview']}"
        )

    print("\n" + "=" * 68)

    if validation_failures:
        print("ERROR: Some completed programs failed validation.")
    elif completed == total_puzzles:
        print("SUCCESS: All puzzles solved at their theoretical lower bound.")
    else:
        print("EXPERIMENT COMPLETE: Direct arithmetic closure has limits.")

    print("=" * 68)


if __name__ == "__main__":
    main()
