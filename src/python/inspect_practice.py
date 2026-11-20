#!/usr/bin/env python3

import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILE = ROOT / "data" / "practice_puzzles.csv"


def load_puzzles():
    with FILE.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as f:
        return list(csv.DictReader(f))


def describe(values):
    if not values:
        return "No data"

    return (
        f"min={min(values)}, "
        f"median={statistics.median(values)}, "
        f"mean={statistics.mean(values):.2f}, "
        f"max={max(values)}"
    )


def main():
    puzzles = load_puzzles()

    family_stats = defaultdict(list)
    tier_stats = defaultdict(list)

    target_counts = []
    lower_bounds = []
    initial_target_counts = []

    for row in puzzles:
        initial = json.loads(row["starting_values"])
        targets = json.loads(row["targets"])

        family = row["family"]
        tier = row["design_tier"]
        lower_bound = int(row["lower_bound"])

        target_count = len(targets)
        initial_hits = len(set(initial) & set(targets))

        target_counts.append(target_count)
        lower_bounds.append(lower_bound)
        initial_target_counts.append(initial_hits)

        family_stats[family].append(lower_bound)
        tier_stats[tier].append(lower_bound)

    print("=" * 70)
    print("PRACTICE PUZZLE PROFILE")
    print("=" * 70)

    print("Total puzzles:", len(puzzles))
    print("Average targets:", round(statistics.mean(target_counts), 2))
    print("Target count:", describe(target_counts))

    print("\nLOWER BOUND")
    print(describe(lower_bounds))

    print("\nINITIAL TARGET OVERLAP")
    print("Puzzles with at least one initial target:",
          sum(count > 0 for count in initial_target_counts))
    print("Total initially satisfied targets:",
          sum(initial_target_counts))
    print("Maximum initially satisfied targets:",
          max(initial_target_counts))

    print("\nBY FAMILY")
    for family, values in sorted(family_stats.items()):
        print(
            f"{family:16} "
            f"count={len(values):3} "
            f"{describe(values)}"
        )

    print("\nBY DESIGN TIER")
    for tier, values in sorted(tier_stats.items()):
        print(
            f"{tier:16} "
            f"count={len(values):3} "
            f"{describe(values)}"
        )

    print("\nPUZZLE EXAMPLES")
    for row in puzzles[:5]:
        initial = json.loads(row["starting_values"])
        targets = json.loads(row["targets"])

        print(
            f"{row['id']}: "
            f"family={row['family']}, "
            f"tier={row['design_tier']}, "
            f"initial={initial}, "
            f"targets={len(targets)}, "
            f"lower_bound={row['lower_bound']}"
        )


if __name__ == "__main__":
    main()
