#!/usr/bin/env python3
"""
Day 11: Reactor - Diagnostic Version
Shows progress and statistics while solving.
"""

import sys
import time
from typing import Dict, List, Set


def parse_graph(filename: str) -> Dict[str, List[str]]:
    """Parse the input file into a directed graph (adjacency list)."""
    graph = {}
    try:
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
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


# Global counter for progress tracking
path_counter = 0
last_report_time = time.time()


def count_paths_with_progress(graph: Dict[str, List[str]], start: str, end: str,
                               visited: Set[str] = None, depth: int = 0) -> int:
    """Count all paths with progress reporting."""
    global path_counter, last_report_time

    if visited is None:
        visited = set()

    # Base case: reached the destination
    if start == end:
        path_counter += 1
        current_time = time.time()
        if current_time - last_report_time > 5:  # Report every 5 seconds
            print(f"Progress: Found {path_counter:,} paths so far... (depth: {depth})")
            last_report_time = current_time
        return 1

    # If start node has no outgoing edges or already visited, no path
    if start not in graph or start in visited:
        return 0

    # Mark current node as visited
    visited.add(start)

    total_paths = 0

    # Explore all neighbors
    for neighbor in graph[start]:
        total_paths += count_paths_with_progress(graph, neighbor, end, visited, depth + 1)

    # Backtrack
    visited.remove(start)

    return total_paths


def analyze_graph(graph: Dict[str, List[str]]):
    """Print graph statistics."""
    print("\n=== GRAPH ANALYSIS ===")
    print(f"Total nodes: {len(graph)}")

    # Count edges
    total_edges = sum(len(destinations) for destinations in graph.values())
    print(f"Total edges: {total_edges}")

    # Average branching factor
    avg_branching = total_edges / len(graph) if graph else 0
    print(f"Average branching factor: {avg_branching:.2f}")

    # Find nodes with high branching
    high_branch = [(node, len(dests)) for node, dests in graph.items() if len(dests) > 10]
    if high_branch:
        print(f"\nNodes with >10 outgoing edges: {len(high_branch)}")
        for node, count in sorted(high_branch, key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {node}: {count} edges")

    # Check if start and end nodes exist
    print(f"\nKey nodes:")
    print(f"  'you' exists: {'you' in graph}")
    print(f"  'svr' exists: {'svr' in graph}")
    print(f"  'out' exists in values: {any('out' in dests for dests in graph.values())}")
    print(f"  'dac' exists: {'dac' in graph}")
    print(f"  'fft' exists: {'fft' in graph}")
    print("=" * 50)


def main():
    """Main execution function."""
    global path_counter, last_report_time

    print("Parsing graph...")
    graph = parse_graph('input.txt')

    analyze_graph(graph)

    print("\n=== SOLVING PUZZLE 1 ===")
    print("Counting paths from 'you' to 'out'...\n")

    path_counter = 0
    last_report_time = time.time()
    start_time = time.time()

    result1 = count_paths_with_progress(graph, 'you', 'out')
    elapsed = time.time() - start_time

    print(f"\nPuzzle 1 complete!")
    print(f"Result: {result1:,} paths")
    print(f"Time: {elapsed:.2f} seconds")

    print("\n=== SOLVING PUZZLE 2 ===")
    print("Counting paths from 'svr' to 'out'...")
    print("(Will count all paths, then filter for those visiting 'dac' and 'fft')\n")

    path_counter = 0
    last_report_time = time.time()
    start_time = time.time()

    result2_all = count_paths_with_progress(graph, 'svr', 'out')
    elapsed = time.time() - start_time

    print(f"\nAll paths from 'svr' to 'out': {result2_all:,}")
    print(f"Time: {elapsed:.2f} seconds")
    print("\nNow testing paths with required nodes...")


if __name__ == "__main__":
    main()
