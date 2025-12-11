#!/usr/bin/env python3
"""
Day 11: Reactor - Graph Path Finding
Finds all paths through a directed graph with optional node constraints.
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

                # Parse format: "node: dest1 dest2 dest3 ..."
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


def count_paths(graph: Dict[str, List[str]], start: str, end: str,
                visited: Set[str] = None) -> int:
    """
    Count all paths from start to end in a directed graph using DFS.
    More memory-efficient than storing all paths.

    Args:
        graph: Adjacency list representation of the graph
        start: Starting node
        end: Target node
        visited: Set of nodes already visited in the current path

    Returns:
        Number of distinct paths
    """
    if visited is None:
        visited = set()

    # Base case: reached the destination
    if start == end:
        return 1

    # If start node has no outgoing edges or already visited, no path
    if start not in graph or start in visited:
        return 0

    # Mark current node as visited
    visited.add(start)

    total_paths = 0

    # Explore all neighbors
    for neighbor in graph[start]:
        total_paths += count_paths(graph, neighbor, end, visited)

    # Backtrack: remove current node from visited
    visited.remove(start)

    return total_paths


def count_paths_with_required_nodes(graph: Dict[str, List[str]], start: str, end: str,
                                     required_nodes: Set[str], visited: Set[str] = None,
                                     found_required: Set[str] = None) -> int:
    """
    Count paths from start to end that visit all required nodes.

    Args:
        graph: Adjacency list representation of the graph
        start: Starting node
        end: Target node
        required_nodes: Set of nodes that must be visited
        visited: Set of nodes already visited in the current path
        found_required: Set of required nodes found so far in this path

    Returns:
        Count of paths visiting all required nodes
    """
    if visited is None:
        visited = set()
    if found_required is None:
        found_required = set()

    # Track if current node is required
    if start in required_nodes:
        found_required = found_required | {start}

    # Base case: reached the destination
    if start == end:
        # Check if we visited all required nodes
        return 1 if found_required == required_nodes else 0

    # If start node has no outgoing edges or already visited, no path
    if start not in graph or start in visited:
        return 0

    # Mark current node as visited
    visited.add(start)

    total_paths = 0

    # Explore all neighbors
    for neighbor in graph[start]:
        total_paths += count_paths_with_required_nodes(
            graph, neighbor, end, required_nodes, visited, found_required
        )

    # Backtrack: remove current node from visited
    visited.remove(start)

    return total_paths


def solve_puzzle1(graph: Dict[str, List[str]]) -> int:
    """
    Puzzle 1: Find all paths from 'you' to 'out'.

    Returns:
        Number of distinct paths
    """
    return count_paths(graph, 'you', 'out')


def solve_puzzle2(graph: Dict[str, List[str]]) -> int:
    """
    Puzzle 2: Find all paths from 'svr' to 'out' that visit both 'dac' and 'fft'.

    Returns:
        Number of paths that visit both required nodes
    """
    required_nodes = {'dac', 'fft'}
    return count_paths_with_required_nodes(graph, 'svr', 'out', required_nodes)


def main():
    """Main execution function."""
    # Parse the input graph
    graph = parse_graph('input.txt')

    # Track total execution time
    start_time = time.time()

    # Solve both puzzles
    result1 = solve_puzzle1(graph)
    result2 = solve_puzzle2(graph)

    # Calculate total duration in milliseconds
    end_time = time.time()
    duration_ms = (end_time - start_time) * 1000

    # Display results in the required format
    print(f"Puzzle 1: {result1}")
    print(f"Puzzle 2: {result2}")
    print(f"Total Duration: {duration_ms:.2f}ms")


if __name__ == "__main__":
    main()
