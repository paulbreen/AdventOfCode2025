# Day 6: Trash Compactor - Solution

## Language Choice

**Python 3.8+** was selected for this solution due to:

- **Excellent string and grid manipulation**: Python's string operations and list comprehensions make parsing the worksheet grid straightforward
- **Built-in arbitrary precision integers**: No risk of integer overflow when calculating large products
- **Clean, readable code**: Python's syntax allows for expressing the algorithm clearly
- **Zero compilation overhead**: Immediate execution without build steps
- **Rich standard library**: `pathlib` for file handling, `time` for performance measurement
- **Optimal for parsing problems**: Advent of Code-style problems benefit from Python's expressiveness

## Problem Summary

### Puzzle 1: Left-to-Right Reading
Parse a math worksheet where:
- Each column represents a problem
- Numbers are stacked vertically within each column
- The operator (`*` or `+`) is at the bottom of each problem
- Problems are separated by blank columns
- Calculate each problem and sum all results

### Puzzle 2: Right-to-Left Reading
Parse the same worksheet but:
- Read columns from right to left
- Each column's digits (top to bottom) form a single number
- Same operator rules apply
- Calculate each problem and sum all results

## Prerequisites

- **Python**: Version 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **No external dependencies**: Uses only Python standard library

## Build Instructions

No build step required. Python is an interpreted language.

## Run Command

```bash
python solution.py
```

Or, if you have both Python 2 and 3 installed:

```bash
python3 solution.py
```

## Expected Output Format

```
Puzzle 1: [result]
Puzzle 2: [result]
Total Duration: [time]ms
```

## Input File

The solution expects an `input.txt` file in the same directory with the following format:
- Lines 1-4: Number rows (grid data)
- Line 5: Operator row (`*` or `+` symbols)
- Problems separated by columns of spaces

## Dependencies

None. This solution uses only Python's standard library:
- `time`: For execution time measurement
- `sys`: For error handling
- `pathlib`: For robust file path handling

## Algorithm Overview

### Puzzle 1 (Left-to-Right)
1. Parse input into a grid structure
2. Iterate through columns from left to right
3. Identify problem boundaries (blank column separators)
4. For each problem, collect all numbers in the columns
5. Apply the operator to all numbers sequentially
6. Sum all problem results

### Puzzle 2 (Right-to-Left)
1. Use the same grid structure
2. Iterate through columns from right to left
3. For each column, concatenate digits top-to-bottom to form a number
4. Group numbers by problem (using blank column separators)
5. Apply the operator to all numbers in each problem
6. Sum all problem results

## Code Structure

- `read_input()`: Reads and validates the input file
- `parse_worksheet()`: Converts input lines into a normalized grid
- `solve_puzzle1()`: Implements the left-to-right parsing logic
- `solve_puzzle2()`: Implements the right-to-left parsing logic
- `main()`: Orchestrates the solution and formats output

## Error Handling

- File not found errors are caught and reported
- Invalid input format raises descriptive errors
- Empty or malformed problems are skipped gracefully

## Performance

The solution runs in O(n × m) time where:
- n = number of rows in the grid
- m = number of columns in the grid

Both puzzles are solved in a single pass through the data with minimal memory overhead.
