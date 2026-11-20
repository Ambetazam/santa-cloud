import sys
from pathlib import Path

sys.path.insert(0, "src/python")

from validator import load_csv, parse_puzzle, validate_program
from target_closure_solver import solve

rows = load_csv(Path("data/practice_puzzles.csv"))

print("=" * 72)
print("ALL COMPLETED TARGET-CLOSURE PUZZLES")
print("=" * 72)

completed = []

for row in rows:
    puzzle = parse_puzzle(row)
    program, missing = solve(puzzle)

    if not missing:
        valid, details = validate_program(puzzle, program)

        if valid:
            lower_bound = len(
                set(puzzle["targets"]) -
                set(puzzle["starting_values"])
            )

            completed.append(
                (puzzle["id"], row["family"], len(program), lower_bound)
            )

for puzzle_id, family, instructions, lower_bound in completed:
    print(
        f"{puzzle_id:16} {family:16} "
        f"instructions={instructions:3} "
        f"lower_bound={lower_bound:3} "
        f"gap={instructions - lower_bound:3}"
    )

print("-" * 72)
print(f"Completed puzzles: {len(completed)}")
print("=" * 72)

