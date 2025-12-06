import time
import sys
from pathlib import Path


def read_input(filename):
    """Read the input file and return lines."""
    try:
        with open(filename, 'r') as f:
            return [line.rstrip('\n') for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: Could not find {filename}")
        sys.exit(1)


def parse_worksheet(lines):
    """Parse the worksheet into a grid."""
    # The input has 4 rows of numbers and 1 row of operators
    if len(lines) < 5:
        raise ValueError("Invalid input: expected at least 5 lines")

    # Get the maximum line length to ensure consistent grid width
    max_len = max(len(line) for line in lines)

    # Pad all lines to the same length
    grid = []
    for line in lines:
        grid.append(line.ljust(max_len))

    return grid


def solve_puzzle1(grid):
    """
    Puzzle 1: Read left-to-right.
    Each column represents a problem where numbers are stacked vertically,
    and the operator is at the bottom.
    """
    if len(grid) < 5:
        return 0

    num_rows = len(grid) - 1  # Last row is operators
    num_cols = len(grid[0])

    problems = []
    current_problem = []

    # Process column by column (left to right)
    for col in range(num_cols):
        # Check if this column is all spaces (separator)
        is_separator = all(grid[row][col] == ' ' for row in range(len(grid)))

        if is_separator:
            if current_problem:
                problems.append(current_problem)
                current_problem = []
        else:
            # Extract the column (numbers + operator)
            column_data = {
                'numbers': [],
                'operator': grid[-1][col]  # Last row is the operator
            }

            # Get numbers from rows 0 to num_rows-1
            for row in range(num_rows):
                cell = grid[row][col].strip()
                if cell and cell.isdigit():
                    column_data['numbers'].append(int(cell))

            current_problem.append(column_data)

    # Don't forget the last problem
    if current_problem:
        problems.append(current_problem)

    # Calculate results for each problem
    grand_total = 0

    for problem in problems:
        if not problem:
            continue

        # Get the operator (should be the same for all columns in the problem)
        operator = None
        all_numbers = []

        for col_data in problem:
            if col_data['operator'] in ['*', '+']:
                operator = col_data['operator']
            all_numbers.extend(col_data['numbers'])

        if not all_numbers or operator is None:
            continue

        # Calculate the result
        result = all_numbers[0]
        for num in all_numbers[1:]:
            if operator == '*':
                result *= num
            else:  # operator == '+'
                result += num

        grand_total += result

    return grand_total


def solve_puzzle2(grid):
    """
    Puzzle 2: Read right-to-left.
    Each column's digits (top to bottom) form a single number.
    """
    if len(grid) < 5:
        return 0

    num_rows = len(grid) - 1  # Last row is operators
    num_cols = len(grid[0])

    problems = []
    current_problem = []

    # Process column by column (RIGHT to LEFT)
    for col in range(num_cols - 1, -1, -1):
        # Check if this column is all spaces (separator)
        is_separator = all(grid[row][col] == ' ' for row in range(len(grid)))

        if is_separator:
            if current_problem:
                problems.append(current_problem)
                current_problem = []
        else:
            # Extract the column and form a number from top to bottom
            digits = []
            for row in range(num_rows):
                cell = grid[row][col].strip()
                if cell and cell.isdigit():
                    digits.append(cell)

            # Form the number from the digits (top to bottom)
            if digits:
                number = int(''.join(digits))
                operator = grid[-1][col]  # Last row is the operator

                current_problem.append({
                    'number': number,
                    'operator': operator
                })

    # Don't forget the last problem
    if current_problem:
        problems.append(current_problem)

    # Calculate results for each problem
    grand_total = 0

    for problem in problems:
        if not problem:
            continue

        # Get the operator (should be the same for all in the problem)
        operator = None
        numbers = []

        for item in problem:
            if item['operator'] in ['*', '+']:
                operator = item['operator']
            numbers.append(item['number'])

        if not numbers or operator is None:
            continue

        # Calculate the result
        result = numbers[0]
        for num in numbers[1:]:
            if operator == '*':
                result *= num
            else:  # operator == '+'
                result += num

        grand_total += result

    return grand_total


def main():
    # Read input
    input_file = Path(__file__).parent / 'input.txt'
    lines = read_input(input_file)

    # Parse the worksheet
    grid = parse_worksheet(lines)

    # Start timing
    start_time = time.time()

    # Solve Puzzle 1
    puzzle1_start = time.time()
    result1 = solve_puzzle1(grid)
    puzzle1_time = time.time() - puzzle1_start

    # Solve Puzzle 2
    puzzle2_start = time.time()
    result2 = solve_puzzle2(grid)
    puzzle2_time = time.time() - puzzle2_start

    # Calculate total duration
    total_duration = (time.time() - start_time) * 1000  # Convert to milliseconds

    # Print results in the required format
    print(f"Puzzle 1: {result1}")
    print(f"Puzzle 2: {result2}")
    print(f"Total Duration: {total_duration:.2f}ms")


if __name__ == "__main__":
    main()
