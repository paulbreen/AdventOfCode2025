# Advent of Code 2025 - Day 1: Secret Entrance

## Language Choice: Python 3

### Why Python?
Python was selected for this challenge because:

- **Simplicity**: Straightforward string parsing and arithmetic operations
- **Zero compilation**: Runs directly with a single command
- **Readability**: Clean, maintainable code that clearly expresses the algorithm
- **Performance**: More than adequate for this computational task
- **Standard library**: Built-in time measurement and file handling
- **Cross-platform**: Works identically on Windows, macOS, and Linux

## Problem Summary

The puzzles involve simulating a circular dial (0-99) that starts at position 50. Given a series of rotations (L for left/lower, R for right/higher), we need to track how many times the dial points to position 0.

- **Puzzle 1**: Count zeros at the end of each rotation
- **Puzzle 2**: Count zeros during rotations (all intermediate positions)

## Algorithm

The solution uses modular arithmetic to handle the circular nature of the dial:

1. Parse each rotation instruction (direction + distance)
2. For Puzzle 1: Calculate final position after each rotation using `(position ± distance) % 100`
3. For Puzzle 2: Step through each click of the dial to count all zero crossings
4. Track cumulative zero counts throughout the rotation sequence

## Prerequisites

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

## Installation

No installation required! Python comes pre-installed on most systems.

To verify Python is installed:
```bash
python --version
```
or
```bash
python3 --version
```

## Build Instructions

No build step required for Python scripts.

## Run Command

From the `Claude CLI` directory:

```bash
python solution.py
```

Or on systems where Python 3 is explicitly named:

```bash
python3 solution.py
```

## Output Format

The solution outputs results in the exact format specified:

```
Puzzle 1: [result]
Puzzle 2: [result]
Total Duration: [time]ms
```

## Dependencies

**None** - Uses only Python standard library:
- `time`: For execution timing
- `pathlib`: For cross-platform file path handling

## File Structure

```
Claude CLI/
├── solution.py    # Main solution implementation
└── README.md      # This file

Instructions/
├── input.txt      # Puzzle input data
├── Puzzle 1.txt   # Puzzle 1 description
├── Puzzle 2.txt   # Puzzle 2 description
└── Prompt.md      # Challenge instructions
```

## Implementation Details

The solution is structured with clear separation of concerns:

- `parse_rotation()`: Extracts direction and distance from input
- `solve_puzzle_one()`: Efficient O(n) solution using modular arithmetic
- `solve_puzzle_two()`: Simulates each dial click to count all zero crossings
- `main()`: Orchestrates file I/O, timing, and output formatting

The code includes error handling for missing input files and comprehensive documentation.
