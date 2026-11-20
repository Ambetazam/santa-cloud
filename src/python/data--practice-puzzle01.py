python - <<'PY'
import csv
import json
from pathlib import Path

path = Path("data/practice_puzzles.csv")

with path.open(newline="") as f:
    rows = csv.DictReader(f)

    for row in rows:
        if row["id"] == "practice_0001":
            initial = json.loads(row["starting_values"])
            targets = json.loads(row["targets"])

            print("Initial values:", initial)
            print("Targets:", len(targets))
            print("Value limit:", row["value_limit"])
            print("\nTarget factorization clues:")

            for target in targets[:10]:
                print(f"{target:>18} | divisible by initial values:", [
                    x for x in initial if target % x == 0
                ])

            break
PY
