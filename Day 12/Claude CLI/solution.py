import time
from typing import List, Tuple, Set

def parse_input(filename: str):
    """Parse the input file to extract shapes and regions."""
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    # Parse shapes
    shapes = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        # Check if this is a shape definition line (number followed by colon)
        if line and ':' in line:
            # Check if it's a shape ID line (not a region line with 'x')
            if 'x' not in line.split(':')[0]:
                shape_id = int(line.split(':')[0])
                shape_lines = []
                i += 1
                # Read shape pattern lines
                while i < len(lines) and lines[i] and lines[i][0] in '#.':
                    shape_lines.append(lines[i])
                    i += 1
                shapes[shape_id] = shape_lines
                continue
            else:
                # This is a region line, stop parsing shapes
                break
        i += 1

    # Parse regions
    regions = []
    for line in lines:
        if line and 'x' in line and ':' in line:
            parts = line.split(': ')
            if len(parts) == 2:
                dims = parts[0].split('x')
                if len(dims) == 2:
                    try:
                        width, height = int(dims[0]), int(dims[1])
                        counts = list(map(int, parts[1].split()))
                        regions.append((width, height, counts))
                    except ValueError:
                        pass

    return shapes, regions

def shape_to_coords(shape_lines: List[str]) -> List[Tuple[int, int]]:
    """Convert shape lines to set of coordinates (relative to top-left)."""
    coords = []
    for y, line in enumerate(shape_lines):
        for x, char in enumerate(line):
            if char == '#':
                coords.append((x, y))
    return coords

def normalize_coords(coords: List[Tuple[int, int]]) -> Tuple[Tuple[int, int], ...]:
    """Normalize coordinates so min x and y are 0."""
    if not coords:
        return tuple()
    min_x = min(x for x, y in coords)
    min_y = min(y for x, y in coords)
    normalized = tuple(sorted((x - min_x, y - min_y) for x, y in coords))
    return normalized

def rotate_90(coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Rotate coordinates 90 degrees clockwise."""
    return [(-y, x) for x, y in coords]

def flip_horizontal(coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Flip coordinates horizontally."""
    return [(-x, y) for x, y in coords]

def get_all_orientations(shape_lines: List[str]) -> Set[Tuple[Tuple[int, int], ...]]:
    """Get all unique orientations of a shape (rotations and flips)."""
    coords = shape_to_coords(shape_lines)
    orientations = set()

    # Try all rotations
    current = coords
    for _ in range(4):
        orientations.add(normalize_coords(current))
        current = rotate_90(current)

    # Try all rotations of flipped version
    current = flip_horizontal(coords)
    for _ in range(4):
        orientations.add(normalize_coords(current))
        current = rotate_90(current)

    return orientations

def can_place(grid: Set[Tuple[int, int]], shape: Tuple[Tuple[int, int], ...],
              x: int, y: int, width: int, height: int) -> bool:
    """Check if shape can be placed at position (x, y)."""
    for dx, dy in shape:
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= width or ny < 0 or ny >= height:
            return False
        if (nx, ny) in grid:
            return False
    return True

def place_shape(grid: Set[Tuple[int, int]], shape: Tuple[Tuple[int, int], ...],
                x: int, y: int) -> None:
    """Place shape on grid at position (x, y)."""
    for dx, dy in shape:
        grid.add((x + dx, y + dy))

def remove_shape(grid: Set[Tuple[int, int]], shape: Tuple[Tuple[int, int], ...],
                 x: int, y: int) -> None:
    """Remove shape from grid at position (x, y)."""
    for dx, dy in shape:
        grid.discard((x + dx, y + dy))

def solve_region(width: int, height: int, presents: List[Tuple[int, Set[Tuple[Tuple[int, int], ...]]]],
                 grid: Set[Tuple[int, int]], index: int) -> bool:
    """Recursively try to place all presents using backtracking."""
    if index == len(presents):
        return True  # All presents placed successfully

    shape_id, orientations = presents[index]

    # Try each orientation
    for orientation in orientations:
        # Try each position in the grid
        for y in range(height):
            for x in range(width):
                if can_place(grid, orientation, x, y, width, height):
                    place_shape(grid, orientation, x, y)
                    if solve_region(width, height, presents, grid, index + 1):
                        return True
                    remove_shape(grid, orientation, x, y)

    return False

def can_fit_presents(width: int, height: int, shape_counts: List[int],
                     shape_orientations: dict) -> bool:
    """Check if all presents can fit in the region."""
    # Build list of presents to place
    presents = []
    for shape_id, count in enumerate(shape_counts):
        for _ in range(count):
            presents.append((shape_id, shape_orientations[shape_id]))

    # Check if total area is feasible
    total_area_needed = sum(len(list(shape_orientations[sid])[0]) * count
                           for sid, count in enumerate(shape_counts))
    if total_area_needed > width * height:
        return False

    # Try to solve using backtracking
    grid = set()
    return solve_region(width, height, presents, grid, 0)

def solve_puzzle1(shapes: dict, regions: List[Tuple[int, int, List[int]]]) -> int:
    """Solve puzzle 1: count how many regions can fit all presents."""
    # Precompute all orientations for each shape
    shape_orientations = {}
    for shape_id, shape_lines in shapes.items():
        shape_orientations[shape_id] = get_all_orientations(shape_lines)

    count = 0
    for i, (width, height, shape_counts) in enumerate(regions):
        if can_fit_presents(width, height, shape_counts, shape_orientations):
            count += 1

    return count

def solve_puzzle2(shapes: dict, regions: List[Tuple[int, int, List[int]]]) -> int:
    """Solve puzzle 2: Placeholder for when Part 2 is revealed."""
    # Part 2 will be implemented when the puzzle is revealed
    return 0

def main():
    start_time = time.time()

    # Parse input
    shapes, regions = parse_input('input.txt')

    # Solve puzzle 1
    puzzle1_start = time.time()
    result1 = solve_puzzle1(shapes, regions)
    puzzle1_time = time.time() - puzzle1_start

    # Solve puzzle 2 (placeholder)
    puzzle2_start = time.time()
    result2 = solve_puzzle2(shapes, regions)
    puzzle2_time = time.time() - puzzle2_start

    # Calculate total duration
    total_duration = (time.time() - start_time) * 1000  # Convert to ms

    # Display results in required format
    print(f"Puzzle 1: {result1}")
    print(f"Puzzle 2: {result2}")
    print(f"Total Duration: {total_duration:.0f}ms")

if __name__ == "__main__":
    main()
