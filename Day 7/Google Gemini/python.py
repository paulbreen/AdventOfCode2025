import sys
import time

def solve_puzzle_1(grid, start_pos):
    """
    Calculates the total number of times the beam is split (classical manifold).
    
    The simulation tracks beam segments that move downward. A beam stops at a splitter
    and creates two new beams (left and right) one row below.
    A state is (row, column_of_origin) where column_of_origin is the column
    from which the current downward beam started *after* the last split.
    This approach is actually too complex because of overlap. Let's stick
    to the simpler rule: a split is counted whenever a beam hits a '^'.
    
    A more effective way is a recursive/iterative simulation, tracking which
    (row, col) splitters have been activated. Since the beams move down,
    we only need to track the current active "beam sources" (columns that
    are currently emitting a downward beam from a split one row above).
    """
    
    # Grid dimensions
    R = len(grid)
    C = len(grid[0])
    
    # The set of columns currently emitting a downward beam.
    # Initial beam starts at the start column.
    active_beam_cols = {start_pos[1]}
    total_splits = 0
    
    # Iterate through rows, starting one row below 'S' (since S is in a row).
    # The beam has effectively passed through the 'S' row to start its downward journey.
    for r in range(start_pos[0] + 1, R):
        new_active_cols = set()
        
        # We need to track which splitters in the current row 'r' have been hit and processed.
        # This set will store the column index of the *splitter* that was hit.
        splitters_hit_in_row = set()
        
        # Iterate over all columns currently carrying a downward beam.
        for c in active_beam_cols:
            # Check if the current cell contains a splitter
            if 0 <= c < C and grid[r][c] == '^':
                # Splitter hit! Only count the split once, even if multiple beams
                # would hit the same splitter. The problem asks for "how many times 
                # will the beam be split," implying unique splitter events.
                if c not in splitters_hit_in_row:
                    total_splits += 1
                    splitters_hit_in_row.add(c)
                
                # New beams are emitted one column left and one column right.
                # These columns will be the active beam columns for the next row (r+1).
                new_active_cols.add(c - 1)
                new_active_cols.add(c + 1)
            else:
                # Empty space (or out of bounds, which we ignore until the next row check), 
                # the beam continues downward in the same column.
                new_active_cols.add(c)
        
        # The new active beam columns for the next iteration (r+1) are the ones
        # that were not stopped by a splitter in this row. We only care about 
        # columns within the grid bounds for the next check.
        active_beam_cols = {c for c in new_active_cols if 0 <= c < C}
        
        # If no more beams are active, we can stop the simulation early.
        if not active_beam_cols:
            break
            
    return total_splits

def solve_puzzle_2(grid, start_pos):
    """
    Calculates the number of active timelines after all possible journeys (quantum manifold).
    
    This is a path-counting problem on a DAG (movement is only downward). We use Dynamic Programming.
    DP[r][c] will store the number of paths (timelines) reaching cell (r, c).
    """
    R = len(grid)
    C = len(grid[0])
    
    # Initialize DP table: DP[r][c] = number of timelines reaching (r, c)
    # The array needs to be R+1 rows to handle paths exiting the manifold boundary
    # and the last row where the paths "complete."
    DP = [[0] * C for _ in range(R + 1)]
    
    # Initial state: One path (timeline) starts at S position.
    DP[start_pos[0]][start_pos[1]] = 1
    
    # The start row of the manifold processing is the row of 'S'.
    # We iterate down to the last row (R-1). The paths that land in row R 
    # are the ones that have "completed their journey."
    for r in range(start_pos[0], R):
        for c in range(C):
            # If no timelines reach this cell, skip it
            if DP[r][c] == 0:
                continue
            
            num_paths = DP[r][c]
            cell = grid[r][c]
            
            if cell == '.':
                # Empty space: paths continue straight down to (r+1, c)
                if r + 1 < R + 1: # Always true, but good practice
                    DP[r + 1][c] += num_paths
            
            elif cell == 'S' or cell == '^':
                # Start 'S' or Splitter '^': paths split left and right
                
                # Path 1: Move left (r+1, c-1)
                if c - 1 >= 0 and r + 1 < R + 1:
                    DP[r + 1][c - 1] += num_paths
                
                # Path 2: Move right (r+1, c+1)
                if c + 1 < C and r + 1 < R + 1:
                    DP[r + 1][c + 1] += num_paths

    # The total number of active timelines is the sum of all paths that 
    # successfully reached the final row of the grid.
    # The final row of the grid is R-1, and paths from R-1 land in R.
    # We use row R of the DP table for the final tally.
    return sum(DP[R])


def run_solution():
    try:
        # Read the input file
        with open("input.txt", 'r') as f:
            lines = [line.strip() for line in f]
    except FileNotFoundError:
        print("Error: input.txt not found.")
        sys.exit(1)

    # Clean the grid: remove empty lines and parse the S position
    grid = []
    start_pos = None # (row, col)
    for r, line in enumerate(lines):
        if not line:
            continue
        # Replace 'S' with '.' for correct simulation of subsequent steps
        # but keep track of its position.
        if 'S' in line:
            s_col = line.find('S')
            start_pos = (r, s_col)
            # Replace 'S' with '.' for the grid
            grid.append(list(line.replace('S', '.'))) 
        else:
            grid.append(list(line))
    
    # Convert list of lists to list of strings for easier simulation
    grid_str = ["".join(row) for row in grid]
    
    if not start_pos:
        print("Error: 'S' (start position) not found in input.")
        sys.exit(1)
        
    # --- Puzzle 1 Execution ---
    start_time_1 = time.time()
    result_1 = solve_puzzle_1(grid_str, start_pos)
    end_time_1 = time.time()
    duration_1 = (end_time_1 - start_time_1) * 1000

    # --- Puzzle 2 Execution ---
    start_time_2 = time.time()
    result_2 = solve_puzzle_2(grid_str, start_pos)
    end_time_2 = time.time()
    duration_2 = (end_time_2 - start_time_2) * 1000

    # --- Output Results ---
    total_duration = duration_1 + duration_2

    print(f"Puzzle 1: {result_1}")
    print(f"Puzzle 2: {result_2}")
    print(f"Total Duration: {total_duration:.3f}ms")

if __name__ == "__main__":
    run_solution()