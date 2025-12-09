import sys
import time

# --- Utility Functions ---

def parse_input(filename):
    """
    Reads the input file and returns a list of (x, y) coordinates for red tiles,
    and a set for O(1) lookup.
    """
    red_tiles = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    x = int(parts[0])
                    y = int(parts[1])
                    red_tiles.append((x, y))
    except FileNotFoundError:
        print(f"Error: Input file '{filename}' not found.", file=sys.stderr)
        sys.exit(1)
    
    red_tile_set = set(red_tiles)
    return red_tiles, red_tile_set

def is_point_on_segment(p, a, b):
    """
    Checks if point p is on the segment defined by a and b.
    Since segments are axis-aligned (a,b on same row or col), we use a simpler check.
    """
    # Check for collinearity (implicitly true since problem guarantees axis-aligned segments)
    # Check if p is within the bounding box of the segment a-b
    return (min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and
            min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))

def is_inside_polygon(point, polygon_vertices):
    """
    Checks if a point is inside or on the boundary of the polygon
    defined by polygon_vertices using the Ray Casting Algorithm.
    The polygon is guaranteed to be axis-aligned by the puzzle constraints.
    """
    x, y = point
    n = len(polygon_vertices)
    inside = False
    
    for i in range(n):
        p1 = polygon_vertices[i]
        p2 = polygon_vertices[(i + 1) % n]
        
        x1, y1 = p1
        x2, y2 = p2
        
        # 1. Check if the point is on the boundary (a red or green tile)
        if is_point_on_segment(point, p1, p2):
            return True

        # 2. Ray Casting algorithm (adapted for horizontal segments/integer grid)
        # Check if the ray (horizontal, positive x-direction) from the point
        # intersects the segment p1-p2.
        
        # Segment must be non-horizontal and straddle the point's y-coordinate
        if (y1 <= y < y2) or (y2 <= y < y1):
            # Calculate intersection x-coordinate
            # Formula: x_intersect = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if y1 != y2:
                x_intersect = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                
                # If the intersection point is to the right of the test point
                if x_intersect > x:
                    inside = not inside
                    
    return inside

# --- Puzzle 1 Solver ---

def solve_puzzle_1(red_tiles):
    """
    Finds the largest rectangle using two red tiles as opposite corners.
    Complexity: O(N^2)
    """
    max_area = 0
    N = len(red_tiles)
    
    # Iterate over all unique pairs of red tiles
    for i in range(N):
        for j in range(i + 1, N):
            p1 = red_tiles[i]
            p2 = red_tiles[j]
            
            x1, y1 = p1
            x2, y2 = p2
            
            # The tiles must not be on the same row or column to form a non-zero area rectangle
            if x1 != x2 and y1 != y2:
                area = abs(x2 - x1) * abs(y2 - y1)
                max_area = max(max_area, area)
                
    return max_area

# --- Puzzle 2 Solver ---

def solve_puzzle_2(red_tiles, red_tile_set):
    """
    Finds the largest rectangle with red-tile opposite corners, where all tiles
    inside the rectangle must be red or green (i.e., the rectangle is fully
    contained within the polygon).
    Complexity: O(N^3)
    """
    max_area = 0
    N = len(red_tiles)
    
    # We iterate over all unique pairs of red tiles (p1, p2) as opposite corners
    for i in range(N):
        for j in range(i + 1, N):
            p1 = red_tiles[i]
            p2 = red_tiles[j]
            
            x1, y1 = p1
            x2, y2 = p2
            
            # The tiles must not be on the same row or column
            if x1 == x2 or y1 == y2:
                continue
                
            # The two other corners of the potential rectangle
            p3 = (x1, y2)
            p4 = (x2, y1)
            
            # The red tiles are the vertices, and the polygon is composed of the
            # red/green tiles. A rectangle is valid if all its interior points
            # are red/green. This is true if and only if the rectangle is fully
            # contained within the polygon defined by the red vertices.
            
            # Since p1 and p2 are red (on the boundary), we only need to check
            # if the other two corners (p3 and p4) are on the boundary (red/green)
            # or inside (green) the polygon.
            
            # If a corner is a red tile, it is automatically valid.
            is_p3_valid = p3 in red_tile_set or is_inside_polygon(p3, red_tiles)
            is_p4_valid = p4 in red_tile_set or is_inside_polygon(p4, red_tiles)
            
            if is_p3_valid and is_p4_valid:
                area = abs(x2 - x1) * abs(y2 - y1)
                max_area = max(max_area, area)
                
    return max_area

# --- Main Execution ---

def main():
    start_time = time.time()
    
    # 1. Parse Input
    red_tiles, red_tile_set = parse_input('input.txt')
    
    # 2. Solve Puzzle 1
    p1_start = time.time()
    result_1 = solve_puzzle_1(red_tiles)
    p1_duration = (time.time() - p1_start) * 1000
    
    # 3. Solve Puzzle 2
    p2_start = time.time()
    # Note: red_tiles is already a list of vertices in order
    result_2 = solve_puzzle_2(red_tiles, red_tile_set)
    p2_duration = (time.time() - p2_start) * 1000
    
    total_duration = (time.time() - start_time) * 1000
    
    # 4. Display Results
    print(f"Puzzle 1: {result_1}")
    print(f"Puzzle 2: {result_2}")
    print(f"Total Duration: {total_duration:.2f}ms")

if __name__ == "__main__":
    main()