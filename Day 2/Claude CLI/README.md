# Gift Shop - Invalid Product ID Solver

Solution for Advent of Code 2025, Day 2: Identifying invalid product IDs based on repeating digit patterns.

## Language Choice: Python 3

**Why Python?**

1. **String Manipulation Excellence**: The core algorithm requires detecting repeating digit patterns (e.g., "123123" = "123" repeated). Python's string slicing (`str[:mid]`) and comparison operations make this logic extremely clean and readable.

2. **Big Integer Support**: The input contains large 10-digit numbers (e.g., `9292901468`). Python handles arbitrary-precision integers natively without overflow concerns or special libraries.

3. **Minimal Boilerplate**: Parsing comma-separated ranges and iterating over number sequences requires minimal code compared to compiled languages.

4. **Single-Command Execution**: No compilation step needed - just `python solve.py` to run.

5. **Standard Library Only**: The solution uses only built-in modules (`sys`, `time`, `os`), eliminating external dependencies.

## Algorithm Overview

### Puzzle 1: Sequence Repeated Exactly Twice
An ID is invalid if it consists of some digit sequence repeated exactly twice.

Examples:
- `55` → "5" repeated twice ✓
- `6464` → "64" repeated twice ✓
- `123123` → "123" repeated twice ✓
- `1234` → Cannot be split into two identical halves ✗

**Algorithm**: Check if the number has even length and the first half equals the second half.

### Puzzle 2: Sequence Repeated At Least Twice
An ID is invalid if it consists of some digit sequence repeated 2 or more times.

Examples:
- `12341234` → "1234" repeated 2 times ✓
- `123123123` → "123" repeated 3 times ✓
- `1212121212` → "12" repeated 5 times ✓
- `1111111` → "1" repeated 7 times ✓

**Algorithm**: For each possible pattern length that divides the total length evenly, check if repeating that pattern recreates the original number.

## Prerequisites

- **Python 3.9+** (recommended: Python 3.11+)
- The `input.txt` file must be present in the same directory as `solve.py`

## Dependencies

**None** - Uses only Python standard library:
- `sys` - Command-line arguments and error handling
- `time` - Performance timing
- `os` - File existence checking

## Build Instructions

No compilation required.

## Run Command

Execute from the command line:

```bash
python solve.py
```

Or make it executable (Linux/Mac):

```bash
chmod +x solve.py
./solve.py
```

## Expected Output Format

```
Puzzle 1: [sum of invalid IDs using rule 1]
Puzzle 2: [sum of invalid IDs using rule 2]
Total Duration: [execution time]ms
```

## Example

Given the sample ranges from the puzzle description, the output would be:

```
Puzzle 1: 1227775554
Puzzle 2: 4174379265
Total Duration: 45.23ms
```

## Performance

The solution iterates through all numbers in the given ranges and checks each for the repeating pattern criteria. For typical Advent of Code inputs with moderate range sizes, execution completes in under 100ms.

## Error Handling

- Checks for `input.txt` existence before processing
- Provides clear error messages if file is missing or unreadable
- Validates range parsing from comma-separated format

## Code Structure

- `is_invalid_puzzle1()` - Detects patterns repeated exactly twice
- `is_invalid_puzzle2()` - Detects patterns repeated at least twice
- `parse_ranges()` - Parses comma-separated range format
- `solve_puzzle1()` - Sums all invalid IDs for puzzle 1
- `solve_puzzle2()` - Sums all invalid IDs for puzzle 2
- `main()` - Orchestrates file reading, solving, and output
