#!/usr/bin/env python3

from collections import defaultdict
from pathlib import Path

from validator import load_csv, parse_puzzle


ROOT = Path(__file__).resolve().parents[2]
PRACTICE_FILE = ROOT / "data" / "practice_puzzles.csv"


def arithmetic_results(a, b, limit):
    """Yield valid positive results from the four permitted operations."""

    candidates = [
        ("+", a + b),
        ("-", a - b),
        ("*", a * b),
    ]

    if b != 0 and a % b == 0:
        candidates.append(("/", a // b))

    for operation, result in candidates:
        if 0 < result <= limit:
            yield operation, result


def generate_intermediates(initial, targets, limit):
    """
    Generate all distinct non-target values obtainable
    from two initial registers in one instruction.
    """

    intermediates = {}

    for i, a in enumerate(initial):
        for j, b in enumerate(initial):

            for operation, result in arithmetic_results(a, b, limit):

                if result in initial:
                    continue

                if result in targets:
                    continue

                intermediates.setdefault(
                    result,
                    (operation, i, j),
                )

    return intermediates


def can_generate(target, values):
    """Check whether one operation on two available values makes target."""

    for a in values:
        for b in values:

            if a + b == target:
                return True

            if a - b == target:
                return True

            if a * b == target:
                return True

            if b != 0 and a % b == 0 and a // b == target:
                return True

    return False


def analyze_puzzle(puzzle):

    initial = puzzle["starting_values"]
    targets = set(puzzle["targets"])
    limit = puzzle["value_limit"]

    direct = {
        target
        for target in targets
        if can_generate(target, initial)
    }

    missing = targets - set(initial)
    intermediates = generate_intermediates(
        initial,
        targets,
        limit,
    )

    union_reachable = set(direct)
    best_intermediate = None
    best_coverage = set(direct)

    for intermediate in intermediates:

        available = initial + [intermediate]

        reachable = {
            target
            for target in missing
            if can_generate(target, available)
        }

        union_reachable.update(reachable)

       newly_reachable = reachable - direct
       best_newly_reachable = best_coverage - direct

       if len(newly_reachable) > len(best_newly_reachable):
            best_coverage = direct | reachable
            best_intermediate = intermediate

	#if len(reachable) > len(best_coverage - direct):
        #    best_coverage = direct | reachable
        #    best_intermediate = intermediate

    return {
        "direct": len(direct & missing),
        "missing": len(missing),
        "intermediates": len(intermediates),
        "union": len(union_reachable & missing),
        "best": len(best_coverage & missing),
        "best_value": best_intermediate,
    }


def main():

    rows = load_csv(PRACTICE_FILE)

    family_stats = defaultdict(
        lambda: {
            "puzzles": 0,
            "missing": 0,
            "direct": 0,
            "union": 0,
            "best": 0,
            "intermediates": 0,
        }
    )

    results = []

    for row in rows:

        puzzle = parse_puzzle(row)
        result = analyze_puzzle(puzzle)
        family = row["family"]

        stats = family_stats[family]
        stats["puzzles"] += 1

        for key in (
            "missing",
            "direct",
            "union",
            "best",
            "intermediates",
        ):
            stats[key] += result[key]

        results.append({
            "id": puzzle["id"],
            "family": family,
            **result,
        })

    total_missing = sum(r["missing"] for r in results)
    total_direct = sum(r["direct"] for r in results)
    total_union = sum(r["union"] for r in results)

    print("=" * 76)
    print("ONE-INTERMEDIATE REACHABILITY ANALYSIS")
    print("=" * 76)

    print(f"Practice puzzles:                  {len(rows)}")
    print(f"Missing targets:                   {total_missing:,}")
    print(f"Directly reachable targets:        {total_direct:,}")
    print(f"Reachable with some intermediate:  {total_union:,}")

    print(
        "Individual reachability coverage: "
        f"{100 * total_union / total_missing:.2f}%"
    )

    print("\nBY FAMILY")
    print("-" * 76)

    for family in sorted(family_stats):

        s = family_stats[family]

        coverage = (
            100 * s["union"] / s["missing"]
            if s["missing"] else 100
        )

        print(
            f"{family:16}"
            f"puzzles={s['puzzles']:3}  "
            f"direct={s['direct']:4}  "
            f"one-intermediate union={s['union']:4}  "
            f"best-per-puzzle={s['best']:4}  "
            f"coverage={coverage:6.2f}%"
        )

    print("\nMOST PROMISING PUZZLES")
    print("-" * 76)

    ranked = sorted(
        results,
        key=lambda r: (
            r["best"],
            r["union"],
        ),
        reverse=True,
    )

    for r in ranked[:15]:

        print(
            f"{r['id']} | {r['family']:14} | "
            f"missing={r['missing']:2} | "
            f"direct={r['direct']:2} | "
            f"union={r['union']:2} | "
            f"best={r['best']:2} | "
            f"candidates={r['intermediates']:4} | "
            f"best_value={r['best_value']}"
        )

    print("\n" + "=" * 76)
    print("ANALYSIS COMPLETE")
    print("=" * 76)


if __name__ == "__main__":
    main()
