import time
import sys
from collections import defaultdict

# --- Robust Input Parsing ---

def read_input(filename):
    """
    Reads and parses the input file using a state-machine approach
    to handle variable whitespace and input formatting.
    """
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{filename}' not found.")
        sys.exit(1)

    shapes = {}
    regions = []
    
    current_shape_idx = None
    current_shape_rows = []

    def save_current_shape():
        nonlocal current_shape_idx, current_shape_rows
        if current_shape_idx is not None and current_shape_rows:
            shapes[current_shape_idx] = parse_grid_to_coords(current_shape_rows)
        current_shape_rows = []
        current_shape_idx = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check for Shape Header (e.g., "0:")
        if line[0].isdigit() and line.endswith(':') and 'x' not in line:
            save_current_shape() # Save previous shape if exists
            try:
                current_shape_idx = int(line[:-1])
            except ValueError:
                continue # Skip malformed lines

        # Check for Region Line (e.g., "40x42: 30 30 ...")
        elif 'x' in line and ':' in line:
            save_current_shape() # Ensure last shape is saved
            
            parts = line.split(':')
            size_part = parts[0].strip()
            counts_part = parts[1].strip()
            
            try:
                w_str, l_str = size_part.split('x')
                width = int(w_str)
                length = int(l_str)
                
                counts = [int(x) for x in counts_part.split() if x.isdigit()]
                
                # Create the list of presents for this region
                present_list = []
                for idx, count in enumerate(counts):
                    if idx in shapes:
                        present_list.extend([shapes[idx]] * count)
                
                if present_list:
                    regions.append({
                        'width': width,
                        'length': length,
                        'presents': tuple(present_list)
                    })
            except ValueError:
                continue # Skip malformed region lines

        # Check for Shape Body (e.g., "###", "..#")
        elif set(line).issubset({'#', '.'}):
            if current_shape_idx is not None:
                current_shape_rows.append(line)

    # Save the very last shape if the file ends with one
    save_current_shape()

    return shapes, regions

def parse_grid_to_coords(grid):
    """Converts a list of strings (grid) into a canonical set of coordinates."""
    coords = set()
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == '#':
                coords.add((r, c))
    
    if not coords:
        return frozenset()
    
    # Normalize: Top-leftmost '#' becomes (0,0)
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return frozenset((r - min_r, c - min_c) for r, c in coords)

# --- Transformations and Optimization ---

def generate_transformations(shape_coords):
    """Generates all 8 unique rotations and flips."""
    if not shape_coords:
        return {frozenset()}

    coords = list(shape_coords)
    orientations = set()

    def normalize(c_set):
        if not c_set:
            return frozenset()
        min_r = min(r for r, c in c_set)
        min_c = min(c for r, c in c_set)
        return frozenset((r - min_r, c - min_c) for r, c in c_set)

    # Rotate 4 times
    current = coords
    for _ in range(4):
        orientations.add(normalize(frozenset(current)))
        current = [(c, -r) for r, c in current] # 90 deg clockwise
    
    # Flip and Rotate 4 times
    flipped = [(r, -c) for r, c in coords]
    current = flipped
    for _ in range(4):
        orientations.add(normalize(frozenset(current)))
        current = [(c, -r) for r, c in current]
        
    return frozenset(orientations)

# --- Backtracking Solver ---

