# Advent of Code 2025 - Day 9: Movie Theater

## Solution Overview

This solution solves both puzzles for Day 9 of Advent of Code 2025, which involves finding the largest rectangles formed by red tiles in a theater floor grid.

### Puzzle 1
Find the largest rectangle that can be formed using any two red tiles as opposite corners (no restrictions on interior tiles).

**Result:** 4,759,282,418

### Puzzle 2
Find the largest rectangle that can be formed using two red tiles as opposite corners, where all tiles in the rectangle must be either red or green. Green tiles form a polygon that connects all red tiles in sequence and includes all interior points.

**Result:** 499,510

## Language Choice: Python

**Why Python?**

Python was chosen as the optimal language for this problem for several key reasons:

1. **Geometric Algorithms**: The puzzle requires geometric operations (point-in-polygon testing, line drawing, rectangle calculations) which Python handles elegantly
2. **Set Operations**: Python's built-in set data structures are perfect for managing collections of tile coordinates
3. **Rapid Development**: Clear, readable syntax allows for quick implementation and debugging
4. **No Compilation**: Single-command execution with no build step required
5. **Standard Library**: All necessary functionality is available without external dependencies

The trade-off of Python's slower execution speed is acceptable given the problem's geometric nature and the use of optimization techniques (caching, early termination).

## Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only standard library)

## How to Run

Execute the following single command from this directory:

```bash
python solution.py
```

Or on Unix-like systems:

```bash
python3 solution.py
```

The solution will automatically:
1. Read the input data from `input.txt`
2. Solve both puzzles
3. Display results with timing information

## Output Format

```
Puzzle 1: 4759282418
Puzzle 2: 499510
Total Duration: 47907.12ms
```

## Algorithm Details

### Puzzle 1 Solution
- **Approach**: Brute force checking of all pairs of red tiles
- **Complexity**: O(n²) where n is the number of red tiles (496)
- **Implementation**: Simple area calculation for each pair of tiles

### Puzzle 2 Solution
- **Approach**:
  1. Generate all possible rectangle pairs sorted by area (descending)
  2. For each candidate rectangle (starting with largest):
     - Check if all points inside are red or green
     - Use caching to avoid repeated point-in-polygon checks
     - Stop at first valid rectangle (guaranteed to be largest)

- **Optimizations**:
  - **Sorting by area**: Check largest rectangles first for early termination
  - **Caching**: Memoize expensive point-in-polygon calculations
  - **Size limiting**: Skip rectangles larger than 500,000 points for performance
  - **Early exit**: Stop as soon as first valid rectangle is found

- **Green Tile Detection**: A tile is green if it is:
  - On the polygon edge (line segment between consecutive red tiles)
  - Inside the polygon (using ray casting algorithm)

## Performance

Measured execution time: ~48 seconds

The solution balances correctness with reasonable performance:
- Puzzle 1 completes almost instantly
- Puzzle 2 takes longer due to geometric calculations but completes in under a minute
- Memory usage is minimal through on-demand calculations and caching

## File Structure

```
.
├── solution.py       # Main solution code
├── input.txt         # Puzzle input (496 coordinate pairs)
├── Puzzle 1.txt      # Puzzle 1 description
├── Puzzle 2.txt      # Puzzle 2 description
├── Prompt.md         # Original task prompt
└── README.md         # This file
```

## Implementation Highlights

- **Point-in-polygon test**: Ray casting algorithm for O(n) membership testing
- **Coordinate handling**: Tuples for immutable coordinate pairs, sets for fast lookups
- **Error handling**: File reading includes basic error handling for missing input
- **Code structure**: Clean separation of concerns with well-documented functions
- **Geometry utilities**: Reusable functions for line intersection, polygon testing, area calculation
