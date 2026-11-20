
#!/usr/bin/env python3

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


def load_puzzles():
    with (DATA / "practice_puzzles.csv").open(
        newline="", encoding="utf-8"
    ) as f:
        return list(csv.DictReader(f))


def main():
    puzzles = load_puzzles()

    exact_matches = 0
    mismatches = []
    total_targets = 0
    total_initial_targets = 0
    total_lower_bound = 0

    family_results = {}

    for row in puzzles:
        initial = set(json.loads(row["starting_values"]))
        targets = set(json.loads(row["targets"]))
        lower_bound = int(row["lower_bound"])

        initially_satisfied = targets & initial
        required = targets - initial

        theoretical_bound = len(required)

        total_targets += len(targets)
        total_initial_targets += len(initially_satisfied)
        total_lower_bound += lower_bound

        if lower_bound == theoretical_bound:
            exact_matches += 1
        else:
            mismatches.append({
                "id": row["id"],
                "family": row["family"],
                "provided": lower_bound,
                "calculated": theoretical_bound,
            })

        family = row["family"]
        stats = family_results.setdefault(
            family, {"count": 0, "matches": 0}
        )
        stats["count"] += 1
        stats["matches"] += (
            lower_bound == theoretical_bound
        )

    print("=" * 65)
    print("LOWER-BOUND VERIFICATION")
    print("=" * 65)

    print("Practice puzzles:", len(puzzles))
    print("Total targets:", total_targets)
    print("Initially satisfied:", total_initial_targets)
    print("Calculated minimum:", total_targets - total_initial_targets)
    print("Sum of provided bounds:", total_lower_bound)

    print(
        f"\nExact matches: {exact_matches}/{len(puzzles)}"
    )

    print("\nBY FAMILY")

    for family, stats in sorted(family_results.items()):
        print(
            f"{family:16} "
            f"{stats['matches']}/{stats['count']}"
        )

    if mismatches:
        print("\nMISMATCHES")

        for item in mismatches[:20]:
            print(item)
    else:
        print("\nSUCCESS: All supplied lower bounds match.")


if __name__ == "__main__":
    main()

