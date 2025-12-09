# Advent of Code - Movie Theater Tile Puzzles

This repository contains the solution for the "Movie Theater" tile puzzles. The task involves finding the largest rectangle area based on a set of red tile coordinates under two different constraints.

## Language Chosen: Python

Python was chosen for its excellent balance of **simplicity, readability, and performance** for this problem.
* The $O(N^2)$ and $O(N^3)$ algorithms required for the puzzles are highly efficient with Python's native data structures (dictionaries, sets, lists) for the given input size ($N=200$ points).
* Python's clear syntax aids in implementing the complex geometry logic, specifically the Ray Casting algorithm needed for Puzzle 2's polygon containment check.

## Prerequisites

* **Language Version:** Python 3.6+
* **Runtime:** The standard Python runtime environment.

## Dependencies

* No external packages or libraries are required. The solution uses only the Python standard library (`sys`, `time`).

## Build Instructions

No compilation is needed. Python is an interpreted language.

## Run Command

The solution can be executed with a single command, provided the `input.txt` file is in the same directory as the script.

```bash
python3 solution.py