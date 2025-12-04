import time
from typing import List, Set, Tuple

def read_input(filename: str) -> List[List[str]]:
    """Read the input file and return as a 2D grid."""
    try:
        with open(filename, 'r') as f:
            return [list(line.rstrip('\n')) for line in f]
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        exit(1)

def count_adjacent_rolls(grid: List[List[str]], row: int, col: int) -> int:
    """Count the number of rolls (@) in the 8 adjacent positions."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    count = 0

    # Check all 8 directions: N, NE, E, SE, S, SW, W, NW
    directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row][new_col] == '@':
                count += 1

    return count

def find_accessible_rolls(grid: List[List[str]]) -> Set[Tuple[int, int]]:
    """Find all rolls that can be accessed (< 4 adjacent rolls)."""
    accessible = set()
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == '@':
                adjacent_count = count_adjacent_rolls(grid, row, col)
                if adjacent_count < 4:
                    accessible.add((row, col))

    return accessible

def solve_puzzle1(grid: List[List[str]]) -> int:
    """Solve puzzle 1: Count initially accessible rolls."""
    return len(find_accessible_rolls(grid))

def solve_puzzle2(grid: List[List[str]]) -> int:
    """Solve puzzle 2: Count total rolls that can be removed iteratively."""
    # Create a mutable copy of the grid
    working_grid = [row[:] for row in grid]
    total_removed = 0

    while True:
        # Find accessible rolls
        accessible = find_accessible_rolls(working_grid)

        if not accessible:
            break

        # Remove accessible rolls
        for row, col in accessible:
            working_grid[row][col] = '.'

        total_removed += len(accessible)

    return total_removed

def main():
    # Read input
    grid = read_input('input.txt')

    # Solve Puzzle 1
    start_time = time.perf_counter()
    result1 = solve_puzzle1(grid)
    time1 = time.perf_counter() - start_time

    # Solve Puzzle 2
    start_time = time.perf_counter()
    result2 = solve_puzzle2(grid)
    time2 = time.perf_counter() - start_time

    # Display results
    total_duration = (time1 + time2) * 1000  # Convert to milliseconds
    print(f"Puzzle 1: {result1}")
    print(f"Puzzle 2: {result2}")
    print(f"Total Duration: {total_duration:.2f}ms")

if __name__ == "__main__":
    main()