def solve_packing(width, length, presents_list, unique_transformations):
    """
    Backtracking solver.
    Heuristic: Sort presents by size (largest first) to fail fast on impossible paths.
    """
    
    # 1. Sort presents by size (Area) descending.
    # Larger pieces are harder to place, so placing them first reduces the search tree.
    sorted_presents = sorted(presents_list, key=lambda p: len(p), reverse=True)
    
    # Group identical shapes
    presents_groups = defaultdict(list)
    for i, p_shape in enumerate(sorted_presents):
        presents_groups[p_shape].append(i)
        
    # Convert to list of (shape, count)
    # Note: We use a list here because order matters (largest first)
    presents_to_pack = [(shape, len(indices)) for shape, indices in presents_groups.items()]
    
    # Grid: 0 = Empty, 1 = Occupied
    grid = [[0] * width for _ in range(length)]
    
    # Pre-calculate grid dimensions for speed
    GRID_W = width
    GRID_L = length

    def find_first_empty():
        for r in range(GRID_L):
            cols = grid[r]
            for c in range(GRID_W):
                if cols[c] == 0:
                    return r, c
        return None

    def can_place(r_start, c_start, shape):
        for dr, dc in shape:
            r, c = r_start + dr, c_start + dc
            if not (0 <= r < GRID_L and 0 <= c < GRID_W):
                return False
            if grid[r][c] != 0:
                return False
        return True

    def place(r_start, c_start, shape, val):
        for dr, dc in shape:
            grid[r_start + dr][c_start + dc] = val

    def backtrack(group_idx):
        # Base case: All groups processed
        if group_idx >= len(presents_to_pack):
            return True

        canonical_shape, count = presents_to_pack[group_idx]

        # Optimization: If we ran out of this shape, move to next
        if count == 0:
            return backtrack(group_idx + 1)

        # Find anchor for the next piece
        empty_cell = find_first_empty()
        
        # If no empty cell but we still have items, fail
        if empty_cell is None:
            return False # Still have 'count' items to place but no space
        
        r_empty, c_empty = empty_cell
        
        # Try to place ONE instance of current shape covering the anchor
        possible_orientations = unique_transformations[canonical_shape]
        
        for orientation in possible_orientations:
            # We must cover (r_empty, c_empty).
            # The orientation has cells (dr, dc).
            # If we place the shape at (r_start, c_start), then (r_start+dr, c_start+dc) must equal (r_empty, c_empty)
            # Therefore: r_start = r_empty - dr
            
            for dr_anchor, dc_anchor in orientation:
                r_start = r_empty - dr_anchor
                c_start = c_empty - dc_anchor
                
                # Pruning: Basic bounds check before expensive can_place
                # Top-left of shape bounding box is roughly (r_start, c_start). 
                # If r_start is negative, it might still be valid if shape has negative coords?
                # But our shapes are normalized to (0,0). So r_start cannot be > r_empty.
                
                if can_place(r_start, c_start, orientation):
                    place(r_start, c_start, orientation, 1)
                    
                    # Decrement count and recurse
                    presents_to_pack[group_idx] = (canonical_shape, count - 1)
                    
                    if backtrack(group_idx):
                        return True
                    
                    # Backtrack
                    place(r_start, c_start, orientation, 0)
                    presents_to_pack[group_idx] = (canonical_shape, count)

        # Crucial for Exact Cover / Tiling logic:
        # If we cannot cover the *first* empty cell with the *current* largest shape,
        # can we skip this shape group and cover it with a smaller shape later?
        # Only if we are allowed to *not* place this shape right now.
        # But we sorted presents largest to smallest. 
        # If we enforce order, we avoid combinatorial explosion of "which piece to pick".
        # However, purely enforcing order might miss solutions where a small piece goes in the hole
        # and the big piece goes elsewhere.
        #
        # FIX: The "Anchor" logic requires that *some* piece covers the hole.
        # If the current piece *cannot* cover the hole, we MUST try the next available piece type.
        # We cannot simply return False here. We must try skipping to group_idx + 1 
        # *BUT* only if we haven't skipped placing necessary items.
        # Actually, standard "Knuth's Algorithm X" picks a hole and tries *all* pieces that fit.
        # Our current recursion is "Pick a piece type, then find a hole".
        # Let's align them:
        # 1. Identify hole.
        # 2. Try placing ANY available piece type into that hole.
        
        # To do this efficiently with our data structure:
        # Iterate over all groups that still have count > 0
        
        return False

    # REVISED BACKTRACK: Hole-centric
    def backtrack_hole_centric():
        empty_cell = find_first_empty()
        
        # Success: No holes?
        # Wait, the puzzle is "fit all presents", not "tile the grid perfectly".
        # There might be holes left over!
        # So finding the first empty cell and demanding it be filled is WRONG for this specific puzzle variation
        # if the total area of presents < total area of grid.
        
        # If presents area < grid area, we can leave holes.
        # Strategy switch: "Pick a piece, place it anywhere valid".
        # But that is too slow.
        # Optimized Strategy: "Pick a piece, place it in the first valid spot?"
        # Better: Standard backtracking on the *list of presents*.
        
        return backtrack_presents(0)

    def backtrack_presents(present_idx):
        if present_idx >= len(sorted_presents):
            return True # All placed
            
        current_shape = sorted_presents[present_idx]
        orientations = unique_transformations[current_shape]
        
        # Try to find a spot for this present
        # To optimize, we only check "valid" spots.
        # This is still slow (Grid Size * Orientations * Num Presents).
        # But Grid is small (40x40). 
        
        # Optimization: Find first empty cell? No, we don't have to fill it.
        # Optimization: We just scan the grid for the first valid placement?
        # To make it deterministic and prune duplicates:
        # We can force the placement to be "after" the previous placement if identical shapes?
        
        # Let's try to place this specific present in the first place it fits.
        for r in range(GRID_L):
            for c in range(GRID_W):
                if grid[r][c] == 0:
                    # Try placing here (top-left of shape at r,c)
                    for orientation in orientations:
                        if can_place(r, c, orientation):
                            place(r, c, orientation, 1)
                            if backtrack_presents(present_idx + 1):
                                return True
                            place(r, c, orientation, 0)
        return False
        
    return backtrack_presents(0)


def run_solver(input_filename="input.txt"):
    start_time = time.perf_counter_ns()
    
    shapes, regions = read_input(input_filename)
    
    if not regions:
        print("Warning: No regions found in input.")
    
    # Pre-calculate transformations
    unique_transformations = {}
    for canonical_shape in shapes.values():
        unique_transformations[canonical_shape] = generate_transformations(canonical_shape)

    fits_count = 0
    
    for i, region in enumerate(regions):
        width = region['width']
        length = region['length']
        presents = region['presents']
        
        # Area Check
        total_present_area = sum(len(p) for p in presents)
        region_area = width * length
        if total_present_area > region_area:
            continue

        if solve_packing(width, length, presents, unique_transformations):
            fits_count += 1
    
    end_time = time.perf_counter_ns()
    duration_ms = (end_time - start_time) / 1_000_000.0

    print(f"Puzzle 1: {fits_count}")
    print(f"Total Duration: {duration_ms:.2f}ms")

if __name__ == "__main__":
    run_solver()