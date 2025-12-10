# Factory Puzzle Solver

This project solves both parts of the **Day 10: Factory** puzzle using the shared `input.txt` file as described in the puzzle statements. 

The solver is implemented as a single Python script, `solve.py`, which reads the machines from `input.txt`, computes the minimal number of button presses for both puzzles, and prints the results and total runtime in the required format. :contentReference[oaicite:3]{index=3}

## Language Choice

**Language:** Python 3

**Reasons:**

- The puzzle is dominated by:
  - Text parsing of a custom line format (`[pattern] (a,b,...) ... {numbers}`).
  - Small-to-medium combinatorial searches per machine.
  - Exact rational arithmetic for solving small linear systems.
- Python's standard library provides:
  - `re` for robust parsing.
  - `fractions.Fraction` for exact rational arithmetic in Gaussian elimination.
  - `time.perf_counter()` for precise timing.
- Input sizes are modest (hundreds of machines, each with at most ~10 counters/buttons), so Python's performance is sufficient while keeping the implementation compact and readable.

No external dependencies are required.

## Puzzle Overview

Each line of `input.txt` describes a single machine:

```text
[pattern] (i,j,...) (k,...) ... {t0,t1,...}
