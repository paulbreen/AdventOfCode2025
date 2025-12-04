import time
import sys
from typing import List, Tuple

# --- Constants ---
# The character representing a roll of paper
PAPER_ROLL = '@'
# The character representing an empty space (or removed paper)
EMPTY_SPACE = '.'

def load_grid(file_path: str) -> List[List[str]]:
    """Loads the grid from the input file."""
    try:
        with open(file_path, 'r') as f:
            # Replace 'x' in the example with '.' for a clean grid representation, 
            # though the input file itself should only contain '@' and '.'
            content = f.read().strip().replace('x', EMPTY_SPACE) 
            # Split by line and convert each line string into a list of characters (cells)
            return [list(line) for line in content.split('\n') if line]
    except FileNotFoundError:
        print(f"Error: Input file '{file_path}' not found.")
        sys.exit(1)

def count_neighbors(grid: List[List[str]], r: int, c: int) -> int:
    """Counts the number of PAPER_ROLL neighbors (8-way adjacency) for a cell (r, c)."""
    rows = len(grid)
    cols = len(grid[0])
    neighbor_count = 0
    
    # Iterate over the 3x3 neighborhood centered at (r, c)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center cell itself
            if dr == 0 and dc == 0:
                continue
            
            nr, nc = r + dr, c + dc
            
            # Check bounds and if the neighbor is a paper roll
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == PAPER_ROLL:
                neighbor_count += 1
                
    return neighbor_count

# --- Puzzle 1 Solver ---

def solve_puzzle_1(initial_grid: List[List[str]]) -> int:
    """
    Solves Puzzle 1: Count rolls accessible by a forklift in the initial state.
    Accessible: A roll ('@') has fewer than four PAPER_ROLL neighbors.
    """
    rows = len(initial_grid)
    cols = len(initial_grid[0])
    accessible_count = 0
    
    for r in range(rows):
        for c in range(cols):
            if initial_grid[r][c] == PAPER_ROLL:
                # Check the accessibility rule: fewer than four neighbors
                if count_neighbors(initial_grid, r, c) < 4:
                    accessible_count += 1
                    
    return accessible_count

# --- Puzzle 2 Solver ---

def solve_puzzle_2(initial_grid: List[List[str]]) -> int:
    """
    Solves Puzzle 2: Count total rolls removed through the iterative process.
    Process: 
    1. Find all accessible rolls (fewer than 4 neighbors)
    2. Remove all of them in a single step.
    3. Repeat until no rolls are accessible.
    """
    # Create a deep copy of the grid to modify
    grid = [row[:] for row in initial_grid]
    rows = len(grid)
    cols = len(grid[0])
    total_removed = 0
    
    while True:
        # 1. Identify accessible rolls in the current state
        accessible_rolls: List[Tuple[int, int]] = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == PAPER_ROLL:
                    # Check accessibility rule: fewer than four neighbors
                    if count_neighbors(grid, r, c) < 4:
                        accessible_rolls.append((r, c))

        # 2. Check termination condition
        if not accessible_rolls:
            break

        # 3. Remove all accessible rolls in this step
        removed_in_step = len(accessible_rolls)
        total_removed += removed_in_step
        
        # Update the grid state for the next iteration
        for r, c in accessible_rolls:
            # Change the removed roll to an empty space for neighbor counting in the next step
            grid[r][c] = EMPTY_SPACE

        # print(f"Removed {removed_in_step} rolls.") # Debugging print
        
    return total_removed

# --- Main Execution ---

if __name__ == "__main__":
    
    # The uploaded file name is 'input.txt'
    INPUT_FILE = "input.txt" 
    
    # 1. Load Data
    start_time = time.perf_counter()
    initial_grid = load_grid(INPUT_FILE)
    
    # 2. Solve Puzzle 1
    p1_start = time.perf_counter()
    result_p1 = solve_puzzle_1(initial_grid)
    p1_duration = (time.perf_counter() - p1_start) * 1000
    
    # 3. Solve Puzzle 2
    p2_start = time.perf_counter()
    result_p2 = solve_puzzle_2(initial_grid)
    p2_duration = (time.perf_counter() - p2_start) * 1000
    
    # 4. Display Results
    total_duration = (time.perf_counter() - start_time) * 1000
    
    # The prompt requires the exact format below:
    print(f"Puzzle 1: {result_p1}")
    print(f"Puzzle 2: {result_p2}")
    print(f"Total Duration: {total_duration:.3f}ms")

# Example Test Case for Verification (from Puzzle 2.txt):
# Initial state: 10 rows, 10 cols
# ..@@.@@@@.
# @@@.@.@.@@
# @@@@@.@.@@
# @.@@@@..@.
# @@.@@@@.@@
# .@@@@@@@.@
# .@.@.@.@@@
# @.@@@.@@@@
# .@@@@@@@@.
# @.@.@@@.@.
# Expected P1: 13
# Expected P2: 43