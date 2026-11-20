#!/usr/bin/env python3

import csv
import json
from collections import Counter
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"

PUZZLES_FILE = DATA_DIR / "puzzles.csv"
SUBMISSION_FILE = DATA_DIR / "sample_submission.csv"

VALID_OPERATIONS = {"+", "-", "*", "/"}

MAX_INSTRUCTIONS = 4096
MAX_PROGRAM_BYTES = 131072


# ============================================================
# CSV loading
# ============================================================

def load_csv(path):
    """Load a CSV file and return its rows."""
    with path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        return list(csv.DictReader(file))


def parse_puzzle(row):
    """Convert a CSV puzzle row into typed Python data."""
    return {
        "id": row["id"],
        "starting_values": json.loads(row["starting_values"]),
        "targets": json.loads(row["targets"]),
        "value_limit": int(row["value_limit"]),
        "registers": int(row["registers"]),
    }


# ============================================================
# Program validation
# ============================================================

def validate_program(puzzle, program, raw_program=None):
    """
    Execute and validate a program.

    Returns:
        (True, statistics) if valid.
        (False, error_message) otherwise.
    """

    initial = puzzle["starting_values"]
    targets = set(puzzle["targets"])
    value_limit = puzzle["value_limit"]
    register_count = puzzle["registers"]

    # --------------------------------------------------------
    # Program structure
    # --------------------------------------------------------

    if not isinstance(program, list):
        return False, "Program must be a JSON array"

    if len(program) > MAX_INSTRUCTIONS:
        return False, "Instruction limit exceeded"

    if raw_program is not None:
        byte_count = len(raw_program.encode("utf-8"))

        if byte_count > MAX_PROGRAM_BYTES:
            return False, (
                f"Program exceeds byte limit: {byte_count}"
            )

    if len(initial) > register_count:
        return False, "Too many initial register values"

    # --------------------------------------------------------
    # Initialize registers
    # --------------------------------------------------------

    registers = [None] * register_count

    for index, value in enumerate(initial):
        if type(value) is not int:
            return False, (
                f"Initial register {index} is not an integer"
            )

        if not 0 < value <= value_limit:
            return False, (
                f"Initial register {index} violates value limit"
            )

        registers[index] = value

    # Initial values can already satisfy targets.
    satisfied_targets = set(initial) & targets

    # --------------------------------------------------------
    # Execute instructions
    # --------------------------------------------------------

    for pc, instruction in enumerate(program):

        if not isinstance(instruction, list):
            return False, (
                f"Instruction {pc}: expected a list"
            )

        if len(instruction) != 4:
            return False, (
                f"Instruction {pc}: expected four elements"
            )

        op, a, b, dest = instruction

        if op not in VALID_OPERATIONS:
            return False, (
                f"Instruction {pc}: invalid operation {op!r}"
            )

        if any(
            type(index) is not int
            for index in (a, b, dest)
        ):
            return False, (
                f"Instruction {pc}: register indices "
                "must be integers"
            )

        if any(
            not 0 <= index < register_count
            for index in (a, b, dest)
        ):
            return False, (
                f"Instruction {pc}: register index out of range"
            )

        # Read both source registers before writing destination.
        left = registers[a]
        right = registers[b]

        if left is None or right is None:
            return False, (
                f"Instruction {pc}: read from undefined register"
            )

        # ----------------------------------------------------
        # Arithmetic
        # ----------------------------------------------------

        if op == "+":
            result = left + right

        elif op == "-":
            result = left - right

        elif op == "*":
            result = left * right

        elif op == "/":

            if right == 0:
                return False, (
                    f"Instruction {pc}: division by zero"
                )

            if left % right != 0:
                return False, (
                    f"Instruction {pc}: inexact division"
                )

            result = left // right

        # ----------------------------------------------------
        # Validate result
        # ----------------------------------------------------

        if type(result) is not int:
            return False, (
                f"Instruction {pc}: result is not an integer"
            )

        if not 0 < result <= value_limit:
            return False, (
                f"Instruction {pc}: result {result} "
                "violates value limit"
            )

        registers[dest] = result

        if result in targets:
            satisfied_targets.add(result)

    # --------------------------------------------------------
    # Target coverage
    # --------------------------------------------------------

    missing_targets = targets - satisfied_targets

    if missing_targets:
        preview = sorted(missing_targets)[:10]

        return False, (
            f"Missing {len(missing_targets)} targets; "
            f"first missing values: {preview}"
        )

    return True, {
        "instructions": len(program),
        "target_count": len(targets),
        "satisfied_targets": len(satisfied_targets),
    }


