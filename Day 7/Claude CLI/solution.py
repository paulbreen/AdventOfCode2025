import time
from collections import deque

def parse_input(filename):
    """Parse the manifold diagram from input file."""
    with open(filename, 'r') as f:
        grid = [list(line.rstrip('\n')) for line in f]

    # Find starting position 'S'
    start_row, start_col = None, None
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'S':
                start_row, start_col = row, col
                break
        if start_row is not None:
            break

    return grid, start_row, start_col


def solve_puzzle1(grid, start_row, start_col):
    """
    Puzzle 1: Count how many times beams are split.
    Beams move downward from S. When a beam hits a '^' splitter,
    it stops and creates two new beams at positions to the left and right.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    split_count = 0
    # Queue contains (row, col) of active beams moving downward
    queue = deque([(start_row, start_col)])
    # Track which splitters have been activated to avoid double-counting
    activated_splitters = set()

    while queue:
        row, col = queue.popleft()

        # Move downward until we hit a splitter or exit the manifold
        while row < rows:
            # Check if current position has a splitter
            if row >= 0 and col >= 0 and col < len(grid[row]) and grid[row][col] == '^':
                # Only count this split if we haven't activated this splitter before
                if (row, col) not in activated_splitters:
                    activated_splitters.add((row, col))
                    split_count += 1

                    # Create two new beams: one to the left, one to the right
                    # Both continue moving downward from the next row
                    if col > 0:
                        queue.append((row + 1, col - 1))
                    if col < cols - 1:
                        queue.append((row + 1, col + 1))

                break  # This beam stops here

            row += 1  # Continue moving downward

    return split_count


def solve_puzzle2(grid, start_row, start_col):
    """
    Puzzle 2: Count the number of unique timelines.
    A single particle takes BOTH paths at each splitter.
    Count unique exit positions where particles leave the manifold.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Track visited positions to avoid reprocessing
    visited = set()
    # Track unique exit positions
    exit_positions = set()

    # Queue contains (row, col)
    queue = deque([(start_row, start_col)])

    while queue:
        row, col = queue.popleft()

        # Skip if already visited this position
        if (row, col) in visited:
            continue
        visited.add((row, col))

        # Move downward until we hit a splitter or exit
        current_row = row
        while current_row < rows:
            # Check if current position has a splitter
            if current_row >= 0 and col >= 0 and col < len(grid[current_row]) and grid[current_row][col] == '^':
                # At a splitter, the particle takes BOTH paths
                # Left path
                if col > 0:
                    queue.append((current_row + 1, col - 1))

                # Right path
                if col < cols - 1:
                    queue.append((current_row + 1, col + 1))

                break  # Stop moving this particular path

            current_row += 1
        else:
            # Beam exited the manifold at this position
            exit_positions.add((current_row, col))

    return len(exit_positions)


def main():
    try:
        # Parse input
        grid, start_row, start_col = parse_input('input.txt')

        if start_row is None:
            print("Error: Could not find starting position 'S' in input")
            return

        # Solve Puzzle 1
        start_time1 = time.perf_counter()
        result1 = solve_puzzle1(grid, start_row, start_col)
        time1 = (time.perf_counter() - start_time1) * 1000

        # Solve Puzzle 2
        start_time2 = time.perf_counter()
        result2 = solve_puzzle2(grid, start_row, start_col)
        time2 = (time.perf_counter() - start_time2) * 1000

        # Display results
        print(f"Puzzle 1: {result1}")
        print(f"Puzzle 2: {result2}")
        print(f"Total Duration: {time1 + time2:.2f}ms")

    except FileNotFoundError:
        print("Error: input.txt file not found")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
