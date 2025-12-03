#!/usr/bin/env python3
"""Test the solution with the examples from the puzzle description."""

from solution import find_max_k_digits, solve_puzzle1, solve_puzzle2

# Example data from puzzle description
example_lines = [
    "987654321111111",
    "811111111111119",
    "234234234234278",
    "818181911112111"
]

print("Testing Puzzle 1 (2 digits):")
print("=" * 50)
expected_p1 = [98, 89, 78, 92]
for i, line in enumerate(example_lines):
    result = find_max_k_digits(line, 2)
    status = "PASS" if result == expected_p1[i] else "FAIL"
    print(f"{line} -> {result} (expected {expected_p1[i]}) [{status}]")

total1 = solve_puzzle1(example_lines)
status = "PASS" if total1 == 357 else "FAIL"
print(f"\nTotal: {total1} (expected 357) [{status}]")

print("\n" + "=" * 50)
print("Testing Puzzle 2 (12 digits):")
print("=" * 50)
expected_p2 = [987654321111, 811111111119, 434234234278, 888911112111]
for i, line in enumerate(example_lines):
    result = find_max_k_digits(line, 12)
    status = "PASS" if result == expected_p2[i] else "FAIL"
    print(f"{line} -> {result}")
    print(f"  Expected: {expected_p2[i]} [{status}]")

total2 = solve_puzzle2(example_lines)
expected_total2 = 3121910778619
status = "PASS" if total2 == expected_total2 else "FAIL"
print(f"\nTotal: {total2} (expected {expected_total2}) [{status}]")
