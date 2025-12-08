import time
from collections import defaultdict

class UnionFind:
    """Union-Find data structure for tracking connected components."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        """Find the root of x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """Union two sets and return True if they were previously disconnected."""
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        # Union by size
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x

        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        return True

    def get_component_sizes(self):
        """Get sizes of all connected components."""
        components = defaultdict(int)
        for i in range(len(self.parent)):
            root = self.find(i)
            components[root] = self.size[root]
        return list(components.values())


def parse_input(filename):
    """Parse the input file and return a list of 3D coordinates."""
    with open(filename, 'r') as f:
        return [tuple(map(int, line.strip().split(','))) for line in f]


def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two 3D points."""
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2) ** 0.5


def solve_puzzles(filename):
    """Solve both puzzles and return results."""
    # Parse input
    junction_boxes = parse_input(filename)
    n = len(junction_boxes)

    # Calculate all pairwise distances
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(junction_boxes[i], junction_boxes[j])
            edges.append((dist, i, j))

    # Sort edges by distance
    edges.sort()

    # Initialize Union-Find
    uf = UnionFind(n)

    # Process connections
    connection_attempts = 0
    puzzle1_result = None
    puzzle2_result = None
    last_i, last_j = None, None

    for dist, i, j in edges:
        # Try to connect (whether successful or not)
        was_connected = uf.union(i, j)

        if was_connected:
            last_i, last_j = i, j

        connection_attempts += 1

        # After 1000 connection attempts, calculate puzzle 1 result
        if connection_attempts == 1000:
            component_sizes = uf.get_component_sizes()
            component_sizes.sort(reverse=True)
            puzzle1_result = component_sizes[0] * component_sizes[1] * component_sizes[2]

        # Check if all boxes are in one circuit (for puzzle 2)
        if puzzle1_result is not None:
            component_sizes = uf.get_component_sizes()
            if len(component_sizes) == 1:
                # The last successful connection that made them all connected
                x1 = junction_boxes[last_i][0]
                x2 = junction_boxes[last_j][0]
                puzzle2_result = x1 * x2
                break

    return puzzle1_result, puzzle2_result


def main():
    start_time = time.perf_counter()

    try:
        puzzle1, puzzle2 = solve_puzzles('input.txt')

        end_time = time.perf_counter()
        duration = (end_time - start_time) * 1000  # Convert to milliseconds

        print(f"Puzzle 1: {puzzle1}")
        print(f"Puzzle 2: {puzzle2}")
        print(f"Total Duration: {duration:.2f}ms")

    except FileNotFoundError:
        print("Error: input.txt not found")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
