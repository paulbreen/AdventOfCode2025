#!/usr/bin/env python3
import time
import sys
import os

# Utility: load file safely
def load_input(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing required file: {path}")
    with open(path, "r") as f:
        return [list(line.rstrip("\n")) for line in f]

# Count adjacent @ rolls
def count_neighbors(grid, r, c):
    h, w = len(grid), len(grid[0])
    count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and grid[nr][nc] == "@":
                count += 1
    return count

# Puzzle 1
def puzzle1(grid):
    h, w = len(grid), len(grid[0])
    accessible = 0
    for r in range(h):
        for c in range(w):
            if grid[r][c] == "@":
                if count_neighbors(grid, r, c) < 4:
                    accessible += 1
    return accessible

# Puzzle 2
def puzzle2(grid):
    h, w = len(grid), len(grid[0])
    removed_total = 0

    # Convert to mutable structure
    grid = [row[:] for row in grid]

    # Precompute neighbor counts
    neigh = [[0] * w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if grid[r][c] == "@":
                neigh[r][c] = count_neighbors(grid, r, c)

    # queue of currently accessible rolls
    from collections import deque
    q = deque()

    def try_enqueue(r, c):
        if grid[r][c] == "@" and neigh[r][c] < 4:
            q.append((r, c))
            # mark so we don't enqueue twice
            grid[r][c] = "#"  # temporary mark

    # initialize
    for r in range(h):
        for c in range(w):
            try_enqueue(r, c)

    while q:
        r, c = q.popleft()
        # convert "#" placeholder into actual removal
        if grid[r][c] != "#" and grid[r][c] != "@":
            continue
        grid[r][c] = "."  # remove roll
        removed_total += 1

        # update neighbors
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w:
                    if neigh[nr][nc] > 0:
                        # lost one adjacent roll
                        neigh[nr][nc] = max(0, neigh[nr][nc] - 1)

                    # If it's still an @ roll, check accessibility
                    if grid[nr][nc] == "@":
                        if neigh[nr][nc] < 4:
                            try_enqueue(nr, nc)

    return removed_total


def main():
    input_path = "input.txt"

    grid = load_input(input_path)

    # Puzzle 1
    start1 = time.time()
    p1 = puzzle1(grid)
    end1 = time.time()

    # Puzzle 2
    start2 = time.time()
    p2 = puzzle2(grid)
    end2 = time.time()

    total_ms = int((end1 - start1 + end2 - start2) * 1000)

    print(f"Puzzle 1: {p1}")
    print(f"Puzzle 2: {p2}")
    print(f"Total Duration: {total_ms}ms")


if __name__ == "__main__":
    main()
