# Cafeteria Puzzle Solver (Day 5)

## Overview

This project solves two related inventory puzzles based on ingredient ID ranges and available ingredient IDs.

Input format (from `input.txt`):

- A list of **fresh ingredient ID ranges**, one per line, e.g. `3-5`
- A **blank line**
- A list of **available ingredient IDs**, one per line, e.g. `11`

Puzzle descriptions are provided in `Puzzle 1.txt` and `Puzzle 2.txt`. `input.txt` is the only file needed at runtime.

### Puzzle 1

Count how many of the available ingredient IDs are **fresh**, i.e. fall within **at least one** of the fresh ID ranges (ranges are inclusive).

### Puzzle 2

Ignore the list of available IDs. Treat the fresh ID ranges as a union of intervals and compute the **total number of unique ingredient IDs** that are considered fresh (i.e. size of the union of all ranges).

---

## Language Choice

**Language:** Python 3

**Rationale:**

- The puzzles involve:
  - Parsing many lines of text.
  - Working with large integer ranges and sets of IDs.
  - Simple but careful interval algorithms.
- Python offers:
  - Built-in arbitrary-precision integers (no overflow risk).
  - Straightforward string and file handling.
  - Quick implementation of interval merging and binary search with standard library support (`bisect`).
- Performance is easily sufficient for the given input sizes (hundreds of ranges and thousands of IDs), while keeping the solution clean and readable.

No external dependencies are required.

---

## Prerequisites

- **Python**: Version **3.8+** (tested features: `pathlib`, `time.perf_counter`, type hints).
- A standard command-line environment (Linux, macOS, or Windows).

---

## Files

- `solver.py` – Main entry point containing the implementation of both puzzles.
- `input.txt` – Puzzle input:
  - Fresh ranges
  - Blank line
  - Available IDs
- `Puzzle 1.txt` – Human-readable description for Puzzle 1 (not required at runtime).
- `Puzzle 2.txt` – Human-readable description for Puzzle 2 (not required at runtime).

---

## Build Instructions

No compilation is needed.

Ensure the following files are in the same directory:

- `solver.py`
- `input.txt`

---

## Run Command

From the directory containing `solver.py` and `input.txt`, run:

```bash
python solver.py
