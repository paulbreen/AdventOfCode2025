#!/usr/bin/env python3
import time
import sys
from collections import deque

def load_input(path):
    try:
        with open(path, "r") as f:
            return [list(line.rstrip("\n")) for line in f]
    except FileNotFoundError:
        print(f"Missing input file: {path}")
        sys.exit(1)

# Puzzle 1: Count beam splitting events
def puzzle1(grid):
    R, C = len(grid), len(grid[0])

    # Locate S
    start_col = None
    for c in range(C):
        if grid[0][c] == "S":
            start_col = c
            break

    q = deque()
    # State = (r, c)
    q.append((1, start_col))

    visited = set()
    splits = 0

    while q:
        r, c = q.popleft()
        if r < 0 or r >= R or c < 0 or c >= C:
            continue
        if (r, c) in visited:
            continue
        visited.add((r, c))

        cell = grid[r][c]
        if cell == "^":
            splits += 1
            # new beams left/right
            if c - 1 >= 0:
                q.append((r + 1, c - 1))
            if c + 1 < C:
                q.append((r + 1, c + 1))
        else:
            q.append((r + 1, c))

    return splits

# Puzzle 2: Quantum timelines = 2^(number of reachable splitters)
def puzzle2(grid):
    R, C = len(grid), len(grid[0])

    # Locate S
    start_col = None
    for c in range(C):
        if grid[0][c] == "S":
            start_col = c
            break

    q = deque()
    q.append((1, start_col))
    visited = set()
    reachable_splitters = set()

    while q:
        r, c = q.popleft()
        if r < 0 or r >= R or c < 0 or c >= C:
            continue
        if (r, c) in visited:
            continue
        visited.add((r, c))

        cell = grid[r][c]
        if cell == "^":
            reachable_splitters.add((r, c))
            # both branches are taken in a quantum manifold
            if c - 1 >= 0:
                q.append((r + 1, c - 1))
            if c + 1 < C:
                q.append((r + 1, c + 1))
        else:
            q.append((r + 1, c))

    # timelines = 2^(number of encountered splitters)
    return pow(2, len(reachable_splitters))

def main():
    grid = load_input("input.txt")

    t0 = time.time()
    ans1 = puzzle1(grid)
    t1 = time.time()
    ans2 = puzzle2(grid)
    t2 = time.time()

    print(f"Puzzle 1: {ans1}")
    print(f"Puzzle 2: {ans2}")
    print(f"Total Duration: {int((t2 - t0) * 1000)}ms")

if __name__ == "__main__":
    main()
