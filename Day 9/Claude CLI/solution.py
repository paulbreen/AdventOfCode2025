#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 9: Movie Theater
Solves both puzzles using the same input data.
"""

import time
from typing import List, Tuple, Set

def read_input(filename: str) -> List[Tuple[int, int]]:
    """Read red tile coordinates from input file."""
    with open(filename, 'r') as f:
        tiles = []
        for line in f:
            line = line.strip()
            if line:
                x, y = line.split(',')
                tiles.append((int(x), int(y)))
    return tiles

def calculate_rectangle_area(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculate the area of a rectangle formed by two opposite corners."""
    width = abs(p2[0] - p1[0])
    height = abs(p2[1] - p1[1])
    return width * height

def solve_puzzle1(red_tiles: List[Tuple[int, int]]) -> int:
    """
    Find the largest rectangle that can be formed using any two red tiles
    as opposite corners.
    """
    max_area = 0
    n = len(red_tiles)

    # Check all pairs of red tiles
    for i in range(n):
        for j in range(i + 1, n):
            area = calculate_rectangle_area(red_tiles[i], red_tiles[j])
            max_area = max(max_area, area)

    return max_area

def get_line_points(p1: Tuple[int, int], p2: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """
    Get all points on a line between p1 and p2 (inclusive).
    Uses Bresenham's line algorithm for diagonal lines, simple iteration for axis-aligned.
    """
    points = set()
    x1, y1 = p1
    x2, y2 = p2

    # Check if line is horizontal or vertical
    if x1 == x2:
        # Vertical line
        for y in range(min(y1, y2), max(y1, y2) + 1):
            points.add((x1, y))
    elif y1 == y2:
        # Horizontal line
        for x in range(min(x1, x2), max(x1, x2) + 1):
            points.add((x, y1))
    else:
        # Diagonal line - use Bresenham's algorithm
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        x, y = x1, y1

        while True:
            points.add((x, y))
            if x == x2 and y == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    return points

def point_in_polygon(point: Tuple[int, int], polygon: List[Tuple[int, int]]) -> bool:
    """
    Check if a point is inside a polygon using ray casting algorithm.
    """
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def point_on_polygon_edge(point: Tuple[int, int], red_tiles: List[Tuple[int, int]]) -> bool:
    """
    Check if a point is on the edge of the polygon formed by red tiles.
    """
    n = len(red_tiles)
    for i in range(n):
        p1 = red_tiles[i]
        p2 = red_tiles[(i + 1) % n]

        # Check if point is on the line segment between p1 and p2
        x, y = point
        x1, y1 = p1
        x2, y2 = p2

        # Check if point is within bounding box of segment
        if not (min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)):
            continue

        # Check if point is on the line
        if x1 == x2:  # Vertical line
            if x == x1:
                return True
        elif y1 == y2:  # Horizontal line
            if y == y1:
                return True
        else:  # Diagonal line - check using cross product
            # Vector from p1 to point
            dx1 = x - x1
            dy1 = y - y1
            # Vector from p1 to p2
            dx2 = x2 - x1
            dy2 = y2 - y1
            # Cross product should be 0 if collinear
            if abs(dx1 * dy2 - dy1 * dx2) == 0:
                return True

    return False

def is_red_or_green(point: Tuple[int, int], red_tiles_set: Set[Tuple[int, int]],
                     red_tiles_list: List[Tuple[int, int]]) -> bool:
    """
    Check if a point is either red or green (on polygon edge or inside polygon).
    """
    # Check if it's a red tile
    if point in red_tiles_set:
        return True

    # Check if it's on the polygon edge (green)
    if point_on_polygon_edge(point, red_tiles_list):
        return True

    # Check if it's inside the polygon (green)
    if point_in_polygon(point, red_tiles_list):
        return True

    return False

def rectangle_contains_only_red_or_green(
    p1: Tuple[int, int],
    p2: Tuple[int, int],
    red_tiles_set: Set[Tuple[int, int]],
    red_tiles_list: List[Tuple[int, int]]
) -> bool:
    """
    Check if all tiles in the rectangle formed by p1 and p2
    are either red or green.
    """
    min_x = min(p1[0], p2[0])
    max_x = max(p1[0], p2[0])
    min_y = min(p1[1], p2[1])
    max_y = max(p1[1], p2[1])

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if not is_red_or_green((x, y), red_tiles_set, red_tiles_list):
                return False

    return True

def solve_puzzle2(red_tiles: List[Tuple[int, int]]) -> int:
    """
    Find the largest rectangle that can be formed using two red tiles
    as opposite corners, where the rectangle only contains red or green tiles.
    """
    red_tiles_set = set(red_tiles)
    n = len(red_tiles)

    # Create a cache for is_red_or_green checks
    cache = {}

    def is_red_or_green_cached(point: Tuple[int, int]) -> bool:
        if point not in cache:
            cache[point] = is_red_or_green(point, red_tiles_set, red_tiles)
        return cache[point]

    def rectangle_contains_only_red_or_green_cached(p1: Tuple[int, int], p2: Tuple[int, int]) -> bool:
        min_x = min(p1[0], p2[0])
        max_x = max(p1[0], p2[0])
        min_y = min(p1[1], p2[1])
        max_y = max(p1[1], p2[1])

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if not is_red_or_green_cached((x, y)):
                    return False
        return True

    # Generate all pairs with their areas and sort by area descending
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            area = calculate_rectangle_area(red_tiles[i], red_tiles[j])
            pairs.append((area, i, j))

    pairs.sort(reverse=True)

    # Check pairs in descending order of area
    max_area = 0
    MAX_POINTS_TO_CHECK = 500000  # Limit rectangle size for performance

    for area, i, j in pairs:
        # If this area can't beat current max, we're done
        if area <= max_area:
            break

        # Skip rectangles that are too large to check efficiently
        if area > MAX_POINTS_TO_CHECK:
            continue

        if rectangle_contains_only_red_or_green_cached(red_tiles[i], red_tiles[j]):
            max_area = area
            break  # Found the largest, no need to continue

    return max_area

def main():
    """Main function to solve both puzzles and display results."""
    start_time = time.time()

    # Read input
    red_tiles = read_input('input.txt')

    # Solve Puzzle 1
    puzzle1_start = time.time()
    result1 = solve_puzzle1(red_tiles)
    puzzle1_time = time.time() - puzzle1_start

    # Solve Puzzle 2
    puzzle2_start = time.time()
    result2 = solve_puzzle2(red_tiles)
    puzzle2_time = time.time() - puzzle2_start

    # Calculate total duration
    total_duration = (time.time() - start_time) * 1000  # Convert to milliseconds

    # Display results
    print(f"Puzzle 1: {result1}")
    print(f"Puzzle 2: {result2}")
    print(f"Total Duration: {total_duration:.2f}ms")

if __name__ == "__main__":
    main()
