
from pathlib import Path
import sys
import json

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validator import load_csv, parse_puzzle, validate_program


ROOT = Path(__file__).resolve().parents[2]
PRACTICE_FILE = ROOT / "data" / "practice_puzzles.csv"

MAX_NODES = 100_000


def find_instruction(target, available, destination, limit):
    """
    Find one valid instruction that generates target.

    available: list of (value, register_index)
    """
    for left, left_reg in available:
        for right, right_reg in available:

            operations = [
                ("+", left + right),
                ("-", left - right),
                ("*", left * right),
            ]

            if right != 0 and left % right == 0:
                operations.append(("/", left // right))

            for operation, result in operations:
                if result == target and 0 < result <= limit:
                    return [
                        operation,
                        left_reg,
                        right_reg,
                        destination,
                    ]

    return None


def search_target_order(puzzle, max_nodes=MAX_NODES):
    """
    Search different orders of target generation.

    Only initial values and target values may be used.
    No non-target intermediates are generated.

    Returns:
        program, missing, statistics
    """

    initial = puzzle["starting_values"]
    targets = set(puzzle["targets"])
    limit = puzzle["value_limit"]

    missing_targets = sorted(targets - set(initial))
    target_count = len(missing_targets)

    if target_count == 0:
        return [], set(), {
            "nodes": 1,
            "exhausted": True,
        }

    # Each bit represents one missing target.
    target_bits = {
        target: index
        for index, target in enumerate(missing_targets)
    }

    full_mask = (1 << target_count) - 1

    failed_states = set()
    nodes = 0
    exhausted = True

    def dfs(mask):
        nonlocal nodes, exhausted

        if mask == full_mask:
            return []

        if mask in failed_states:
            return None

        if nodes >= max_nodes:
            exhausted = False
            return None

        nodes += 1

        available_values = list(initial)

        for target, bit in target_bits.items():
            if mask & (1 << bit):
                available_values.append(target)

        candidates = []

        for target, bit in target_bits.items():
            bit_mask = 1 << bit

            if mask & bit_mask:
                continue

            if can_generate(target, available_values, limit):
                candidates.append(target)

        # Explore each possible next target.
        for target in candidates:
            next_mask = mask | (1 << target_bits[target])

            suffix = dfs(next_mask)

            if suffix is not None:
                return [target] + suffix

            if not exhausted:
                return None

        failed_states.add(mask)
        return None

    def can_generate(target, values, limit):
        for left in values:
            for right in values:
                results = [
                    left + right,
                    left - right,
                    left * right,
                ]

                if right != 0 and left % right == 0:
                    results.append(left // right)

                if target in results and 0 < target <= limit:
                    return True

        return False

    order = dfs(0)

    if order is None:
        return None, set(missing_targets), {
            "nodes": nodes,
            "exhausted": exhausted,
        }

    # Replay the discovered order to assign actual registers.
    available = [
        (value, index)
        for index, value in enumerate(initial)
    ]

    program = []

    for target in order:
        destination = len(initial) + len(program)

        instruction = find_instruction(
            target,
            available,
            destination,
            limit,
        )

        if instruction is None:
            raise RuntimeError(
                f"Could not reconstruct instruction for target {target}"
            )

        program.append(instruction)
        available.append((target, destination))

    return program, set(), {
        "nodes": nodes,
        "exhausted": exhausted,
    }


def main():
    rows = load_csv(PRACTICE_FILE)

    tiny_rows = [
        row for row in rows
        if row["family"] == "tiny"
    ]

    solved = 0
    optimal = 0
    incomplete = 0
    total_nodes = 0

    print("=" * 72)
    print("BOUNDED TARGET-ORDER SEARCH")
    print("=" * 72)

    for row in tiny_rows:
        puzzle = parse_puzzle(row)

        program, missing, stats = search_target_order(puzzle)

        total_nodes += stats["nodes"]

        if program is None:
            incomplete += 1

            status = (
                "SEARCH LIMIT"
                if not stats["exhausted"]
                else "NO TARGET-ONLY SOLUTION"
            )

            print(
                f'{puzzle["id"]:16} '
                f"{status:26} "
                f'nodes={stats["nodes"]}'
            )
            continue

        valid, details = validate_program(puzzle, program)

        if not valid:
            raise RuntimeError(
                f'{puzzle["id"]}: validation failed: {details}'
            )

        lower_bound = len(
            set(puzzle["targets"]) -
            set(puzzle["starting_values"])
        )

        gap = len(program) - lower_bound

        solved += 1

        if gap == 0:
            optimal += 1

        print(
            f'{puzzle["id"]:16} '
            f"instructions={len(program):3} "
            f"lower_bound={lower_bound:3} "
            f"gap={gap:3} "
            f'nodes={stats["nodes"]}'
        )

    print("-" * 72)
    print(f"Tiny puzzles:                 {len(tiny_rows)}")
    print(f"Completed:                    {solved}")
    print(f"Optimal:                      {optimal}")
    print(f"Incomplete:                   {incomplete}")
    print(f"Total search nodes:            {total_nodes}")
    print("=" * 72)


if __name__ == "__main__":
    main()