# ============================================================
# Submission validation and benchmarking
# ============================================================

def main():

    print("Loading competition data...")

    puzzle_rows = load_csv(PUZZLES_FILE)
    submission_rows = load_csv(SUBMISSION_FILE)

    puzzles = {
        row["id"]: parse_puzzle(row)
        for row in puzzle_rows
    }

    submission_ids = [
        row["id"]
        for row in submission_rows
    ]

    # --------------------------------------------------------
    # Check submission identifiers
    # --------------------------------------------------------

    duplicate_ids = {
        puzzle_id
        for puzzle_id in submission_ids
        if submission_ids.count(puzzle_id) > 1
    }

    missing_ids = set(puzzles) - set(submission_ids)
    extra_ids = set(submission_ids) - set(puzzles)

    if duplicate_ids or missing_ids or extra_ids:
        print("\nSUBMISSION ID ERROR")
        print("Duplicates:", sorted(duplicate_ids)[:10])
        print("Missing:", sorted(missing_ids)[:10])
        print("Extra:", sorted(extra_ids)[:10])

        raise SystemExit(1)

    # --------------------------------------------------------
    # Validate all programs
    # --------------------------------------------------------

    total_instructions = 0
    valid_instructions = 0

    operation_counts = Counter()
    failures = []

    total_program_bytes = 0

    print(f"Validating {len(puzzles)} programs...\n")

    for row in submission_rows:

        puzzle_id = row["id"]
        raw_program = row["program"]

        # Parse JSON.
        try:
            program = json.loads(raw_program)

        except json.JSONDecodeError as error:
            failures.append(
                (puzzle_id, f"Invalid JSON: {error}")
            )
            continue

        # Count every parsed program, whether valid or not.
        total_instructions += len(program)
        total_program_bytes += len(
            raw_program.encode("utf-8")
        )

        if isinstance(program, list):
            for instruction in program:
                if (
                    isinstance(instruction, list)
                    and len(instruction) == 4
                    and instruction[0] in VALID_OPERATIONS
                ):
                    operation_counts[instruction[0]] += 1

        valid, details = validate_program(
            puzzles[puzzle_id],
            program,
            raw_program=raw_program,
        )

        if not valid:
            failures.append((puzzle_id, details))
            continue

        valid_instructions += details["instructions"]

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    valid_count = len(puzzles) - len(failures)

    print("=" * 65)
    print("VALIDATION RESULTS")
    print("=" * 65)

    print(f"Total puzzles:       {len(puzzles):,}")
    print(f"Valid programs:      {valid_count:,}")
    print(f"Invalid programs:    {len(failures):,}")

    print("\nINSTRUCTION BENCHMARK")
    print("-" * 65)

    print(f"Submitted instructions: {total_instructions:,}")
    print(f"Valid-program instructions: {valid_instructions:,}")

    if puzzles:
        print(
            "Average instructions per puzzle: "
            f"{total_instructions / len(puzzles):,.2f}"
        )

    print("\nOPERATION DISTRIBUTION")
    print("-" * 65)

    for operation in sorted(VALID_OPERATIONS):
        print(
            f"{operation}: "
            f"{operation_counts[operation]:,}"
        )

    print("\nPROGRAM SIZE")
    print("-" * 65)

    print(
        "Total program bytes: "
        f"{total_program_bytes:,}"
    )

    print(
        "Average program bytes: "
        f"{total_program_bytes / len(submission_rows):,.2f}"
    )

    if failures:
        print("\nVALIDATION FAILURES")
        print("-" * 65)

        for puzzle_id, reason in failures[:20]:
            print(f"{puzzle_id}: {reason}")

        raise SystemExit(1)

    print("\nSUCCESS: ALL PROGRAMS PASSED VALIDATION.")


if __name__ == "__main__":
    main()
