# Advent of Code 2025 - Day 4: Printing Department

## Language Choice: Python

### Why Python?

Python was selected for this solution based on the following factors:

1. **Grid Manipulation Excellence**: Python's list comprehensions and intuitive indexing make 2D grid operations clean and readable
2. **Algorithmic Problem Suitability**: The puzzle involves neighbor counting and iterative grid updates - tasks where Python's clear syntax excels
3. **Rapid Development**: No compilation step, immediate execution, and straightforward debugging
4. **Standard Library**: Built-in data structures (sets, lists) perfectly match the problem requirements
5. **Performance**: While not as fast as compiled languages, Python is more than adequate for this grid size (~140x140)
6. **Single-File Solution**: The entire solution fits cleanly in one file with no external dependencies

## Prerequisites

- **Python**: Version 3.7 or higher
- **Operating System**: Cross-platform (Windows, macOS, Linux)
- **No external dependencies**: Uses only Python standard library

### Checking Python Version

```bash
python --version
```

or

```bash
python3 --version
```

## Build Instructions

No build or compilation step required. Python is an interpreted language.

## Run Command

Execute the solution with a single command:

```bash
python solution.py
```

On some systems, you may need to use `python3` instead:

```bash
python3 solution.py
```

## Dependencies

**None** - This solution uses only Python's standard library:
- `time` - For execution timing
- `typing` - For type hints (improves code readability)

## Input Files

- `input.txt` - The puzzle input data (grid of paper rolls)
- `Puzzle 1.txt` - Description of puzzle 1
- `Puzzle 2.txt` - Description of puzzle 2

## Output Format

The program outputs results in the exact format specified:

```
Puzzle 1: [result]
Puzzle 2: [result]
Total Duration: [time]ms
```

### Example Output

```
Puzzle 1: 1604
Puzzle 2: 9397
Total Duration: 272.73ms
```

## Solution Approach

### Puzzle 1: Count Accessible Rolls
- Parse the grid from `input.txt`
- For each roll (@), count adjacent rolls in all 8 directions
- A roll is accessible if it has fewer than 4 adjacent rolls
- Count and return the number of accessible rolls

### Puzzle 2: Iterative Removal
- Start with the original grid
- Find all accessible rolls (< 4 adjacent)
- Remove them (replace with '.')
- Repeat until no more rolls can be accessed
- Return the total count of removed rolls

### Data Structures

- **2D List (Grid)**: Represents the paper roll layout
- **Set of Tuples**: Stores coordinates of accessible rolls for efficient lookup
- **8-Direction Vector**: `[(-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1)]`

### Time Complexity

- **Puzzle 1**: O(n×m) where n×m is the grid size
- **Puzzle 2**: O(k×n×m) where k is the number of iterations (until no rolls remain)

### Space Complexity

- O(n×m) for storing the grid and accessible roll coordinates

## Verification

The solution was tested against the example provided in the puzzle description:

**Example Grid:**
```
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
```

**Expected Results:**
- Puzzle 1: 13 accessible rolls ✓
- Puzzle 2: 43 total rolls removed ✓

Both puzzles pass validation with the example data.

## Code Quality

The solution includes:
- Clear function names and docstrings
- Type hints for better code documentation
- Error handling for missing input files
- Modular design with separate functions for each task
- Comments explaining non-obvious logic
- Clean separation between puzzle 1 and puzzle 2 logic

## Performance

On the provided input (139 lines × ~140 characters):
- Total execution time: ~270ms
- Both puzzles solved in a single run
- No optimization needed for this problem size

## File Structure

```
.
├── solution.py           # Main solution code
├── input.txt            # Puzzle input data
├── Puzzle 1.txt         # Puzzle 1 description
├── Puzzle 2.txt         # Puzzle 2 description
├── test_example.txt     # Example test data
├── README.md            # This file
└── Prompt.md            # Original task prompt
```

## Author Notes

This solution prioritizes:
1. **Correctness**: Verified against example data
2. **Readability**: Clean, well-documented code
3. **Simplicity**: No unnecessary complexity or dependencies
4. **Performance**: Efficient algorithms without premature optimization
5. **Maintainability**: Easy to understand and modify
