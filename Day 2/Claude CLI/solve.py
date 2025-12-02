#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 2: Gift Shop
Identifies invalid product IDs based on repeating digit patterns.
"""

import sys
import time
import os


def is_invalid_puzzle1(num_str):
    """
    Check if a number is invalid for Puzzle 1.
    Invalid = sequence of digits repeated exactly twice.
    Examples: 55, 6464, 123123
    """
    length = len(num_str)

    # Must have even length to be split in half
    if length % 2 != 0:
        return False

    # Check if first half equals second half
    mid = length // 2
    return num_str[:mid] == num_str[mid:]


def is_invalid_puzzle2(num_str):
    """
    Check if a number is invalid for Puzzle 2.
    Invalid = sequence of digits repeated at least twice.
    Examples: 12341234, 123123123, 1212121212, 1111111
    """
    length = len(num_str)

    # Try all possible pattern lengths (from 1 to length//2)
    for pattern_len in range(1, length // 2 + 1):
        # Pattern must divide evenly into the total length
        if length % pattern_len == 0:
            pattern = num_str[:pattern_len]
            repeat_count = length // pattern_len

            # Check if repeating this pattern recreates the original number
            if pattern * repeat_count == num_str:
                return True

    return False


def parse_ranges(input_text):
    """
    Parse comma-separated ranges from input text.
    Returns list of (start, end) tuples.
    """
    # Remove whitespace and split by commas
    ranges_text = input_text.strip().replace('\n', '').replace(' ', '')
    range_parts = ranges_text.split(',')

    ranges = []
    for part in range_parts:
        if '-' in part:
            start, end = part.split('-')
            ranges.append((int(start), int(end)))

    return ranges


def solve_puzzle1(ranges):
    """
    Find all invalid IDs in ranges using Puzzle 1 rules.
    Returns the sum of all invalid IDs.
    """
    total = 0

    for start, end in ranges:
        for num in range(start, end + 1):
            num_str = str(num)
            if is_invalid_puzzle1(num_str):
                total += num

    return total


def solve_puzzle2(ranges):
    """
    Find all invalid IDs in ranges using Puzzle 2 rules.
    Returns the sum of all invalid IDs.
    """
    total = 0

    for start, end in ranges:
        for num in range(start, end + 1):
            num_str = str(num)
            if is_invalid_puzzle2(num_str):
                total += num

    return total


def main():
    # Check if input file exists
    input_file = 'input.txt'
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!", file=sys.stderr)
        sys.exit(1)

    # Read input data
    try:
        with open(input_file, 'r') as f:
            input_text = f.read()
    except Exception as e:
        print(f"Error reading {input_file}: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse ranges
    ranges = parse_ranges(input_text)

    # Start timing
    start_time = time.perf_counter()

    # Solve both puzzles
    result1 = solve_puzzle1(ranges)
    result2 = solve_puzzle2(ranges)

    # End timing
    end_time = time.perf_counter()
    duration_ms = (end_time - start_time) * 1000

    # Display results in required format
    print(f"Puzzle 1: {result1}")
    print(f"Puzzle 2: {result2}")
    print(f"Total Duration: {duration_ms:.2f}ms")


if __name__ == "__main__":
    main()
