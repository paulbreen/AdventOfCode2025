# Advent of Code 2025 - Day 10: Factory Initialization

This solution solves both parts of the Day 10 puzzle using Python with no external dependencies beyond the standard library.

## Language Choice: Python 3

**Why Python?**
- **Problem Nature**: Both puzzles involve mathematical optimization:
  - Puzzle 1: Finding minimum button presses in a binary XOR system (lights toggle)
  - Puzzle 2: Solving an underdetermined system of linear equations with minimum L1 norm
- **Clean Implementation**: Python's simple syntax allows for clear expression of complex algorithms
- **Efficient for this Scale**: While not the fastest language, Python is more than adequate for the problem size (~200 machines)
- **No External Dependencies Needed**: Pure Python implementation using only standard library (no numpy, scipy, or other packages)
- **Rapid Development**: Built-in data structures (lists, dictionaries) and comprehensions make the code concise and readable

## Algorithm Overview

### Puzzle 1: Indicator Lights (Binary XOR System)
The problem is to find the minimum number of button presses to configure indicator lights, where:
- Each button toggles specific lights (XOR operation)
- Pressing a button twice cancels out (XOR is self-inverse)
- Therefore, we only need to consider pressing each button 0 or 1 times

**Solution**: Brute force enumeration of all 2^n combinations where n is the number of buttons. For each machine with up to ~13 buttons, this is tractable (2^13 = 8,192 combinations).

### Puzzle 2: Joltage Counters (Linear System)
The problem is to find the minimum total button presses to reach exact joltage levels, where:
- Each button increments specific counters by 1
- We need to reach exact target values for all counters
- This forms a system of linear equations: Ax = b, where we want to minimize ||x||₁

**Solution**:
1. Use Gaussian elimination to reduce to row echelon form
2. Identify "free variables" (degrees of freedom in the system)
3. For small numbers of free variables (≤10), try all reasonable assignments
4. For each assignment, solve for "basic variables" and check validity
5. Return the solution with minimum total presses

## Prerequisites

- **Python 3.7 or higher**
- No external packages required (uses only Python standard library)

## Files

- `solution.py` - Main solution code
- `input.txt` - Puzzle input data
- `README.md` - This file

## Build Instructions

No build step is required. Python is an interpreted language.

## Run Command

```bash
python solution.py
```

Or on systems where Python 3 needs explicit invocation:

```bash
python3 solution.py
```

## Output Format

The solution outputs results in the required format:

```
Puzzle 1: [result]
Puzzle 2: [result]
Total Duration: [time]ms
```

Example output:
```
Puzzle 1: 491
Puzzle 2: 19974
Total Duration: 3996ms
```

## Dependencies

**None** - This solution uses only Python standard library modules:
- `re` - Regular expression parsing for input
- `time` - Execution time measurement
- `sys` - Error handling and exit codes
- `typing` - Type hints for code clarity
- `itertools.product` - Cartesian product for exhaustive search

## Performance

- **Puzzle 1**: O(2^n × m) per machine, where n = buttons, m = lights
  - Typically n ≤ 13, so ~8K iterations per machine
- **Puzzle 2**: O(n³) for Gaussian elimination + exponential search over free variables
  - Free variables typically ≤ 3, making exhaustive search practical
- **Total Runtime**: ~4 seconds for 187 machines on standard hardware

## Code Structure

```
solution.py
├── parse_machine()          # Parses input format using regex
├── solve_puzzle1_machine()  # Brute force XOR system solver
├── solve_puzzle2_machine()  # Linear system solver with optimization
└── main()                   # Driver function with timing
```

## Error Handling

- File not found: Exits with error message if `input.txt` is missing
- Invalid input: Regex parsing handles malformed lines gracefully
- No solution: Returns 0 if no valid configuration exists

## Testing

To test with the example data:
1. Create a `test_input.txt` with example machines
2. Temporarily modify line 204 to read `test_input.txt`
3. Run and verify results match expected values (Puzzle 1: 7, Puzzle 2: 33)

## Design Decisions

1. **Pure Python**: Avoided numpy/scipy to minimize dependencies
2. **Brute Force for Puzzle 1**: Exhaustive search guarantees optimal solution
3. **Hybrid Approach for Puzzle 2**: Gaussian elimination + smart enumeration balances correctness and performance
4. **No premature optimization**: Code prioritizes clarity and correctness over micro-optimizations

## Complexity Analysis

- **Space**: O(n × m) for matrices, where n = buttons, m = counters/lights
- **Time**:
  - Puzzle 1: O(2^n) per machine (exponential in buttons)
  - Puzzle 2: O(n³ + k^f) where k = search range, f = free variables
- **Practical**: Both puzzles complete in under 5 seconds for the given input
