#!/usr/bin/env python3
import sys
import time
from typing import List, Tuple


INPUT_FILE = "input.txt"


def read_input(path: str) -> List[str]:
    """
    Read the input file as a list of rotation instructions, one per line.

    Each line is of the form 'L<number>' or 'R<number>'.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: could not find required input file: {path}", file=sys.stderr)
        sys.exit(1)
    return lines


def solve_puzzle1(rotations: List[str]) -> int:
    """
    Puzzle 1:
    - Dial has positions 0..99.
    - Starts at 50.
    - Each rotation moves the dial by N clicks left (toward lower numbers) or
      right (toward higher numbers), wrapping around modulo 100.
    - Count the number of times the dial is left pointing at 0 *after* a rotation.
    """
    position = 50
    zeros = 0

    for line in rotations:
        direction = line[0]
        distance = int(line[1:])

        if direction == "L":
            position = (position - distance) % 100
        elif direction == "R":
            position = (position + distance) % 100
        else:
            raise ValueError(f"Invalid direction in line: {line}")

        if position == 0:
            zeros += 1

    return zeros


def solve_puzzle2(rotations: List[str]) -> int:
    """
    Puzzle 2 (method 0x434C49434B):
    - Same dial, same starting position (50).
    - For each rotation, we count how many times the dial *passes through or lands on* 0.
      That is, every individual click is considered; if the resulting position after that
      click is 0, we increment the count.
    - Includes cases where the final position of a rotation is 0 as part of the clicks.

    Implementation:
    - For each rotation of N clicks, simulate N single-step moves on a circular dial.
    - This is O(total_clicks). For the given input sizes this is easily fast enough.
    """
    position = 50
    zeros = 0

    for line in rotations:
        direction = line[0]
        distance = int(line[1:])

        if direction == "L":
            step = -1
        elif direction == "R":
            step = 1
        else:
            raise ValueError(f"Invalid direction in line: {line}")

        for _ in range(distance):
            position = (position + step) % 100
            if position == 0:
                zeros += 1

    return zeros


def main() -> None:
    rotations = read_input(INPUT_FILE)

    start_total = time.perf_counter()

    start_p1 = time.perf_counter()
    result1 = solve_puzzle1(rotations)
    end_p1 = time.perf_counter()

    start_p2 = time.perf_counter()
    result2 = solve_puzzle2(rotations)
    end_p2 = time.perf_counter()

    end_total = time.perf_counter()

    # Durations in milliseconds
    dur_p1_ms = (end_p1 - start_p1) * 1000.0
    dur_p2_ms = (end_p2 - start_p2) * 1000.0
    total_ms = (end_total - start_total) * 1000.0

    # Required output format (results only; timings not in the first two lines)
    print(f"Puzzle 1: {result1}")
    print(f"Puzzle 2: {result2}")
    print(f"Total Duration: {total_ms:.3f}ms")

    # If you ever need per-puzzle timings, uncomment:
    # print(f"Puzzle 1 Duration: {dur_p1_ms:.3f}ms", file=sys.stderr)
    # print(f"Puzzle 2 Duration: {dur_p2_ms:.3f}ms", file=sys.stderr)


if __name__ == "__main__":
    main()
