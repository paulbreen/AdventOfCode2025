#!/usr/bin/env python3
"""
Day 11: Reactor - Puzzle Solver

Puzzle 1:
  Count all paths from 'you' to 'out'. :contentReference[oaicite:1]{index=1}

Puzzle 2:
  Count all paths from 'svr' to 'out' that visit both 'dac' and 'fft'. :contentReference[oaicite:2]{index=2}
"""

import sys
import time
from functools import lru_cache
from typing import Dict, List, Tuple

Graph = Dict[str, List[str]]


def parse_graph(path: str) -> Graph:
    """
    Parse the input file into an adjacency list.

    Each line: NAME: child1 child2 ...
    Nodes that only appear as children will not have entries,
    but graph.get(name, []) handles that safely.
    """
    graph: Graph = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line:
                    continue
                name, rest = line.split(":", 1)
                name = name.strip()
                outs = rest.strip().split()
                graph[name] = outs
    except FileNotFoundError:
        print(f"Error: input file '{path}' not found.", file=sys.stderr)
        sys.exit(1)
    return graph


def solve_puzzle1(graph: Graph) -> int:
    """
    Puzzle 1:
    Count all distinct paths from 'you' to 'out'.

    The subgraph reachable from 'you' is a DAG in this input, so
    a simple DFS with memoization by node is correct and efficient. :contentReference[oaicite:3]{index=3}
    """
    start = "you"
    target = "out"

    if start not in graph:
        raise ValueError(f"Start node '{start}' not found in graph")

    @lru_cache(maxsize=None)
    def count_paths(node: str) -> int:
        total = 0
        for nxt in graph.get(node, []):
            if nxt == target:
                total += 1
            else:
                total += count_paths(nxt)
        return total

    return count_paths(start)


def solve_puzzle2(graph: Graph) -> int:
    """
    Puzzle 2:
    Count all paths from 'svr' to 'out' that visit both 'dac' and 'fft'
    (in any order). :contentReference[oaicite:4]{index=4}

    We track two booleans:
      seen_dac: have we visited 'dac' on this path so far?
      seen_fft: have we visited 'fft' on this path so far?

    State = (node, seen_dac, seen_fft), memoized to avoid recomputation.
    DFS returns (total_paths, valid_paths_with_both).
    We only need valid_paths_with_both for the puzzle answer.
    """
    start = "svr"
    target = "out"
    dac = "dac"
    fft = "fft"

    if start not in graph:
        raise ValueError(f"Start node '{start}' not found in graph")

    @lru_cache(maxsize=None)
    def dfs(node: str, seen_dac: bool, seen_fft: bool) -> Tuple[int, int]:
        total = 0
        valid = 0

        for nxt in graph.get(node, []):
            next_seen_dac = seen_dac or (nxt == dac)
            next_seen_fft = seen_fft or (nxt == fft)

            if nxt == target:
                # We've reached 'out'; count this path, but only mark it
                # as "valid" if both dac and fft have been seen somewhere
                # along the path (including this edge).
                total += 1
                if next_seen_dac and next_seen_fft:
                    valid += 1
            else:
                t_sub, v_sub = dfs(nxt, next_seen_dac, next_seen_fft)
                total += t_sub
                valid += v_sub

        return total, valid

    _, valid_paths = dfs(start, False, False)
    return valid_paths


def main(argv=None) -> None:
    """
    Entry point.

    Usage:
        python3 solve.py            # uses 'input.txt' in current directory
        python3 solve.py path/to/input.txt
    """
    if argv is None:
        argv = sys.argv[1:]

    input_path = argv[0] if argv else "input.txt"
    graph = parse_graph(input_path)

    t0 = time.perf_counter()
    p1 = solve_puzzle1(graph)
    t1 = time.perf_counter()
    p2 = solve_puzzle2(graph)
    t2 = time.perf_counter()

    # Measure per-puzzle durations (in milliseconds)
    puzzle1_ms = (t1 - t0) * 1000.0
    puzzle2_ms = (t2 - t1) * 1000.0
    total_ms = puzzle1_ms + puzzle2_ms

    # Output in the exact required format
    print(f"Puzzle 1: {p1}")
    print(f"Puzzle 2: {p2}")
    print(f"Total Duration: {total_ms:.3f}ms")


if __name__ == "__main__":
    main()
