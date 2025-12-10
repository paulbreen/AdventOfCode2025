#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 10: Factory Initialization
Solves both puzzle 1 (indicator lights) and puzzle 2 (joltage counters)
"""

import re
import time
import sys
from typing import List, Tuple
from itertools import product


def parse_machine(line: str) -> Tuple[List[bool], List[List[int]], List[int]]:
    """
    Parse a machine line into lights, buttons, and joltage requirements.

    Returns:
        lights: List of boolean values (True = #, False = .)
        buttons: List of button configurations (each button is a list of indices)
        joltages: List of joltage requirements
    """
    # Extract indicator lights pattern [.##.]
    lights_match = re.search(r'\[([.#]+)\]', line)
    lights = [c == '#' for c in lights_match.group(1)]

    # Extract button configurations (0,1,3)
    buttons = []
    button_matches = re.findall(r'\(([0-9,]+)\)', line)
    for button_str in button_matches:
        indices = [int(x) for x in button_str.split(',')]
        buttons.append(indices)

    # Extract joltage requirements {3,5,4,7}
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    joltages = [int(x) for x in joltage_match.group(1).split(',')]

    return lights, buttons, joltages


def solve_puzzle1_machine(lights: List[bool], buttons: List[List[int]]) -> int:
    """
    Solve Puzzle 1 for a single machine by finding minimum button presses.

    Since pressing a button twice has no effect (XOR twice = original),
    we only need to consider pressing each button 0 or 1 times.
    We try all 2^n combinations and find the one with minimum presses.
    """
    num_lights = len(lights)
    num_buttons = len(buttons)

    # Target configuration (1 = on, 0 = off)
    target = [1 if light else 0 for light in lights]

    # Brute force all combinations (2^n)
    min_presses = float('inf')

    for mask in range(1 << num_buttons):
        # Simulate pressing buttons according to mask
        state = [0] * num_lights
        presses = 0

        for button_idx in range(num_buttons):
            if mask & (1 << button_idx):
                presses += 1
                # Toggle lights affected by this button
                for light_idx in buttons[button_idx]:
                    if light_idx < num_lights:
                        state[light_idx] ^= 1

        # Check if this achieves the target
        if state == target:
            min_presses = min(min_presses, presses)

    return min_presses if min_presses != float('inf') else 0


def solve_puzzle2_machine(joltages: List[int], buttons: List[List[int]]) -> int:
    """
    Solve Puzzle 2 for a single machine by trying different combinations.

    For small problems, we can try a greedy approach or exhaustive search
    for non-basic variable assignments.
    """
    num_counters = len(joltages)
    num_buttons = len(buttons)

    # Build the system matrix A where A[counter][button] = 1 if button affects counter
    A = [[0] * num_buttons for _ in range(num_counters)]
    for button_idx, button in enumerate(buttons):
        for counter_idx in button:
            if counter_idx < num_counters:
                A[counter_idx][button_idx] = 1

    # Try to solve using reduced row echelon form
    augmented = [row[:] + [joltages[i]] for i, row in enumerate(A)]

    # Gaussian elimination to reduced row echelon form
    pivot_row = 0
    pivot_cols = []

    for col in range(num_buttons):
        # Find pivot
        found_pivot = False
        for row in range(pivot_row, num_counters):
            if abs(augmented[row][col]) > 1e-9:
                # Swap rows
                augmented[pivot_row], augmented[row] = augmented[row], augmented[pivot_row]
                found_pivot = True
                break

        if not found_pivot:
            continue

        pivot_cols.append(col)

        # Normalize pivot row
        pivot_val = augmented[pivot_row][col]
        for k in range(len(augmented[pivot_row])):
            augmented[pivot_row][k] /= pivot_val

        # Eliminate column in all other rows
        for row in range(num_counters):
            if row != pivot_row and abs(augmented[row][col]) > 1e-9:
                factor = augmented[row][col]
                for k in range(len(augmented[row])):
                    augmented[row][k] -= factor * augmented[pivot_row][k]

        pivot_row += 1

    # Identify free variables (non-pivot columns)
    free_vars = [i for i in range(num_buttons) if i not in pivot_cols]

    # For small number of free variables, try all assignments
    if len(free_vars) <= 10:
        min_presses = float('inf')

        # Try different values for free variables (0 to max_joltage)
        max_val = max(joltages) if joltages else 0

        def try_assignment(assignment):
            solution = [0] * num_buttons
            # Set free variables
            for i, var_idx in enumerate(free_vars):
                solution[var_idx] = assignment[i]

            # Solve for basic variables
            for row_idx, col_idx in enumerate(pivot_cols):
                if row_idx < len(augmented):
                    value = augmented[row_idx][-1]
                    for k in range(num_buttons):
                        if k != col_idx:
                            value -= augmented[row_idx][k] * solution[k]
                    solution[col_idx] = value

            # Check if solution is valid (all non-negative)
            if all(x >= -1e-9 for x in solution):
                return sum(max(0, round(x)) for x in solution)
            return float('inf')

        # Try small values for free variables
        for max_free in range(min(max_val + 1, 20)):
            for assignment in product(range(max_free + 1), repeat=len(free_vars)):
                presses = try_assignment(assignment)
                min_presses = min(min_presses, presses)

        return int(min_presses) if min_presses != float('inf') else 0

    else:
        # For larger problems, use greedy heuristic: set free variables to 0
        solution = [0] * num_buttons
        for row_idx, col_idx in enumerate(pivot_cols):
            if row_idx < len(augmented):
                solution[col_idx] = max(0, round(augmented[row_idx][-1]))
        return sum(solution)


def main():
    """Main function to solve both puzzles."""
    start_time = time.time()

    # Read input file
    try:
        with open('input.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: input.txt not found", file=sys.stderr)
        sys.exit(1)

    # Parse all machines
    machines = []
    for line in lines:
        lights, buttons, joltages = parse_machine(line)
        machines.append((lights, buttons, joltages))

    # Solve Puzzle 1: Minimum button presses for indicator lights
    puzzle1_total = 0
    for lights, buttons, _ in machines:
        presses = solve_puzzle1_machine(lights, buttons)
        puzzle1_total += presses

    # Solve Puzzle 2: Minimum button presses for joltage counters
    puzzle2_total = 0
    for _, buttons, joltages in machines:
        presses = solve_puzzle2_machine(joltages, buttons)
        puzzle2_total += presses

    end_time = time.time()
    duration_ms = int((end_time - start_time) * 1000)

    # Output results in the required format
    print(f"Puzzle 1: {puzzle1_total}")
    print(f"Puzzle 2: {puzzle2_total}")
    print(f"Total Duration: {duration_ms}ms")


if __name__ == "__main__":
    main()
