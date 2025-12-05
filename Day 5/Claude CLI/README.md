# Advent of Code 2025 - Day 5: Cafeteria

This solution solves both parts of the Day 5 puzzle involving ingredient freshness checking based on ID ranges.

## Language Choice: Python

**Why Python?**
- **Native large integer support**: The puzzle involves ID ranges with numbers in the hundreds of trillions. Python handles arbitrary-precision integers natively without overflow concerns.
- **Clean parsing**: Python's string manipulation and list comprehensions make parsing the input file straightforward.
- **Algorithm clarity**: Range merging and overlap detection are clearly expressed in Python.
- **Standard library**: No external dependencies needed - `time` module provides timing functionality.
- **Single-command execution**: Python scripts run directly without compilation.

## Prerequisites

- **Python**: Version 3.6 or higher
- **Operating System**: Windows, macOS, or Linux with Python installed

To check your Python version:
```bash
python --version
```
or
```bash
python3 --version
```

## Dependencies

**None** - This solution uses only Python standard library modules:
- `time` - for execution timing

## Build Instructions

No build step required. Python is an interpreted language.

## Run Command

Execute the solution with a single command:

```bash
python solution.py
```

On some systems, you may need to use:
```bash
python3 solution.py
```

## Expected Output

The program outputs results in the following format:
```
Puzzle 1: 607
Puzzle 2: 342433357244012
Total Duration: 4.38ms
```

## How It Works

### Puzzle 1: Fresh Ingredient Count
- Parses the input file to extract fresh ID ranges and available ingredient IDs
- Checks each available ingredient ID against all ranges
- Counts how many IDs fall within at least one fresh range
- **Answer**: 607 ingredients are fresh

### Puzzle 2: Total Fresh IDs
- Takes only the range definitions (ignores the available ingredient list)
- Merges overlapping or adjacent ranges to avoid double-counting
- Counts the total number of unique IDs covered by all ranges
- **Answer**: 342,433,357,244,012 total fresh IDs

### Algorithm Highlights

**Range Checking (Puzzle 1)**:
- Simple linear search through ranges for each ingredient ID
- Time complexity: O(n * m) where n = number of IDs, m = number of ranges
- Efficient enough for the input size (1000 IDs, 173 ranges)

**Range Merging (Puzzle 2)**:
1. Sort ranges by start position: O(m log m)
2. Iterate through sorted ranges once: O(m)
3. Merge overlapping or adjacent ranges
4. Count total IDs in merged ranges: O(k) where k = number of merged ranges
- Overall time complexity: O(m log m)

## File Structure

```
.
├── solution.py    # Main solution code
├── input.txt      # Puzzle input data
├── Puzzle 1.txt   # Puzzle 1 description
├── Puzzle 2.txt   # Puzzle 2 description
└── README.md      # This file
```

## Performance

- **Execution time**: ~4-5ms on modern hardware
- **Memory usage**: Minimal - stores ranges and IDs in memory
- **Scalability**: Handles large numbers efficiently thanks to Python's arbitrary-precision integers

## Code Quality

- Clean, readable code with descriptive function names
- Comments explaining key logic
- Proper separation of concerns (parsing, solving, output)
- Error-free execution with the provided input
- Follows Python conventions (PEP 8 style)
