#This should give us the sample submission's total instruction count, average program length, operation distribution, and the puzzle complexity distribution.

import csv
import json
import statistics
from collections import Counter
from pathlib import Path

DATA = Path("data")

def read_csv(filename):
    with (DATA / filename).open(
        newline="", encoding="utf-8"
    ) as f:
        return list(csv.DictReader(f))

puzzles = read_csv("puzzles.csv")
practice = read_csv("practice_puzzles.csv")
submission = read_csv("sample_submission.csv")

print("=" * 65)
print("DATASET DIMENSIONS")
print("=" * 65)

for name, rows in [
    ("Scored puzzles", puzzles),
    ("Practice puzzles", practice),
    ("Sample submission", submission),
]:
    print(f"{name:22}: {len(rows):,} rows")

print("\n" + "=" * 65)
print("PRACTICE DATASET METADATA")
print("=" * 65)

print("Families:")
print(Counter(row["family"] for row in practice))

print("\nDesign tiers:")
print(Counter(row["design_tier"] for row in practice))

print("\nLower-bound distribution:")
bounds = [int(row["lower_bound"]) for row in practice]
print("Minimum:", min(bounds))
print("Maximum:", max(bounds))
print("Mean:", round(statistics.mean(bounds), 2))

print("\n" + "=" * 65)
print("SAMPLE SUBMISSION ANALYSIS")
print("=" * 65)

instruction_counts = []
operation_counts = Counter()
program_bytes = []

for row in submission:
    program = json.loads(row["program"])

    instruction_counts.append(len(program))
    program_bytes.append(len(row["program"].encode("utf-8")))

    for instruction in program:
        operation_counts[instruction[0]] += 1

print("Total instructions:", f"{sum(instruction_counts):,}")
print("Mean instructions:", round(statistics.mean(instruction_counts), 2))
print("Minimum instructions:", min(instruction_counts))
print("Maximum instructions:", max(instruction_counts))
print("Operation distribution:", operation_counts)
print("Largest program:", f"{max(program_bytes):,} bytes")

print("\n" + "=" * 65)
print("PUZZLE STRUCTURE")
print("=" * 65)

initial_counts = Counter(
    len(json.loads(row["starting_values"]))
    for row in puzzles
)

target_counts = [
    len(json.loads(row["targets"]))
    for row in puzzles
]

print("Initial register count distribution:", initial_counts)
print("Targets per puzzle:")
print("  Minimum:", min(target_counts))
print("  Maximum:", max(target_counts))
print("  Mean:", round(statistics.mean(target_counts), 2))

print("\nFirst scored puzzle:")
first = puzzles[0]

for key, value in first.items():
    if key in ("starting_values", "targets"):
        parsed = json.loads(value)
        print(f"{key}: {len(parsed)} values")
        print("  First 10:", parsed[:10])
    else:
        print(f"{key}: {value}")
