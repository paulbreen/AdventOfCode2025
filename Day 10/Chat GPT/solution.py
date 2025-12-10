#!/usr/bin/env python3
"""
Day 10: Factory – Puzzle Solver

This script solves both parts of the "Factory" puzzle using the
indicator/button/joltage format described in puzzle1.txt and puzzle2.txt.

It reads a single input file (default: input.txt) where each line has the form:

    [pattern] (i,j,...) (k,...) ... {t0,t1,...}

- pattern: '.' and '#' characters for indicator lights (used only in Puzzle 1)
- parenthesis groups: button wiring schematics (indices of lights / counters)
- curly braces: target joltage levels (used only in Puzzle 2)
"""

from __future__ import annotations

import sys
import re
import time
from fractions import Fraction
from pathlib import Path
from typing import List, Tuple


Machine = Tuple[str, List[List[int]], List[int]]  # (pattern, buttons, jolts)


def parse_line(line: str) -> Machine:
    """
    Parse a single machine description line.

    Example:
        "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
    """
    line = line.strip()
    if not line:
        raise ValueError("Empty line in input")

    m_br = re.search(r"\[([.#]+)\]", line)
    if not m_br:
        raise ValueError(f"Missing indicator light diagram [] in line: {line}")
    pattern = m_br.group(1)

    # Extract all button wiring schematics
    buttons: List[List[int]] = []
    for group in re.findall(r"\(([0-9,]+)\)", line):
        idxs = [int(x) for x in group.split(",") if x != ""]
        if not idxs:
            raise ValueError(f"Empty button definition in line: {line}")
        buttons.append(idxs)

    # Extract joltage requirements
    m_curly = re.search(r"\{([0-9,]+)\}", line)
    if not m_curly:
        raise ValueError(f"Missing joltage requirements {{}} in line: {line}")
    jolts = [int(x) for x in m_curly.group(1).split(",") if x != ""]

    return pattern, buttons, jolts


def load_input(path: Path) -> List[Machine]:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    machines: List[Machine] = []
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            machines.append(parse_line(raw))
    if not machines:
        raise ValueError("Input file contained no machine descriptions")
    return machines


# ---------------------------------------------------------------------------
# Puzzle 1: Lights – minimum button presses with toggling (mod 2)
# ---------------------------------------------------------------------------

def min_presses_lights(pattern: str, buttons: List[List[int]]) -> int:
    """
    Given an indicator pattern and button wiring, compute the minimum number of
    button presses required to reach the pattern from all-off.

    Each button toggles the listed bits; we treat this as solving A x = b over
    GF(2) and search for the minimum Hamming-weight solution using DFS with
    pruning. For these input sizes, a simple DFS is sufficient.
    """
    num_lights = len(pattern)

    # Convert pattern to target bitmask
    target_mask = 0
    for i, ch in enumerate(pattern):
        if ch == "#":
            target_mask |= 1 << i

    # Precompute button bitmasks
    masks: List[int] = []
    for idxs in buttons:
        mask = 0
        for i in idxs:
            if not (0 <= i < num_lights):
                raise ValueError(
                    f"Button index {i} out of range for {num_lights} lights"
                )
            mask |= 1 << i
        masks.append(mask)

    best = [float("inf")]
    m = len(masks)

    def dfs(i: int, cur_mask: int, presses: int) -> None:
        # Prune if we already used at least as many presses as best
        if presses >= best[0]:
            return
        if i == m:
            if cur_mask == target_mask:
                best[0] = presses
            return
        # Option 1: skip button i
        dfs(i + 1, cur_mask, presses)
        # Option 2: press button i once
        dfs(i + 1, cur_mask ^ masks[i], presses + 1)

    dfs(0, 0, 0)
    if best[0] == float("inf"):
        # Per puzzle statement, all machines are solvable; reaching here
        # would indicate malformed input.
        raise RuntimeError("No solution found for indicator lights")
    return int(best[0])


def solve_puzzle1(machines: List[Machine]) -> int:
    total = 0
    for pattern, buttons, _jolts in machines:
        total += min_presses_lights(pattern, buttons)
    return total


# ---------------------------------------------------------------------------
# Puzzle 2: Joltage – minimum button presses with integer counters
# ---------------------------------------------------------------------------

def rref(A: List[List[int]], b: List[int]):
    """
    Compute Reduced Row Echelon Form (RREF) of the augmented matrix [A | b]
    over the rationals (using Fraction for exact arithmetic).

    Returns:
        M: augmented matrix in RREF, shape (n_rows, n_cols+1)
        pivot_cols: list of pivot column indices
        pivot_row_for_col: dict mapping pivot column -> row index
        all_cols: list(range(num_cols))
    """
    n = len(A)
    if n == 0:
        return [], [], {}, list(range(0))
    m = len(A[0])
    # Build augmented matrix with Fractions
    M = [[Fraction(A[i][j]) for j in range(m)] + [Fraction(b[i])] for i in range(n)]

    pivot_cols: List[int] = []
    pivot_row_for_col = {}
    row = 0

    for col in range(m):
        # Find a pivot row at or below the current row
        pivot_row = None
        for r in range(row, n):
            if M[r][col] != 0:
                pivot_row = r
                break
        if pivot_row is None:
            continue

        # Move pivot row into position
        if pivot_row != row:
            M[row], M[pivot_row] = M[pivot_row], M[row]

        # Scale pivot row to make the pivot equal to 1
        factor = M[row][col]
        if factor != 1:
            for c in range(col, m + 1):
                M[row][c] /= factor

        # Eliminate this column from all other rows
        for r in range(n):
            if r != row and M[r][col] != 0:
                factor = M[r][col]
                if factor != 0:
                    for c in range(col, m + 1):
                        M[r][c] -= factor * M[row][c]

        pivot_cols.append(col)
        pivot_row_for_col[col] = row
        row += 1
        if row == n:
            break

    # Check for inconsistency: 0 ... 0 | nonzero
    for r in range(n):
        if all(M[r][c] == 0 for c in range(m)) and M[r][m] != 0:
            raise ValueError("Inconsistent linear system for joltage counters")

    return M, pivot_cols, pivot_row_for_col, list(range(m))


