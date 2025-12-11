import sys
import time
from collections import defaultdict

# --- Core Graph Solver ---

def count_paths(graph, start_node, end_node, memo):
    """
    Counts the number of paths from start_node to end_node using DFS with memoization.
    Since the graph is a DAG (data flows through outputs only), this is efficient.
    
    :param graph: Adjacency list representation of the device connections.
    :param start_node: The current node in the path.
    :param end_node: The target node ('out').
    :param memo: Dictionary for memoization (cache) to store path counts.
    :return: The total number of unique paths.
    """
    # 1. Base Cases
    if start_node == end_node:
        return 1
    if start_node not in graph:
        # A node that is not an output for anything cannot reach the end
        return 0
    
    # 2. Check Memo
    if start_node in memo:
        return memo[start_node]

    # 3. Recursive Step
    path_count = 0
    # Iterate through all outputs (neighbors)
    for neighbor in graph[start_node]:
        path_count += count_paths(graph, neighbor, end_node, memo)
    
    # 4. Store Result and Return
    memo[start_node] = path_count
    return path_count

# --- Puzzle Solvers ---

def solve_puzzle_1(graph):
    """
    Find all paths from 'you' to 'out'.
    """
    # Start: 'you', End: 'out' [cite: 36, 37]
    memo = {}
    return count_paths(graph, 'you', 'out', memo)

def solve_puzzle_2(graph):
    """
    Find all paths from 'svr' to 'out' that visit both 'dac' and 'fft'.
    This involves finding the count for two distinct routes: svr->dac->fft->out and svr->fft->dac->out.
    Since the problem is a DAG, the total path count is the sum of (Path A * Path B * Path C).
    
    The devices are: svr (start), dac, fft, out (end). 
    """
    
    # A memoization table for all path counting segments
    memo_global = {}

    def get_count(start, end):
        # We need a fresh memo for each new starting node, but we can reuse results
        # for intermediate nodes if the path counting starts there.
        # However, to simplify, we treat each start/end pair as a distinct problem.
        # A unique key for memoization across all calls is needed.
        key = (start, end)
        if key in memo_global:
            return memo_global[key]
        
        # Count paths and store result
        result = count_paths(graph, start, end, {}) # DFS requires its own memo for a specific run
        memo_global[key] = result
        return result

    # --- Route 1: svr -> dac -> fft -> out ---
    # Paths (svr -> dac)
    count_s_d = get_count('svr', 'dac')
    # Paths (dac -> fft)
    count_d_f = get_count('dac', 'fft')
    # Paths (fft -> out)
    count_f_o = get_count('fft', 'out')
    
    # Total paths for Route 1: Count(S->D) * Count(D->F) * Count(F->O)
    route_1_total = count_s_d * count_d_f * count_f_o

    # --- Route 2: svr -> fft -> dac -> out ---
    # Paths (svr -> fft)
    count_s_f = get_count('svr', 'fft')
    # Paths (fft -> dac)
    count_f_d = get_count('fft', 'dac')
    # Paths (dac -> out)
    count_d_o = get_count('dac', 'out')
    
    # Total paths for Route 2: Count(S->F) * Count(F->D) * Count(D->O)
    route_2_total = count_s_f * count_f_d * count_d_o
    
    # Total paths must visit both dac and fft (in any order). [cite: 4]
    return route_1_total + route_2_total

# --- Main Execution ---

def parse_input(filename="input.txt"):
    """
    Reads the input file and builds the adjacency list (graph).
    """
    graph = defaultdict(list)
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Format: device_a: device_b device_c ...
                parts = line.split(':')
                if len(parts) != 2:
                    continue
                    
                device = parts[0].strip()
                outputs = parts[1].split()
                
                # Since data flows from the device to its outputs,
                # we only store the outputs.
                graph[device].extend(outputs)
                
    except FileNotFoundError:
        print(f"Error: Input file '{filename}' not found.", file=sys.stderr)
        sys.exit(1)
        
    return graph

def main():
    start_time = time.time()
    
    graph = parse_input()
    
    # --- Solve Puzzle 1 ---
    puzzle1_start = time.time()
    result_1 = solve_puzzle_1(graph)
    puzzle1_duration = (time.time() - puzzle1_start) * 1000 # Convert to ms
    
    # --- Solve Puzzle 2 ---
    puzzle2_start = time.time()
    result_2 = solve_puzzle_2(graph)
    puzzle2_duration = (time.time() - puzzle2_start) * 1000 # Convert to ms
    
    # --- Output ---
    total_duration = (time.time() - start_time) * 1000 # Convert to ms
    
    print(f"Puzzle 1: {result_1}")
    print(f"Puzzle 2: {result_2}")
    print(f"Total Duration: {total_duration:.2f}ms")

if __name__ == "__main__":
    main()