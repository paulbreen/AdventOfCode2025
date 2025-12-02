#!/usr/bin/env python3
import sys
import time
from typing import List, Tuple


INPUT_FILE = "input.txt"


def read_ranges(path: str) -> List[Tuple[int, int]]:
    """
    Read the input ranges from the given file.

    The file is expected to contain a single long line (possibly wrapped) of
    comma-separated ranges of the form 'start-end'. For example:

        11-22,95-115,998-1012,...

    Whitespace and newlines are ignored. If a range is written with start > end,
    it is normalized to (min, max).
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
    except FileNotFoundError:
        print(f"Error: could not find required input file: {path}", file=sys.stderr)
        sys.exit(1)

    raw = raw.strip()
    if not raw:
        return []

    # Remove newlines in case the single logical line is wrapped.
    raw = raw.replace("\n", "")
    parts = raw.split(",")

    ranges: List[Tuple[int, int]] = []
    for token in parts:
        token = token.strip()
        if not token:
            continue
        bounds = token.split("-")
        if len(bounds) != 2:
            raise ValueError(f"Invalid range token: {token!r}")
        start = int(bounds[0])
        end = int(bounds[1])
        if start > end:
            start, end = end, start
        ranges.append((start, end))

    if not ranges:
        return []

    return ranges


def merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Merge overlapping or adjacent ranges.

    Input: list of (start, end) with arbitrary order.
    Output: sorted list of non-overlapping, non-adjacent ranges.
    """
    if not ranges:
        return []

    ranges_sorted = sorted(ranges, key=lambda r: r[0])
    merged: List[Tuple[int, int]] = []

    cur_start, cur_end = ranges_sorted[0]
    for s, e in ranges_sorted[1:]:
        if s <= cur_end + 1:
            # Overlapping or touching; merge.
            if e > cur_end:
                cur_end = e
        else:
            merged.append((cur_start, cur_end))
            cur_start, cur_end = s, e

    merged.append((cur_start, cur_end))
    return merged


def generate_repeated_numbers(min_value: int, max_value: int) -> Tuple[List[int], List[int]]:
    """
    Generate all candidate IDs within [min_value, max_value] that are made up of
    a digit-sequence repeated k times (k >= 2).

    Returns:
        (two_rep_only, all_reps)

        - two_rep_only: sorted list of numbers that have at least one
          representation as SOME block repeated exactly 2 times.
          (These are the invalid IDs for Puzzle 1.)

        - all_reps: sorted list of numbers that have at least one representation
          as SOME block repeated k times for k >= 2.
          (These are the invalid IDs for Puzzle 2.)

    Notes:
    - We generate by decimal-length. For a fixed total length L and repeat
      count k, the block length is L / k; we iterate all non-leading-zero
      blocks and replicate them k times.
    - We restrict to the range [min_value, max_value] and deduplicate via sets.
    """
    if min_value > max_value:
        return [], []

    len_min = len(str(min_value))
    len_max = len(str(max_value))

    all_candidates = set()
    two_rep_candidates = set()

    for total_len in range(len_min, len_max + 1):
        # k is the repetition count (>=2)
        for k in range(2, total_len + 1):
            if total_len % k != 0:
                continue

            block_len = total_len // k
            # Block cannot have a leading zero; so first digit is 1-9.
            start_block = 10 ** (block_len - 1)
            end_block = 10 ** block_len - 1

            for block in range(start_block, end_block + 1):
                s = str(block) * k
                # s has length total_len by construction
                n = int(s)

                # Skip those below global range lower bound but continue searching.
                if n < min_value:
                    continue

                # Beyond the max, we can break for this (total_len, k) combination
                # because n grows with block.
                if n > max_value:
                    break

                all_candidates.add(n)
                if k == 2:
                    two_rep_candidates.add(n)

    two_rep_list = sorted(two_rep_candidates)
    all_reps_list = sorted(all_candidates)

    return two_rep_list, all_reps_list


def sum_candidates_in_ranges(
    candidates: List[int],
    ranges: List[Tuple[int, int]],
) -> int:
    """
    Sum all candidate values that lie within any of the given ranges.

    Assumptions:
    - candidates is sorted ascending.
    - ranges is a sorted, non-overlapping list of (start, end) (merged form).
    """
    if not candidates or not ranges:
        return 0

    total = 0
    i = 0
    n_ranges = len(ranges)

    for val in candidates:
        # Advance range index until current range might contain val.
        while i < n_ranges and val > ranges[i][1]:
            i += 1

        if i >= n_ranges:
            break

        if ranges[i][0] <= val <= ranges[i][1]:
            total += val

    return total


def solve_puzzles(ranges: List[Tuple[int, int]]) -> Tuple[int, int]:
    """
    Solve both puzzles:

    - Puzzle 1: IDs that are made of some digit-sequence repeated exactly twice.
    - Puzzle 2: IDs that are made of some digit-sequence repeated at least twice.
    """
    if not ranges:
        return 0, 0

    merged = merge_ranges(ranges)
    global_min = merged[0][0]
    global_max = merged[-1][1]

    # Precompute all repeated-number candidates in the global range.
    two_rep_candidates, all_rep_candidates = generate_repeated_numbers(global_min, global_max)

    # Puzzle 1: sum of all IDs that can be written as some sequence repeated exactly twice.
    p1 = sum_candidates_in_ranges(two_rep_candidates, merged)

    # Puzzle 2: sum of all IDs that can be written as some sequence repeated k times, k >= 2.
    p2 = sum_candidates_in_ranges(all_rep_candidates, merged)

    return p1, p2


def main() -> None:
    start_total = time.perf_counter()

    ranges = read_ranges(INPUT_FILE)
    if not ranges:
        # Degenerate case: no ranges => no invalid IDs.
        print("Puzzle 1: 0")
        print("Puzzle 2: 0")
        total_ms = (time.perf_counter() - start_total) * 1000.0
        print(f"Total Duration: {total_ms:.3f}ms")
        return

    # Time both puzzles (internally shared work is done once).
    start_puzzles = time.perf_counter()
    result1, result2 = solve_puzzles(ranges)
    end_puzzles = time.perf_counter()

    end_total = time.perf_counter()

    # Durations (ms) – not required in the main output format except for total.
    puzzles_ms = (end_puzzles - start_puzzles) * 1000.0
    total_ms = (end_total - start_total) * 1000.0

    # Required output format
    print(f"Puzzle 1: {result1}")
    print(f"Puzzle 2: {result2}")
    print(f"Total Duration: {total_ms:.3f}ms")

    # If you want per-puzzle timing details, uncomment these (stderr / logging).
    # print(f"Puzzles Duration (including shared enumeration): {puzzles_ms:.3f}ms", file=sys.stderr)


if __name__ == "__main__":
    main()
