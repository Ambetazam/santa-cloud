import sys
import json
from pathlib import Path

sys.path.insert(0, "src/python")

from validator import load_csv, parse_puzzle, validate_program
from target_closure_solver import solve

rows = load_csv(Path("data/practice_puzzles.csv"))

for row in rows:
    if row["id"] == "practice_0056":
        puzzle = parse_puzzle(row)

        program, missing = solve(puzzle)

        print("Puzzle:", puzzle["id"])
        print("Initial:", puzzle["starting_values"])
        print("Targets:", puzzle["targets"])

        print("\nGenerated program:")
        for i, instruction in enumerate(program, 1):
            print(f"{i:2}: {instruction}")

        print("\nMissing:", sorted(missing))

        valid, details = validate_program(
            puzzle,
            program,
            raw_program=json.dumps(program),
        )

        print("Valid:", valid)
        print("Validation:", details)
        break

