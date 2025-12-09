#!/usr/bin/env python3
import time
import sys
import os

# ---------------------------------------
# Utility: Point-in-polygon (ray casting)
# Optimized for axis-aligned vertices
# ---------------------------------------
def point_in_poly(x, y, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % n]

        # Check intersection with horizontal ray
        if ((y1 > y) != (y2 > y)):
            # Compute intersection X coordinate
            xinters = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xinters > x:
                inside = not inside

    return inside

# ---------------------------------------
# Rectangle fully inside polygon?
# For orthogonal polygons, checking 4 corners suffices.
# ---------------------------------------
def rect_inside_polygon(x1, y1, x2, y2, poly):
    lx = min(x1, x2)
    hx = max(x1, x2)
    ly = min(y1, y2)
    hy = max(y1, y2)

    return (
        point_in_poly(lx, ly, poly) and
        point_in_poly(lx, hy, poly) and
        point_in_poly(hx, ly, poly) and
        point_in_poly(hx, hy, poly)
    )

# ---------------------------------------
# Load input coordinates
# ---------------------------------------
def load_coords(path):
    coords = []
    with open(path) as f:
        for line in f:
            if line.strip():
                x, y = map(int, line.split(','))
                coords.append((x, y))
    return coords

def main():
    if not os.path.exists("input.txt"):
        print("Missing input.txt", file=sys.stderr)
        sys.exit(1)

    reds = load_coords("input.txt")

    # Puzzle 1
    t1 = time.time()
    max_area_1 = 0
    n = len(reds)

    for i in range(n):
        x1, y1 = reds[i]
        for j in range(i+1, n):
            x2, y2 = reds[j]
            area = abs(x1 - x2) * abs(y1 - y2)
            if area > max_area_1:
                max_area_1 = area

    t1_end = time.time()

    # Puzzle 2
    # Build polygon in given order = input order
    polygon = reds

    t2 = time.time()
    max_area_2 = 0

    for i in range(n):
        x1, y1 = reds[i]
        for j in range(i+1, n):
            x2, y2 = reds[j]
            area = abs(x1 - x2) * abs(y1 - y2)
            if area <= max_area_2:
                continue
            if rect_inside_polygon(x1, y1, x2, y2, polygon):
                max_area_2 = area

    t2_end = time.time()

    total_ms = int((t2_end - t1) * 1000)

    print(f"Puzzle 1: {max_area_1}")
    print(f"Puzzle 2: {max_area_2}")
    print(f"Total Duration: {total_ms}ms")


if __name__ == "__main__":
    main()
