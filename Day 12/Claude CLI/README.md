# Advent of Code 2025 - Day 12: Christmas Tree Farm

## Solution Overview

This solution solves the Day 12 puzzle using a **backtracking algorithm** to determine how many regions can fit all their required present shapes.

## Language Choice: Python

**Why Python?**

1. **Algorithm Complexity Dominates** - This is an NP-hard constraint satisfaction problem (polyomino packing). The algorithmic approach matters far more than raw language speed.

2. **Rapid Development** - Complex logic for:
   - Shape rotations and flips (8 possible orientations per shape)
   - Grid manipulation and collision detection
   - Backtracking with state management
   - All significantly easier to implement and debug in Python

3. **Clean Data Structures** - Python's built-in sets, lists, and tuples provide elegant solutions for:
   - Coordinate representation
   - Occupied cell tracking
   - Unique orientation generation

4. **Sufficient Performance** - Despite being an interpreted language, the solution completes in ~20 seconds for 1000 test cases, which is reasonable for this complexity class.

## Problem Description

**Puzzle 1: Present Packing**

Given:
- 6 different present shapes (polyominoes) that can be rotated and flipped
- 1000 regions with specified dimensions
- Each region lists required quantities of each shape type

Task: Determine how many regions can accommodate ALL their required presents.

**Constraints:**
- Shapes can be rotated (4 orientations) and flipped (2 states) = up to 8 unique orientations
- Shapes cannot overlap (# cells must be in different positions)
- Shapes can interlock (. cells in shape definitions don't block other shapes)
- All presents must fit perfectly on the grid

**Puzzle 2:** Not yet available (typical for Advent of Code - revealed after Part 1)

## Algorithm Approach

### 1. Shape Preprocessing
- Parse all 6 shape definitions
- Generate all unique orientations (rotations + flips) for each shape
- Normalize coordinates for consistent placement

### 2. Constraint Checking
- Quick area check: reject if total shape area exceeds region area
- Prevents unnecessary backtracking on impossible cases

### 3. Backtracking Solver
For each region:
1. Build list of all presents to place (with their orientations)
2. Recursively attempt to place each present:
   - Try each orientation of the current shape
   - Try each position in the grid
   - If placement is valid (no collisions, within bounds):
     - Place the shape
     - Recurse to place next present
     - If recursion succeeds, region is solvable
     - If recursion fails, backtrack (remove shape and try next position)
3. If all presents placed successfully, increment counter

### 4. Optimization Techniques
- **Set-based collision detection** - O(1) lookup for occupied cells
- **Early termination** - Area pre-check eliminates impossible cases
- **Normalized coordinates** - Reduces orientation space by eliminating duplicates

## Prerequisites

- **Python 3.7+** (uses type hints)
- No external dependencies (standard library only)

## Build Instructions

No build step required - Python is interpreted.

## Run Command

```bash
python solution.py
```

## Input Files

- `input.txt` - Contains shape definitions and region specifications
- `Puzzle 1.txt` - Problem description for Part 1

## Output Format

```
Puzzle 1: 565
Puzzle 2: 0
Total Duration: 20705ms
```

- **Puzzle 1**: Number of regions that can fit all required presents
- **Puzzle 2**: Placeholder (0) until Part 2 is revealed
- **Total Duration**: Execution time in milliseconds

## Dependencies

**None** - Uses only Python standard library:
- `time` - Performance measurement
- `typing` - Type annotations for clarity

## Performance Characteristics

- **Time Complexity**: O(n × k × r × w × h) worst case, where:
  - n = number of regions (1000)
  - k = number of presents per region (varies, up to ~350)
  - r = orientations per shape (≤8)
  - w, h = region dimensions (up to 50×50)

- **Space Complexity**: O(w × h) for grid state per region

- **Actual Runtime**: ~20 seconds for 1000 regions on standard hardware

## Code Structure

```python
parse_input()           # Parse shapes and regions from input file
shape_to_coords()       # Convert shape strings to coordinate lists
get_all_orientations()  # Generate rotations and flips
can_fit_presents()      # Main entry point per region
solve_region()          # Recursive backtracking solver
can_place()             # Collision detection
place_shape()           # Add shape to grid
remove_shape()          # Backtrack by removing shape
```

## Error Handling

- File not found: Program will raise `FileNotFoundError` if `input.txt` is missing
- Invalid input format: Parser includes validation and gracefully handles malformed lines

## Testing

To verify the solution works correctly:

1. Ensure `input.txt` is in the same directory as `solution.py`
2. Run `python solution.py`
3. Check that output matches expected format
4. Verify execution completes without errors

## Future Enhancements (Part 2)

When Part 2 is revealed, the solution structure allows easy extension:
- `solve_puzzle2()` function is ready to implement
- Shape and region parsing is reusable
- May require different solving strategy based on Part 2 requirements

## Solution Results

**Part 1 Answer: 565**

Out of 1000 regions, 565 can successfully fit all their required presents using the constraint satisfaction algorithm.