def min_presses_jolts(buttons: List[List[int]], jolts: List[int]) -> int:
    """
    Solve the integer system:

        A x = t,  x >= 0, minimize sum_j x_j

    where:
      - rows of A correspond to counters,
      - columns of A correspond to buttons,
      - A[i][j] = 1 if button j increments counter i.

    Strategy:
      1. Build A (0/1 matrix) from button wiring.
      2. Compute RREF of [A | t] over the rationals.
      3. Identify pivot and free variables and express pivot variables as
         affine functions of the free variables.
      4. Enumerate all non-negative integer assignments for the free variables
         within safe upper bounds (derived from the original constraints).
      5. For each assignment, derive pivot variables, check integrality and
         non-negativity, and keep the feasible solution with minimum total
         presses.

    For this specific puzzle input, the number of free variables per machine
    is small (at most 3), so this bounded enumeration is tractable.
    """
    n = len(jolts)
    m = len(buttons)

    # Build A as n x m matrix
    A: List[List[int]] = []
    for i in range(n):
        row = []
        for idxs in buttons:
            row.append(1 if i in idxs else 0)
        A.append(row)

    # Per-column upper bounds: for each button j, x_j cannot exceed the
    # smallest target among the counters it increments.
    ub = [0] * m
    for j in range(m):
        rows = [i for i in range(n) if A[i][j] == 1]
        if not rows:
            # Button affects no counters; optimal solution never presses it.
            ub[j] = 0
        else:
            ub[j] = min(jolts[i] for i in rows)

    # RREF decomposition
    M, pivot_cols, pivot_row_for_col, all_cols = rref(A, jolts)
    free_cols = [c for c in all_cols if c not in pivot_cols]
    num_free = len(free_cols)

    # Express each pivot variable as:
    #   x_c = const_c + sum_{f in free_cols} coeffs_c[f] * x_f
    const = {}
    coeffs = {}
    num_cols = len(all_cols)
    for c in pivot_cols:
        r = pivot_row_for_col[c]
        const_c = M[r][num_cols]  # RHS
        coeffs_c = {}
        for fc in free_cols:
            val = M[r][fc]
            if val != 0:
                # Move term to right-hand side
                coeffs_c[fc] = -val
        const[c] = const_c
        coeffs[c] = coeffs_c

    # Depth-first search over free variables with simple bounding
    free_order = free_cols  # could be permuted (e.g. by ub) if needed
    ub_free = [ub[c] for c in free_order]
    x_free = [0] * num_free

    best_sum = float("inf")

    def dfs(idx: int) -> None:
        nonlocal best_sum
        if idx == num_free:
            # Build full solution vector x
            x = [0] * m
            # Assign free variables
            for k, col in enumerate(free_order):
                x[col] = x_free[k]
            # Compute pivot variables
            for c in pivot_cols:
                val = const[c]
                for fc, coeff in coeffs[c].items():
                    val += coeff * x[fc]
                # Must be a non-negative integer
                if val.denominator != 1:
                    return
                intval = val.numerator
                if intval < 0:
                    return
                x[c] = intval

            # Validate against original constraints (defensive check)
            for i in range(n):
                s = 0
                for j in range(m):
                    if A[i][j]:
                        s += x[j]
                if s != jolts[i]:
                    return

            total = sum(x)
            if total < best_sum:
                best_sum = total
            return

        # Simple pruning: if we've already used as many free-variable presses
        # as the best known total, we can stop this branch.
        partial_sum = sum(x_free[:idx])
        if partial_sum >= best_sum:
            return

        col = free_order[idx]
        max_v = ub_free[idx]
        for v in range(max_v + 1):
            x_free[idx] = v
            dfs(idx + 1)
        x_free[idx] = 0

    dfs(0)

    if best_sum == float("inf"):
        raise RuntimeError("No non-negative integer solution found for jolts")

    return int(best_sum)


def solve_puzzle2(machines: List[Machine]) -> int:
    total = 0
    for _pattern, buttons, jolts in machines:
        total += min_presses_jolts(buttons, jolts)
    return total


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main(argv: List[str]) -> int:
    if len(argv) > 2:
        print(
            "Usage: python solve.py [input_file]",
            file=sys.stderr,
        )
        return 1

    input_path = Path(argv[1]) if len(argv) == 2 else Path("input.txt")

    try:
        machines = load_input(input_path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Measure each puzzle separately
    t1_start = time.perf_counter()
    result1 = solve_puzzle1(machines)
    t1_end = time.perf_counter()

    t2_start = time.perf_counter()
    result2 = solve_puzzle2(machines)
    t2_end = time.perf_counter()

    t1_ms = (t1_end - t1_start) * 1000.0
    t2_ms = (t2_end - t2_start) * 1000.0
    total_ms = t1_ms + t2_ms

    # Required output format
    print(f"Puzzle 1: {result1}")
    print(f"Puzzle 2: {result2}")
    print(f"Total Duration: {total_ms:.3f}ms")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
