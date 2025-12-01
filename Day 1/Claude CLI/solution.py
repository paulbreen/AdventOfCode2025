#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 1: Secret Entrance
Solves both puzzles involving a circular dial safe mechanism.
"""

import time
from pathlib import Path


def parse_rotation(line):
    """Parse a rotation line like 'L68' or 'R43' into direction and distance."""
    direction = line[0]
    distance = int(line[1:])
    return direction, distance


def solve_puzzle_one(rotations):
    """
    Puzzle 1: Count how many times the dial points at 0 after completing a rotation.
    """
    position = 50
    zero_count = 0

    for direction, distance in rotations:
        if direction == 'L':
            position = (position - distance) % 100
        else:  # R
            position = (position + distance) % 100

        if position == 0:
            zero_count += 1

    return zero_count


def solve_puzzle_two(rotations):
    """
    Puzzle 2: Count how many times the dial points at 0 during any rotation,
    including intermediate positions and final positions.
    """
    position = 50
    zero_count = 0

    for direction, distance in rotations:
        # Count how many times we pass through 0 during this rotation
        if direction == 'L':
            # Moving left (toward lower numbers)
            for _ in range(distance):
                position = (position - 1) % 100
                if position == 0:
                    zero_count += 1
        else:  # R
            # Moving right (toward higher numbers)
            for _ in range(distance):
                position = (position + 1) % 100
                if position == 0:
                    zero_count += 1

    return zero_count


def main():
    # Read input file
    script_dir = Path(__file__).parent
    input_path = script_dir.parent / "Instructions" / "input.txt"

    try:
        with open(input_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Could not find input file at {input_path}")
        return

    # Parse all rotations
    rotations = [parse_rotation(line) for line in lines]

    # Start timing
    start_time = time.time()

    # Solve both puzzles
    result1 = solve_puzzle_one(rotations)
    result2 = solve_puzzle_two(rotations)

    # Calculate duration
    duration_ms = (time.time() - start_time) * 1000

    # Output results in the specified format
    print(f"Puzzle 1: {result1}")
    print(f"Puzzle 2: {result2}")
    print(f"Total Duration: {duration_ms:.2f}ms")


if __name__ == "__main__":
    main()
