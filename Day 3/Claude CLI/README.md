# Advent of Code 2025 - Day 3: Lobby Solution

## Language Chosen: Python 3

### Why Python?

Python was selected for this problem because:

1. **String Manipulation Excellence**: The puzzle involves processing digit strings, and Python's native string handling is both elegant and efficient
2. **Large Number Support**: Python handles arbitrarily large integers natively, which is essential for Puzzle 2 where we deal with 12-digit numbers
3. **Clean Algorithm Implementation**: The greedy monotonic stack algorithm is straightforward to implement and understand in Python
4. **No Compilation Overhead**: Quick iteration and immediate execution
5. **Readability**: The code is self-documenting and easy to verify for correctness

## Problem Summary

### Puzzle 1
From each line (battery bank) of digits, select exactly 2 digits (maintaining their order) that form the maximum possible 2-digit number. Sum all maximum values.

### Puzzle 2
From each line of digits, select exactly 12 digits (maintaining their order) that form the maximum possible 12-digit number. Sum all maximum values.

## Algorithm Approach

The solution uses a **greedy algorithm with a monotonic decreasing stack**:

1. To select k digits from n digits forming the maximum number:
   - Iterate through each digit
   - Maintain a stack of selected digits
   - If the current digit is larger than the stack top and we can still remove digits, pop from stack
   - This ensures larger digits are kept in leftmost positions

2. Time Complexity: O(n) per line, where n is the number of digits
3. Space Complexity: O(k) for the result stack

## Prerequisites

- **Python 3.7 or higher** (uses f-strings and standard library features)
- No external dependencies required

## Build Instructions

No compilation needed - Python is an interpreted language.

## Run Command

```bash
python solution.py
```

Or make it executable (Unix/Linux/Mac):
```bash
chmod +x solution.py
./solution.py
```

## Dependencies

- **Standard Library Only**:
  - `time` - for execution duration measurement
  - No external packages required (pip install not needed)

## Expected Output Format

```
Puzzle 1: [result]
Puzzle 2: [result]
Total Duration: [time]ms
```

## Testing

A test script is included to verify the solution against the examples from the puzzle description:

```bash
python test_example.py
```

Expected test output: All tests should show `[PASS]` status.

## Solution Results

- **Puzzle 1 Answer**: 17155
- **Puzzle 2 Answer**: 169685670469164
- **Execution Time**: ~5ms

## File Structure

```
.
├── solution.py       # Main solution file
├── test_example.py   # Test suite with puzzle examples
├── input.txt         # Puzzle input data
├── README.md         # This file
├── Prompt.md         # Original task instructions
├── Puzzle 1.txt      # Puzzle 1 description
└── Puzzle 2.txt      # Puzzle 2 description
```

## Code Quality Features

- ✓ Clean, readable code with descriptive variable names
- ✓ Comprehensive docstrings for all functions
- ✓ Error handling for missing input files
- ✓ Optimized algorithm (linear time complexity)
- ✓ Well-commented where logic is non-obvious
- ✓ Follows PEP 8 style guidelines
- ✓ Single-command execution
- ✓ Precise timing measurement
