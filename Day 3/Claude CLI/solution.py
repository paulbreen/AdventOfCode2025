#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 3: Lobby
Solution for finding maximum joltage from battery banks.
"""

import time


def find_max_k_digits(digits_str, k):
    """
    Find the maximum k-digit number by selecting k digits from the input string
    while maintaining their relative order.

    Uses a greedy algorithm with monotonic stack:
    - We need to remove (n - k) digits to keep k digits
    - Build result by keeping larger digits and removing smaller ones when possible

    Args:
        digits_str: String of digits
        k: Number of digits to select

    Returns:
        Integer representing the maximum k-digit number
    """
    n = len(digits_str)
    if k >= n:
        return int(digits_str)

    to_remove = n - k
    stack = []

    for digit in digits_str:
        # While we can still remove digits and current digit is larger than stack top
        while stack and to_remove > 0 and stack[-1] < digit:
            stack.pop()
            to_remove -= 1
        stack.append(digit)

    # If we still need to remove digits, remove from the end
    # (these are the smallest remaining digits)
    result = ''.join(stack[:k])
    return int(result)


def solve_puzzle1(lines):
    """
    Puzzle 1: Find maximum 2-digit number from each bank and sum them.

    Args:
        lines: List of digit strings (battery banks)

    Returns:
        Total joltage from all banks
    """
    total = 0
    for line in lines:
        max_joltage = find_max_k_digits(line, 2)
        total += max_joltage
    return total


def solve_puzzle2(lines):
    """
    Puzzle 2: Find maximum 12-digit number from each bank and sum them.

    Args:
        lines: List of digit strings (battery banks)

    Returns:
        Total joltage from all banks
    """
    total = 0
    for line in lines:
        max_joltage = find_max_k_digits(line, 12)
        total += max_joltage
    return total


def main():
    """Main execution function."""
    try:
        # Read input file
        with open('input.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        # Start timing
        start_time = time.time()

        # Solve both puzzles
        result1 = solve_puzzle1(lines)
        result2 = solve_puzzle2(lines)

        # Calculate total duration
        duration_ms = (time.time() - start_time) * 1000

        # Display results in required format
        print(f"Puzzle 1: {result1}")
        print(f"Puzzle 2: {result2}")
        print(f"Total Duration: {duration_ms:.2f}ms")

    except FileNotFoundError:
        print("Error: input.txt file not found")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
