# Day 7: Laboratories - Tachyon Manifold Simulation

## Language Choice: Python

**Why Python?**
- **Clean syntax**: Ideal for grid manipulation and BFS algorithms
- **Built-in data structures**: Sets and deques provide efficient queue operations and deduplication
- **Fast development**: Rapid prototyping without sacrificing readability
- **Sufficient performance**: The BFS algorithm with visited-state tracking runs in milliseconds
- **Single-file execution**: No compilation step required

## Problem Summary

### Puzzle 1: Beam Splitting Count
Simulate tachyon beams moving downward through a manifold. When a beam encounters a splitter (`^`), it stops and creates two new beams that continue from the positions immediately to the left and right. Count the total number of splits that occur.

### Puzzle 2: Quantum Timeline Count
Apply quantum mechanics interpretation where a single particle takes BOTH paths at each splitter, creating multiple timelines. Count the number of unique exit positions where particles leave the manifold (representing distinct timelines).

## Algorithm Approach

**Puzzle 1**: BFS with splitter activation tracking
- Track which splitters have been activated to avoid double-counting
- Simulate each beam moving downward until hitting a splitter or exiting
- Each activated splitter increments the split counter and spawns two new beams

**Puzzle 2**: BFS with position-based deduplication
- Track visited positions to avoid reprocessing the same states
- At each splitter, queue both left and right paths
- Count unique exit positions where particles leave the grid

**Time Complexity**: O(N) where N is the number of grid cells
**Space Complexity**: O(N) for visited set and queue

## Prerequisites

- **Python**: Version 3.6 or higher
- **Standard Library**: Only built-in modules used (`time`, `collections`)

## Build Instructions

No compilation required. Python is an interpreted language.

## Run Command

```bash
python solution.py
```

## Dependencies

None. The solution uses only Python standard library modules:
- `time`: For performance measurement
- `collections.deque`: For efficient BFS queue operations

## Output Format

```
Puzzle 1: [number of splits]
Puzzle 2: [number of timelines]
Total Duration: [execution time]ms
```

## Example Output

```
Puzzle 1: 1613
Puzzle 2: 85
Total Duration: 2.84ms
```

## Error Handling

- Checks for missing `input.txt` file
- Validates that starting position 'S' exists in the manifold diagram
- Graceful error messages for any exceptions

## Code Structure

- `parse_input()`: Reads grid and locates starting position
- `solve_puzzle1()`: Implements classical beam-splitting simulation
- `solve_puzzle2()`: Implements quantum timeline counting
- `main()`: Orchestrates execution, timing, and output formatting
