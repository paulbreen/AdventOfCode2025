#!/usr/bin/env python3
"""Quick test of Puzzle 2 with progress."""

import sys
import time
from typing import Dict, List, Set

def parse_graph(filename: str) -> Dict[str, List[str]]:
    """Parse the input file."""
    graph = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(': ')
            if len(parts) != 2:
                continue
            source = parts[0].strip()
            destinations = parts[1].strip().split()
            graph[source] = destinations
    return graph

path_counter = 0
last_report = time.time()

def count_paths(graph, start, end, visited=None, depth=0):
    """Count paths with progress."""
    global path_counter, last_report

    if visited is None:
        visited = set()

    if start == end:
        path_counter += 1
        now = time.time()
        if now - last_report >= 1:  # Report every second
            print(f"Found {path_counter:,} paths (depth {depth})...", flush=True)
            last_report = now
        return 1

    if start not in graph or start in visited:
        return 0

    visited.add(start)
    total = 0

    for neighbor in graph[start]:
        total += count_paths(graph, neighbor, end, visited, depth + 1)

    visited.remove(start)
    return total

print("Loading graph...", flush=True)
graph = parse_graph('input.txt')

print(f"Graph has {len(graph)} nodes", flush=True)
print(f"Starting search from 'svr' to 'out'...", flush=True)
print("Progress will be shown every second.\n", flush=True)

start_time = time.time()
result = count_paths(graph, 'svr', 'out')
elapsed = time.time() - start_time

print(f"\n=== COMPLETE ===", flush=True)
print(f"Total paths: {result:,}", flush=True)
print(f"Time: {elapsed:.2f} seconds", flush=True)
