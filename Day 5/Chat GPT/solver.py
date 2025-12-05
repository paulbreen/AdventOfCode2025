#!/usr/bin/env python3
"""
Solver for Cafeteria puzzles (Day 5).

Puzzle 1: Count how many available ingredient IDs fall in any fresh interval.
Puzzle 2: Count total unique IDs covered by the union of all fresh intervals.

Input: input.txt
"""

import sys
import time
from pathlib import Path
from bisect import bisect_right
from typing import List, Tuple

INPUT_FILE = "input.txt"
Interval = Tuple[int, int]


def parse_input(path: Path) -> Tuple[List[Interval], List[int]]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        sys.stderr.write(f"Error: input file not found: {path}\n")
        sys.exit(1)

    lines = text.splitlines()

    try:
        split_idx = lines.index("")
    except ValueError:
        sys.stderr.write("Error: input missing blank line separator.\n")
        sys.exit(1)

    range_lines = lines[:split_idx]
    id_lines = lines[split_idx + 1 :]

    ranges: List[Interval] = []
    for line in range_lines:
        line = line.strip()
        if not line:
            continue
        if "-" not in line:
            sys.stderr.write(f"Error: invalid range line: {line!r}\n")
            sys.exit(1)
        s, e = line.split("-", 1)
        try:
            start = int(s)
            end = int(e)
        except ValueError:
            sys.stderr.write(f"Error: invalid integer in range line: {line!r}\n")
            sys.exit(1)
        if end < start:
            sys.stderr.write(f"Error: range end < start: {line!r}\n")
            sys.exit(1)
        ranges.append((start, end))

    ids: List[int] = []
    for line in id_lines:
        line = line.strip()
        if not line:
            continue
        try:
            ids.append(int(line))
        except ValueError:
            sys.stderr.write(f"Error: invalid ID line: {line!r}\n")
            sys.exit(1)

    return ranges, ids


def merge_intervals(intervals: List[Interval]) -> List[Interval]:
    if not intervals:
        return []

    intervals = sorted(intervals, key=lambda x: x[0])
    merged: List[Interval] = []

    cur_start, cur_end = intervals[0]
    for start, end in intervals[1:]:
        if start <= cur_end + 1:
            cur_end = max(cur_end, end)
        else:
            merged.append((cur_start, cur_end))
            cur_start, cur_end = start, end

    merged.append((cur_start, cur_end))
    return merged


def solve_puzzle1(merged: List[Interval], ids: List[int]) -> int:
    starts = [s for s, _ in merged]

    def in_any(x: int) -> bool:
        idx = bisect_right(starts, x) - 1
        if idx < 0:
            return False
        s, e = merged[idx]
        return s <= x <= e

    return sum(1 for v in ids if in_any(v))


def solve_puzzle2(merged: List[Interval]) -> int:
    return sum((end - start + 1) for start, end in merged)


def main() -> None:
    input_path = Path(INPUT_FILE)

    # -------------------------------
    #   Total duration start (µs)
    # -------------------------------
    total_start = time.perf_counter()

    ranges, ids = parse_input(input_path)
    merged = merge_intervals(ranges)

    # Puzzle 1 timing (µs)
    p1_start = time.perf_counter()
    result1 = solve_puzzle1(merged, ids)
    p1_end = time.perf_counter()
    duration1_us = int((p1_end - p1_start) * 1_000_000)

    # Puzzle 2 timing (µs)
    p2_start = time.perf_counter()
    result2 = solve_puzzle2(merged)
    p2_end = time.perf_counter()
    duration2_us = int((p2_end - p2_start) * 1_000_000)

    # Total duration (parse + merge + both puzzles)
    total_end = time.perf_counter()
    total_duration_us = int((total_end - total_start) * 1_000_000)

    # Output format (units changed to µs)
    print(f"Puzzle 1: {result1}")
    print(f"Puzzle 2: {result2}")
    print(f"Total Duration: {total_duration_us}µs")


if __name__ == "__main__":
    main()
