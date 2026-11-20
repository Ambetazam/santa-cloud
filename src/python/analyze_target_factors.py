#!/usr/bin/env python3

import csv
import json
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "practice_puzzles.csv"


def analyze(row):

    initial = json.loads(row["starting_values"])
    targets = set(json.loads(row["targets"]))
    target_list = sorted(targets)

    quotient_relations = []
    target_divisibility = []

    divisor_counts = Counter()

    for target in target_list:

        divisors = [
            value for value in initial
            if target % value == 0
        ]

        divisor_counts.update(divisors)

        for value in divisors:

            quotient = target // value

            quotient_relations.append({
                "target": target,
                "divisor": value,
                "quotient": quotient,
                "quotient_is_target": quotient in targets,
            })

    # Search for target pairs with exact integer ratios.
    ratios = []

    for i, a in enumerate(target_list):
        for b in target_list[i + 1:]:

            if b % a == 0:
                ratios.append((a, b, b // a))

    # GCD of all targets.
    target_gcd = 0

    for target in target_list:
        target_gcd = math.gcd(target_gcd, target)

    print("=" * 76)
    print("TARGET FACTORIZATION ANALYSIS")
    print("=" * 76)

    print("Puzzle:", row["id"])
    print("Family:", row["family"])
    print("Initial values:", initial)
    print("Target count:", len(targets))
    print("Value limit:", row["value_limit"])

    print("\nINITIAL DIVISIBILITY")
    print("-" * 76)

    for value in initial:
        print(
            f"{value:>12}: "
            f"{divisor_counts[value]:>3} targets divisible"
        )

    print("\nTARGET QUOTIENT RELATIONS")
    print("-" * 76)

    for relation in quotient_relations:

        print(
            f"{relation['target']:>18} / "
            f"{relation['divisor']:<4} = "
            f"{relation['quotient']:<18} "
            f"target={relation['quotient_is_target']}"
        )

    print("\nTARGET-TO-TARGET MULTIPLICATIVE RELATIONS")
    print("-" * 76)

    print("Exact integer ratios:", len(ratios))

    for a, b, ratio in ratios[:30]:
        print(f"{b} = {a} * {ratio}")

    print("\nGLOBAL TARGET GCD")
    print("-" * 76)
    print(target_gcd)

    print("\n" + "=" * 76)


def main():

    with DATA_FILE.open(newline="") as f:
        rows = list(csv.DictReader(f))

    selected = [
        row for row in rows
        if row["id"] in {
            "practice_0001",
            "practice_0051",
            "practice_0056",
            "practice_0072",
        }
    ]

    for row in selected:
        analyze(row)


if __name__ == "__main__":
    main()
