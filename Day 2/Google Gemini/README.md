# North Pole Valid ID Checker

[cite_start]This tool solves the "Gift Shop" puzzles by identifying invalid product IDs based on repeating digit patterns[cite: 5, 11]. It parses a list of integer ranges and calculates the sum of all IDs that satisfy the repeating sequence criteria.

## Language Choice: Python 3
Python was selected for:
1.  [cite_start]**String Manipulation**: The core logic relies on slicing strings to detect repeated patterns (e.g., checking if `123123` is `123` repeated)[cite: 11]. Python's slice syntax (`str[:mid]`) makes this extremely readable.
2.  **Big Integer Support**: The input ranges contain 10-digit numbers (e.g., `9292901468`). Python handles these transparently without overflow risks.
3.  **Simplicity**: The boilerplate required to parse comma-separated files and iterate ranges is minimal in Python.

## Prerequisites
* **Python 3.6+** installed on your system.
* The input file `input.txt` must be present in the same directory.

## Dependencies
* Standard Library only (`sys`, `time`, `os`).

## Build Instructions
No compilation is required.

## Run Command
Execute the solution from your terminal:

```bash
python solve.py