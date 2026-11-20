
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validator import load_csv, parse_puzzle, validate_program


ROOT = Path(__file__).resolve().parents[2]
PRACTICE_FILE = ROOT / "data" / "practice_puzzles.csv"

MAX_NODES = 100_000


def reachable_results(values, limit):
    """Return all distinct valid results from pairs of available values."""

    results = set()

    for left in values:
        for right in values:
            candidates = [
                left + right,
                left - right,
                left * right,
            ]

            if right != 0 and left % right == 0:
                candidates.append(left // right)

            for result in candidates:
                if 0 < result <= limit:
                    results.add(result)

    return results


def find_instruction(target, available, destination, limit):
    """Reconstruct one valid instruction producing target."""

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


def search_one_intermediate(puzzle, max_nodes=MAX_NODES):
    """
    Exhaustively search programs using at most one non-target intermediate.

    Targets can be generated in any order.
    The intermediate can be generated at any point.
    """

    initial = puzzle["starting_values"]
    targets = set(puzzle["targets"])
    limit = puzzle["value_limit"]

    missing_targets = sorted(targets - set(initial))

    target_bits = {
        target: index
        for index, target in enumerate(missing_targets)
    }

    full_mask = (1 << len(missing_targets)) - 1

    failed_states = set()
    nodes = 0
    exhausted = True

    def get_values(mask, intermediate):
        values = list(initial)

        for target, bit in target_bits.items():
            if mask & (1 << bit):
                values.append(target)

        if intermediate is not None:
            values.append(intermediate)

        return values

    def dfs(mask, intermediate):
        nonlocal nodes, exhausted

        if mask == full_mask:
            return []

        state = (mask, intermediate)

        if state in failed_states:
            return None

        if nodes >= max_nodes:
            exhausted = False
            return None

        nodes += 1

        available_values = get_values(mask, intermediate)
        reachable = reachable_results(available_values, limit)

        # Option A: generate another missing target.
        candidates = [
            target
            for target in missing_targets
            if not mask & (1 << target_bits[target])
            and target in reachable
        ]

        for target in candidates:
            next_mask = mask | (1 << target_bits[target])

            suffix = dfs(next_mask, intermediate)

            if suffix is not None:
                return [("target", target)] + suffix

            if not exhausted:
                return None

        # Option B: generate one non-target intermediate.
        if intermediate is None:
            intermediate_candidates = sorted(
                reachable - targets - set(initial)
            )

            for value in intermediate_candidates:
                suffix = dfs(mask, value)

                if suffix is not None:
                    return [("intermediate", value)] + suffix

                if not exhausted:
                    return None

        failed_states.add(state)
        return None

    actions = dfs(0, None)

    if actions is None:
        return None, {
            "nodes": nodes,
            "exhausted": exhausted,
        }

    # Reconstruct actual register instructions.
    available = [
        (value, index)
        for index, value in enumerate(initial)
    ]

    program = []
    intermediate_count = 0

    for action_type, value in actions:
        destination = len(initial) + len(program)

        instruction = find_instruction(
            value,
            available,
            destination,
            limit,
        )

        if instruction is None:
            raise RuntimeError(
                f"Could not reconstruct instruction for {value}"
            )

        program.append(instruction)
        available.append((value, destination))

        if action_type == "intermediate":
            intermediate_count += 1

    return program, {
        "nodes": nodes,
        "exhausted": exhausted,
        "intermediates": intermediate_count,
    }


def main():
    rows = load_csv(PRACTICE_FILE)

    tiny_rows = [
        row for row in rows
        if row["family"] == "tiny"
    ]

    solved = 0
    optimal = 0
    with_intermediate = 0
    total_nodes = 0

    print("=" * 78)
    print("ONE-INTERMEDIATE SEARCH")
    print("=" * 78)

    for row in tiny_rows:
        puzzle = parse_puzzle(row)

        program, stats = search_one_intermediate(puzzle)

        total_nodes += stats["nodes"]

        if program is None:
            status = (
                "SEARCH LIMIT"
                if not stats["exhausted"]
                else "NOT SOLVED"
            )

            print(
                f'{puzzle["id"]:16} '
                f"{status:18} "
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
        optimal += int(gap == 0)

        if stats["intermediates"]:
            with_intermediate += 1

        print(
            f'{puzzle["id"]:16} '
            f"instructions={len(program):3} "
            f"intermediates={stats['intermediates']} "
            f"gap={gap:2} "
            f'nodes={stats["nodes"]}'
        )

    print("-" * 78)
    print(f"Tiny puzzles:                  {len(tiny_rows)}")
    print(f"Completed:                     {solved}")
    print(f"Optimal:                       {optimal}")
    print(f"Solutions using intermediate:  {with_intermediate}")
    print(f"Unsolved:                      {len(tiny_rows) - solved}")
    print(f"Total search nodes:             {total_nodes}")
    print("=" * 78)


if __name__ == "__main__":
    main()

