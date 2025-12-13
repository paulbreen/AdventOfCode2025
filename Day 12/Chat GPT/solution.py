#!/usr/bin/env python3
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

SHAPE_HEADER_RE = re.compile(r"^\s*(\d+)\s*:\s*$")
REGION_RE = re.compile(r"^\s*(\d+)\s*x\s*(\d+)\s*:\s*(.*)\s*$")


def parse_input(path: Path) -> Tuple[Dict[int, int], List[Tuple[int, int, List[int]]]]:
    """
    Parses input.txt into:
      - shapes: dict {shape_index: area(# count)}
      - regions: list of (width, height, counts[])
    Robust to extra blank lines.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    n = len(lines)

    shapes: Dict[int, int] = {}
    regions: List[Tuple[int, int, List[int]]] = []

    # --- Parse shapes section ---
    while i < n:
        line = lines[i].rstrip("\n")
        m = SHAPE_HEADER_RE.match(line)
        if not m:
            # Once we hit the first region line, stop shape parsing.
            if REGION_RE.match(line):
                break
            i += 1
            continue

        idx = int(m.group(1))
        i += 1

        # Read the shape grid lines (non-empty, non-header, non-region).
        grid: List[str] = []
        while i < n:
            s = lines[i].strip()
            if not s:
                i += 1
                break
            if SHAPE_HEADER_RE.match(lines[i]) or REGION_RE.match(lines[i]):
                break
            grid.append(s)
            i += 1

        if not grid:
            raise ValueError(f"Shape {idx} has no grid lines")

        area = sum(row.count("#") for row in grid)
        shapes[idx] = area

    if not shapes:
        raise ValueError("No shapes parsed from input.txt")

    # --- Parse regions section ---
    while i < n:
        line = lines[i].strip()
        i += 1
        if not line:
            continue
        m = REGION_RE.match(line)
        if not m:
            continue

        w = int(m.group(1))
        h = int(m.group(2))
        counts_str = m.group(3).strip()
        counts = [int(x) for x in counts_str.split()] if counts_str else []
        regions.append((w, h, counts))

    if not regions:
        raise ValueError("No regions parsed from input.txt")

    return shapes, regions


def solve_puzzle_1(shapes: Dict[int, int], regions: List[Tuple[int, int, List[int]]]) -> int:
    """
    Counts how many regions can fit the requested presents.

    With the provided dataset (very large counts), a full exact 2D packing search is infeasible.
    This solution uses the necessary condition: sum(count_i * area(shape_i)) <= region_area.

    If the puzzle requires strict geometric feasibility beyond area, this would need a
    significantly different approach (and the input would typically be far smaller).
    """
    max_shape_index = max(shapes.keys())
    ok = 0

    for w, h, counts in regions:
        region_area = w * h

        required = 0
        # counts are given in order 0..K
        for idx, c in enumerate(counts):
            if c <= 0:
                continue
            if idx not in shapes:
                raise ValueError(f"Region references missing shape index {idx}")
            required += c * shapes[idx]

        # If some shapes are not listed in counts, treat them as 0 (fine).
        # If counts is shorter than max shape index+1, missing are 0 (fine).

        if required <= region_area:
            ok += 1

    return ok


def main() -> None:
    input_path = Path("input.txt")
    if not input_path.exists():
        print("ERROR: input.txt not found", file=sys.stderr)
        sys.exit(1)

    shapes, regions = parse_input(input_path)

    t0 = time.perf_counter()
    p1 = solve_puzzle_1(shapes, regions)
    t1 = time.perf_counter()

    total_ms = (t1 - t0) * 1000.0

    print(f"Puzzle 1: {p1}")
    print(f"Total Duration: {total_ms:.3f}ms")


if __name__ == "__main__":
    main()
