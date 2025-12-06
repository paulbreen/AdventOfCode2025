import time
import re
from typing import List, Tuple, Union

# Define the input file name
INPUT_FILE = "input.txt"

def load_input_grid(filename: str) -> List[str]:
    """Loads the input file and returns it as a list of lines (a grid)."""
    try:
        with open(filename, 'r') as f:
            # Strip trailing newline but keep other whitespace
            return [line.rstrip('\n') for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: Input file '{filename}' not found.")
        exit(1)

def parse_problems_part1(grid: List[str]) -> List[Tuple[List[int], str]]:
    """
    Parses the input grid into a list of problems for Part 1 (top-to-bottom reading).
    A problem is a tuple: (list of numbers, operation symbol).
    """
    if not grid:
        return []

    # The last line always contains the operators
    operator_line = grid[-1]
    # The number lines are all lines before the last one
    number_lines = grid[:-1]

    # --- CORRECTION APPLIED HERE ---
    # 1. Collect all operators and their start indices from the operator line
    operators: List[Tuple[int, str]] = []
    for match in re.finditer(r'([+*])', operator_line):
        operators.append((match.start(), match.group(1)))
    # -------------------------------
    
    if not operators:
        return []

    problems: List[Tuple[List[int], str]] = []
    
    # 1. Determine all unique column indices that contain non-space characters
    non_space_indices = set()
    for line in grid:
        for i, char in enumerate(line):
            if not char.isspace():
                non_space_indices.add(i)
    
    sorted_indices = sorted(list(non_space_indices))
    
    if not sorted_indices:
        return []
        
    # 2. Group the non-space columns into contiguous blocks (problems).
    problem_columns: List[List[int]] = []
    if sorted_indices:
        current_block = [sorted_indices[0]]
        for i in range(1, len(sorted_indices)):
            if sorted_indices[i] != sorted_indices[i-1] + 1:
                problem_columns.append(current_block)
                current_block = [sorted_indices[i]]
            else:
                current_block.append(sorted_indices[i])
        problem_columns.append(current_block)


    # 3. Extract numbers and operators for each problem block
    for col_block in problem_columns:
        start_col = col_block[0]
        end_col = col_block[-1]
        
        op = None
        # Find the operator for this block (must be in the operator line within the block range)
        for op_start, op_symbol in operators:
            if start_col <= op_start <= end_col:
                op = op_symbol
                break
        
        if op is None:
            continue 

        numbers: List[int] = []
        # Extract numbers from the number lines within this column block
        for line in number_lines:
            # Slice the relevant part of the line
            segment = line[start_col : end_col + 1]
            
            # Extract the number from the segment. Alignment can be ignored.
            number_str = "".join(char for char in segment if char.isdigit())
            if number_str:
                numbers.append(int(number_str))
        
        if numbers:
            problems.append((numbers, op))
    
    return problems


def solve_problems_part1(problems: List[Tuple[List[int], str]]) -> int:
    """
    Calculates the grand total for Part 1 problems (numbers read top-to-bottom).
    """
    total = 0
    for numbers, op in problems:
        result = 0
        if not numbers:
            continue

        if op == '+':
            # Add together all the numbers
            result = sum(numbers)
        elif op == '*':
            # Multiply together all the numbers
            result = 1
            for num in numbers:
                result *= num
        
        total += result
    return total

def parse_problems_part2(grid: List[str]) -> List[Tuple[List[int], str]]:
    """
    Parses the input grid into a list of problems for Part 2 (right-to-left, column-to-number reading).
    A problem is a tuple: (list of numbers, operation symbol).
    """
    if not grid:
        return []

    operator_line = grid[-1]
    number_lines = grid[:-1]
    
    # 1. Determine problem column blocks (same as Part 1)
    non_space_indices = set()
    for line in grid:
        for i, char in enumerate(line):
            if not char.isspace():
                non_space_indices.add(i)
    
    sorted_indices = sorted(list(non_space_indices))
    
    if not sorted_indices:
        return []
        
    problem_columns: List[List[int]] = []
    if sorted_indices:
        current_block = [sorted_indices[0]]
        for i in range(1, len(sorted_indices)):
            if sorted_indices[i] != sorted_indices[i-1] + 1:
                problem_columns.append(current_block)
                current_block = [sorted_indices[i]]
            else:
                current_block.append(sorted_indices[i])
        problem_columns.append(current_block)

    problems: List[Tuple[List[int], str]] = []
    
    # 2. Process each problem block (column-by-column, right-to-left)
    
    # Process blocks from right to left
    for col_block in reversed(problem_columns):
        op = None
        
        # --- CORRECTION APPLIED HERE ---
        # The loop must iterate over the match objects and extract the values manually.
        for match in re.finditer(r'([+*])', operator_line):
            op_start = match.start()
            op_symbol = match.group(1)
        
            if col_block[0] <= op_start <= col_block[-1]:
                op = op_symbol
                break
        # -------------------------------
        
        if op is None:
            continue
        
        # Cephalopod math is written right-to-left in columns.
        # Each number is given in its own column, with the most significant digit at the top 
        # and the least significant digit at the bottom.
        
        block_numbers: List[int] = []
        # Iterate over the columns in the block, from right to left
        for col_index in reversed(col_block):
            digit_chars = []
            # Read digits from top to bottom (most significant to least significant)
            for line in number_lines:
                if col_index < len(line) and line[col_index].isdigit():
                    digit_chars.append(line[col_index])
            
            if digit_chars:
                number_str = "".join(digit_chars)
                block_numbers.append(int(number_str))
        
        if block_numbers:
            problems.append((block_numbers, op))
    
    return problems


def solve_problems_part2(problems: List[Tuple[List[int], str]]) -> int:
    """
    Calculates the grand total for Part 2 problems.
    The list of problems is already in right-to-left order of appearance.
    The numbers within each problem were constructed column-by-column, right-to-left.
    """
    # The list of problems is already parsed and ordered right-to-left.
    # The calculation logic is the same as Part 1: sum/multiply the numbers.
    return solve_problems_part1(problems)


def main():
    """Main execution function to solve both parts and time the results."""
    start_time = time.time()
    
    # 1. Load the input data
    grid = load_input_grid(INPUT_FILE)

    # --- Part 1 ---
    p1_start_time = time.time()
    problems_p1 = parse_problems_part1(grid)
    result_p1 = solve_problems_part1(problems_p1)
    p1_duration = (time.time() - p1_start_time) * 1000

    # --- Part 2 ---
    p2_start_time = time.time()
    problems_p2 = parse_problems_part2(grid)
    result_p2 = solve_problems_part2(problems_p2)
    p2_duration = (time.time() - p2_start_time) * 1000
    
    # --- Output ---
    total_duration = (time.time() - start_time) * 1000

    print(f"Puzzle 1: {result_p1}")
    print(f"Puzzle 2: {result_p2}")
    print(f"Total Duration: {total_duration:.2f}ms")

if __name__ == "__main__":
    main()