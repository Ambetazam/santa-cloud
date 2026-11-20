#!/usr/bin/env python3

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

VALID_OPERATIONS = {"+", "-", "*", "/"}


def load_csv(filename):
    with (DATA / filename).open(
        newline="", encoding="utf-8"
    ) as f:
        return list(csv.DictReader(f))


def parse_puzzle(row):
    return {
        "id": row["id"],
        "starting_values": json.loads(row["starting_values"]),
        "targets": json.loads(row["targets"]),
        "value_limit": int(row["value_limit"]),
        "registers": int(row["registers"]),
    }


def validate_program(puzzle, program, raw_program=None):
    """
    Replay a program and validate its arithmetic,
    register usage, value limits, and target coverage.
    """

    puzzle_id = puzzle["id"]
    initial = puzzle["starting_values"]
    targets = set(puzzle["targets"])
    limit = puzzle["value_limit"]
    register_count = puzzle["registers"]

    if not isinstance(program, list):
        return False, "Program must be a JSON array"

    if len(program) > 4096:
        return False, "Instruction limit exceeded"

    if raw_program is not None:
        byte_count = len(raw_program.encode("utf-8"))
        if byte_count > 131072:
            return False, f"Program exceeds byte limit: {byte_count}"

    if len(initial) > register_count:
        return False, "Too many initial register values"

    registers = [None] * register_count

    for index, value in enumerate(initial):
        if type(value) is not int:
            return False, f"Initial register {index} is not an integer"

        if not 0 < value <= limit:
            return False, f"Initial register {index} violates value limit"

        registers[index] = value

    produced_targets = set()

    for pc, instruction in enumerate(program):
        if not isinstance(instruction, list) or len(instruction) != 4:
            return False, f"Instruction {pc}: expected four elements"

        op, a, b, dest = instruction

        if op not in VALID_OPERATIONS:
            return False, f"Instruction {pc}: invalid operation {op!r}"

        if any(type(x) is not int for x in (a, b, dest)):
            return False, f"Instruction {pc}: register indices must be integers"

        if any(not 0 <= x < register_count for x in (a, b, dest)):
            return False, f"Instruction {pc}: register index out of range"

        # Read BOTH sources before writing the destination.
        left = registers[a]
        right = registers[b]

        if left is None or right is None:
            return False, f"Instruction {pc}: read from undefined register"

        if op == "+":
            result = left + right

        elif op == "-":
            result = left - right

        elif op == "*":
            result = left * right

        else:
            if right == 0:
                return False, f"Instruction {pc}: division by zero"

            if left % right != 0:
                return False, f"Instruction {pc}: inexact division"

            result = left // right

        if not 0 < result <= limit:
            return False, f"Instruction {pc}: result violates value limit"

        registers[dest] = result

        if result in targets:
            produced_targets.add(result)

    missing = targets - produced_targets

    if missing:
        return False, (
            f"Missing {len(missing)} targets; "
            f"first missing values: {sorted(missing)[:5]}"
        )

    return True, {
        "instructions": len(program),
        "targets": len(targets),
        "produced_targets": len(produced_targets),
    }


def main():
    puzzles = load_csv("puzzles.csv")
    submission = load_csv("sample_submission.csv")

    puzzle_by_id = {
        row["id"]: parse_puzzle(row)
        for row in puzzles
    }

    submission_ids = [row["id"] for row in submission]

    if len(submission_ids) != len(set(submission_ids)):
        raise SystemExit("ERROR: Duplicate submission IDs")

    missing_ids = set(puzzle_by_id) - set(submission_ids)
    extra_ids = set(submission_ids) - set(puzzle_by_id)

    if missing_ids or extra_ids:
        raise SystemExit(
            f"ERROR: ID mismatch. Missing={len(missing_ids)}, "
            f"extra={len(extra_ids)}"
        )

    total_instructions = 0
    operation_counts = Counter()
    failures = []

    print("Validating sample submission...")
    print(f"Puzzles: {len(puzzles)}")

    for row in submission:
        puzzle_id = row["id"]
        puzzle = puzzle_by_id[puzzle_id]

        try:
            program = json.loads(row["program"])
        except json.JSONDecodeError as exc:
            failures.append((puzzle_id, f"Invalid JSON: {exc}"))
            continue

        valid, details = validate_program(
            puzzle,
            program,
            raw_program=row["program"],
        )

        if not valid:
            failures.append((puzzle_id, details))
            continue

        total_instructions += details["instructions"]

        for instruction in program:
            operation_counts[instruction[0]] += 1

    print("\n" + "=" * 55)
    print("VALIDATION RESULTS")
    print("=" * 55)

    print(f"Valid programs: {len(puzzles) - len(failures)}")
    print(f"Invalid programs: {len(failures)}")
    print(f"Total instructions: {total_instructions:,}")

    print("\nOperation counts:")
    for operation, count in sorted(operation_counts.items()):
        print(f"  {operation}: {count:,}")

    if failures:
        print("\nFirst validation failures:")
        for puzzle_id, reason in failures[:20]:
            print(f"  {puzzle_id}: {reason}")

        raise SystemExit(1)

    print("\nSUCCESS: Every sample program passed validation.")


if __name__ == "__main__":
    main()
