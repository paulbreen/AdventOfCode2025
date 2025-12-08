import sys
import time
import math
from collections import defaultdict

# --- Data Structures and Utilities ---

class DSU:
    """Disjoint Set Union (Union-Find) structure for tracking circuits."""
    def __init__(self, size):
        # Parent array for Union-Find: parent[i] is the parent of node i
        # Initially, every node is its own parent
        self.parent = list(range(size))
        # Rank/size array for optimization: rank[i] is the size of the set containing i
        # Initially, every set has a size of 1
        self.size = [1] * size
        # Stores the current number of disjoint sets (circuits)
        self.num_sets = size

    def find(self, i):
        """Find the representative (root) of the set containing i (with path compression)."""
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        """Unite the sets containing i and j (union by size)."""
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # Union by size: attach smaller tree to larger tree
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i # Swap to ensure root_i is the larger set

            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            self.num_sets -= 1
            return True # Connection made, sets were different
        return False # Connection not made, sets were already the same

    def get_circuit_sizes(self):
        """Returns a list of the sizes of all current circuits."""
        sizes = []
        for i, p in enumerate(self.parent):
            # Only count the size if 'i' is the root of its set
            if p == i:
                sizes.append(self.size[i])
        return sizes

def calculate_distance(p1, p2):
    """Calculates the squared Euclidean distance between two 3D points (x, y, z).
    Using squared distance avoids the expensive square root operation, which
    is fine for comparison purposes (i.e., finding the closest pairs).
    """
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2

def parse_input(filename="input.txt"):
    """Reads and parses the 3D coordinates from the input file."""
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        points = []
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) == 3:
                try:
                    points.append(tuple(map(int, parts)))
                except ValueError:
                    # Skip lines with non-integer coordinates if any
                    continue
        return points
    except FileNotFoundError:
        print(f"Error: Input file '{filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during file parsing: {e}", file=sys.stderr)
        sys.exit(1)

def get_sorted_edges(points):
    """Calculates all possible distances (edges) between points and sorts them."""
    num_points = len(points)
    edges = []
    
    # Iterate over all unique pairs of points (i, j) where i < j
    for i in range(num_points):
        for j in range(i + 1, num_points):
            dist_sq = calculate_distance(points[i], points[j])
            # Edge format: (squared_distance, index1, index2)
            edges.append((dist_sq, i, j))
            
    # Sort edges primarily by distance (dist_sq is the first element)
    edges.sort(key=lambda x: x[0])
    return edges

# --- Puzzle Solvers ---

def solve_part1(dsu, sorted_edges, num_connections=1000):
    """
    Connects the shortest pairs of junction boxes and calculates the product 
    of the sizes of the three largest resulting circuits.
    
    This is equivalent to running Kruskal's algorithm, stopping after 
    `num_connections` successful unions.
    """
    successful_connections = 0
    
    # Iterate through the edges in increasing order of distance
    for _, i, j in sorted_edges:
        if dsu.union(i, j):
            successful_connections += 1
            if successful_connections == num_connections:
                break
    
    # After 1000 successful connections, get the circuit sizes
    circuit_sizes = dsu.get_circuit_sizes()
    
    # Sort the sizes in descending order
    circuit_sizes.sort(reverse=True)
    
    # Multiply the sizes of the three largest circuits
    # Note: If fewer than 3 circuits exist, the remaining factors are 1 (implicit).
    largest_three = circuit_sizes[:3]
    
    # Ensure there are at least 3 factors (padding with 1 if necessary)
    while len(largest_three) < 3:
        largest_three.append(1)
        
    result = largest_three[0] * largest_three[1] * largest_three[2]
    return result

def solve_part2(dsu, sorted_edges, points):
    """
    Continues connecting the closest unconnected pairs until all junction boxes 
    are in one large circuit. Returns the product of the X coordinates of the 
    last two junction boxes connected.
    """
    # Start from where Part 1 left off, or re-initialise DSU if solved separately
    
    last_pair_connected = None
    
    # Iterate through the edges where the points are not yet connected
    for _, i, j in sorted_edges:
        if dsu.union(i, j):
            # This is a successful union, meaning a new connection was made
            # Check if this connection formed the single large circuit
            if dsu.num_sets == 1:
                # Found the last connection needed
                last_pair_connected = (i, j)
                break
    
    if last_pair_connected:
        i, j = last_pair_connected
        # The coordinates are (x, y, z), we need the X coordinates (index 0)
        x1 = points[i][0]
        x2 = points[j][0]
        return x1 * x2
    else:
        # Should not happen if all points can be connected
        return "Error: All points were already connected or insufficient edges."


def main():
    start_time = time.time()
    
    # 1. Parse Input
    points = parse_input()
    num_points = len(points)
    
    if num_points < 2:
        print("Error: Need at least two junction boxes.", file=sys.stderr)
        sys.exit(1)
        
    # 2. Get and Sort Edges
    # This single expensive step is amortized over both parts.
    edges = get_sorted_edges(points)
    
    # --- Solve Puzzle 1 ---
    p1_start_time = time.time()
    # Create a fresh DSU for Part 1
    dsu_p1 = DSU(num_points)
    
    # Part 1: Connect 1000 shortest pairs
    # The input has 2000 lines, so N=2000. 1000 connections will leave N-1000 = 1000 circuits if all are new.
    puzzle1_result = solve_part1(dsu_p1, edges, num_connections=1000)
    p1_duration = (time.time() - p1_start_time) * 1000

    # --- Solve Puzzle 2 ---
    p2_start_time = time.time()
    # Create a fresh DSU for Part 2, as the state from P1 (1000 connections) 
    # might not be the desired starting point if the puzzle logic implies 
    # running the connectivity to completion.
    # "Continue connecting the closest unconnected pairs... until they're all in one large circuit."
    # This is equivalent to finding the last edge of the MST (Maximum edge weight in Kruskal's for all N-1 edges).
    dsu_p2 = DSU(num_points)
    
    # Part 2: Connect until only 1 circuit remains
    puzzle2_result = solve_part2(dsu_p2, edges, points)
    p2_duration = (time.time() - p2_start_time) * 1000

    # --- Output Results ---
    total_duration = (time.time() - start_time) * 1000
    
    print(f"Puzzle 1: {puzzle1_result}")
    print(f"Puzzle 2: {puzzle2_result}")
    print(f"Total Duration: {total_duration:.2f}ms")


if __name__ == "__main__":
    main()