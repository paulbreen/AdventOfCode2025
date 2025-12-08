# Advent of Code 2025 - Day 8: Playground

Solution for Day 8 puzzles involving junction box circuits and minimum spanning trees.

## Language Choice

**Python 3.x** was selected for this implementation based on the following criteria:

### Why Python?

1. **Algorithm Complexity**: This problem requires implementing a Union-Find (Disjoint Set Union) data structure and processing ~500,000 edge pairs. Python provides clean, readable syntax for complex algorithmic implementations.

2. **Built-in Performance**: Python's built-in `sort()` uses Timsort, which is highly optimized for real-world data and runs in O(n log n) time with excellent constant factors.

3. **Development Speed**: The problem requires careful algorithmic thinking rather than raw computational speed. Python allows for rapid implementation and testing of the solution logic.

4. **Standard Library**: All required functionality (file I/O, data structures, timing) is available in the standard library with no external dependencies.

5. **Simplicity**: Single-file solution with straightforward execution - no compilation, build system, or complex setup required.

### Performance Considerations

While languages like Rust or C++ would offer faster execution, the algorithmic complexity dominates the runtime. The current solution completes in ~1.4 seconds, which is acceptable for this problem size. The bottleneck is the O(n²) pairwise distance calculation, which would benefit from algorithmic optimization (e.g., spatial indexing) rather than language selection.

## Problem Overview

### Puzzle 1
Connect the 1000 closest pairs of junction boxes and determine the product of the three largest circuit sizes.

### Puzzle 2
Continue connecting junction boxes until all are in a single circuit, then multiply the X coordinates of the last two connected boxes.

## Algorithm

The solution uses a **Minimum Spanning Tree (MST)** approach with **Kruskal's algorithm**:

1. **Parse Input**: Read 1000 3D coordinates (X,Y,Z)
2. **Generate Edges**: Calculate Euclidean distance for all pairs (~499,500 edges)
3. **Sort Edges**: Order by increasing distance
4. **Union-Find**: Process edges in order, connecting junction boxes using Union-Find
5. **Track Progress**:
   - After 1000 connection attempts: Record component sizes for Puzzle 1
   - Continue until single circuit: Track last connection for Puzzle 2

### Data Structures

- **Union-Find**: O(α(n)) amortized time for union and find operations (α is the inverse Ackermann function, effectively constant)
- **Edge List**: Sorted list of (distance, box_i, box_j) tuples

### Time Complexity

- Edge generation: O(n²) where n = 1000
- Sorting: O(E log E) where E ≈ 499,500
- Union-Find operations: O(E × α(n)) ≈ O(E)
- **Total: O(n² log n)**

### Space Complexity

- O(n²) for storing all edges
- O(n) for Union-Find structure

## Prerequisites

- **Python 3.6 or higher**
- Standard library only (no external dependencies)

## Build Instructions

No compilation required. Python is an interpreted language.

## Run Command

```bash
python solution.py
```

Or with Python 3 explicitly:

```bash
python3 solution.py
```

## Expected Output

```
Puzzle 1: 352584
Puzzle 2: 9617397716
Total Duration: [time]ms
```

The duration will vary based on hardware but should be in the range of 1000-2000ms on modern systems.

## Input File

The solution expects an `input.txt` file in the same directory with the following format:

```
X1,Y1,Z1
X2,Y2,Z2
...
```

Each line contains three comma-separated integers representing a 3D coordinate.

## Dependencies

None. The solution uses only Python standard library modules:
- `time` - For performance timing
- `collections.defaultdict` - For component size tracking

## Error Handling

The solution includes error handling for:
- Missing `input.txt` file
- Malformed input data
- General exceptions during execution

## Code Structure

- **UnionFind class**: Implements disjoint set union with path compression and union by size
- **parse_input()**: Reads and parses the input file
- **euclidean_distance()**: Calculates 3D Euclidean distance
- **solve_puzzles()**: Main algorithm implementation
- **main()**: Entry point with timing and output formatting
