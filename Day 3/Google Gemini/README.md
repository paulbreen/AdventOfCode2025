# Battery Joltage Puzzle Solver

This tool solves the "Elf Battery" puzzles by analyzing sequences of digits to determine maximum power output configurations.

## Language Choice: Python

Python was selected for this implementation due to:
1.  **Native Large Integer Support**: Puzzle 2 requires summing multiple 12-digit numbers. Python handles integers of arbitrary size automatically, preventing overflow issues without requiring external BigInt libraries.
2.  **Lexicographical String Logic**: The core logic involves comparing digit sequences to find the "largest" combination. Python treats string comparisons lexicographically by default, which simplifies the logic for Part 2.
3.  **Readability**: The "Greedy Stack" algorithm used for Part 2 is most cleanly expressed using Python's list operations.

## Prerequisites

* **Python 3.6** or higher.
* No external dependencies or libraries are required.

## Build Instructions

No compilation is necessary. Ensure `solution.py` and `input.txt` are in the same directory.

## Run Command

Execute the solution using the command line:

```bash
python solution.py