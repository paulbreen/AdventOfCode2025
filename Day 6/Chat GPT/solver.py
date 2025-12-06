# solver.py
#
# Solves both cephalopod math puzzles described in:
# - puzzle1.txt (Part One) :contentReference[oaicite:0]{index=0}
# - puzzle2.txt (Part Two) :contentReference[oaicite:1]{index=1}
#
# using the worksheet in input.txt :contentReference[oaicite:2]{index=2}
#
# Usage:
#   python solver.py
#
# Expected output format:
#   Puzzle 1: [result]
#   Puzzle 2: [result]
#   Total Duration: [time]ms

import sys
import time
from math import prod
from typing import List, Tuple


def read_input(path: str) -> List[str]:
    """
    Read the worksheet file as raw lines, preserving all spaces except trailing newlines.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.rstrip("\n") for line in f]
    except FileNotFoundError:
        print(f"Error: {path} not found.", file=sys.stderr)
        sys.exit(1)


def pad_lines(lines: List[str]) -> List[str]:
    """
    Right-pad all lines with spaces to the same width so that column indexing is safe.
    """
    if not lines:
        return lines
    width = max(len(line) for line in lines)
    return [line.ljust(width) for line in lines]


def find_problem_blocks(lines: List[str]) -> List[Tuple[int, int]]:
    """
    Identify horizontal problem blocks.

    A problem block is a maximal contiguous range of columns [start, end)
    where NOT all rows (including operator row) are spaces.

    Columns where every row is a space are separators between problems.
    """
    if not lines:
        return []

    num_rows = len(lines) - 1  # last row is the operator row
    width = len(lines[0])
    blocks: List[Tuple[int, int]] = []

    c = 0
    while c < width:
        # Column of all spaces across all rows -> separator
        if all(lines[r][c] == " " for r in range(num_rows + 1)):
            c += 1
            continue

        # Start of a problem block
        start = c
        c += 1
        while c < width and not all(lines[r][c] == " " for r in range(num_rows + 1)):
            c += 1
        end = c
        blocks.append((start, end))

    return blocks


def get_operator(lines: List[str], block: Tuple[int, int]) -> str:
    """
    Extract the operator ('+' or '*') for a problem block from the operator row.

    We look at the bottom row in the block and collect all non-space operator
    characters. They are expected to all be the same.
    """
    num_rows = len(lines) - 1
    start, end = block

    ops = {ch for ch in lines[num_rows][start:end] if ch in "+*"}
    if not ops:
        raise ValueError(f"No operator found in block columns {start}-{end}.")
    if len(ops) > 1:
        # Defensive: if malformed, pick one deterministically.
        # Under valid input, this should not happen.
        op = sorted(ops)[0]
    else:
        op = ops.pop()
    return op


def solve_puzzle1(lines: List[str]) -> int:
    """
    Part One: Each problem's numbers are arranged vertically; at the bottom
    of each problem is the symbol for the operation to apply. :contentReference[oaicite:3]{index=3}

    For each problem block:
      - Each non-empty (after stripping spaces) substring in the numeric rows
        is a full integer for that row.
      - Apply the block's operator (+ or *) across all those numbers.
    Finally, return the sum of all problem results.
    """
    lines = pad_lines(lines)
    blocks = find_problem_blocks(lines)
    num_rows = len(lines) - 1  # numeric rows only

    grand_total = 0

    for block in blocks:
        start, end = block
        op = get_operator(lines, block)

        numbers: List[int] = []
        for r in range(num_rows):
            chunk = lines[r][start:end]
            text = chunk.strip()
            if text:
                # Entire row chunk is one integer
                numbers.append(int(text))

        if not numbers:
            # Under valid input, each problem has at least one number.
            continue

        if op == "+":
            grand_total += sum(numbers)
        else:
            grand_total += prod(numbers)

    return grand_total


def solve_puzzle2(lines: List[str]) -> int:
    """
    Part Two: Cephalopod math is written right-to-left in columns. :contentReference[oaicite:4]{index=4}

    For each problem block:
      - Ignore the operator row (bottom).
      - Consider each column in the block (from right to left):
          * Collect all digit characters in that column from top to bottom.
          * If any digits are present, that top-to-bottom sequence defines one integer.
        (Columns with only spaces are ignored; the operator column usually has no digits.)
      - Apply the block's operator (+ or *) across all such column-numbers.
    Finally, return the sum of all problem results.
    """
    lines = pad_lines(lines)
    blocks = find_problem_blocks(lines)
    num_rows = len(lines) - 1  # numeric rows only

    grand_total = 0

    for block in blocks:
        start, end = block
        op = get_operator(lines, block)

        column_numbers: List[int] = []

        # Read right-to-left as described; order is irrelevant for +/* but we follow spec.
        for c in range(end - 1, start - 1, -1):
            digits: List[str] = []
            for r in range(num_rows):
                ch = lines[r][c]
                if ch.isdigit():
                    digits.append(ch)

            if digits:
                # Digits are in most-significant (top) to least-significant (bottom) order.
                column_numbers.append(int("".join(digits)))

        if not column_numbers:
            # Under valid input, there should be at least one number per problem.
            continue

        if op == "+":
            grand_total += sum(column_numbers)
        else:
            grand_total += prod(column_numbers)

    return grand_total


def main() -> None:
    lines = read_input("input.txt")

    # Time each puzzle solution separately.
    t1_start = time.perf_counter()
    result1 = solve_puzzle1(lines)
    t1_end = time.perf_counter()

    t2_start = time.perf_counter()
    result2 = solve_puzzle2(lines)
    t2_end = time.perf_counter()

    duration1_ms = (t1_end - t1_start) * 1000.0
    duration2_ms = (t2_end - t2_start) * 1000.0
    total_ms = duration1_ms + duration2_ms

    # Required output format
    print(f"Puzzle 1: {result1}")
    print(f"Puzzle 2: {result2}")
    print(f"Total Duration: {total_ms:.3f}ms")


if __name__ == "__main__":
    main()
