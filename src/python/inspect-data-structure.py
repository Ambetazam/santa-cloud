import csv
import json
from pathlib import Path

path = Path("data/practice_puzzles.csv")

with path.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print("PRACTICE DATASET")
print("Puzzles:", len(rows))
print("Columns:", list(rows[0].keys()))

for row in rows[:5]:
    initial = json.loads(row["starting_values"])
    targets = json.loads(row["targets"])

    print("\nID:", row["id"])
    print("Family:", row["family"])
    print("Initial:", initial)
    print("Targets:", targets[:10], "...")
    print("Value limit:", row["value_limit"])
    print("Registers:", row["registers"])

