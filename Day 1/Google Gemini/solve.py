import sys
import time
import os

def read_input(filename):
    """Reads and parses the input file."""
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
        
    with open(filename, 'r') as f:
        # Filter out empty lines and whitespace
        return [line.strip() for line in f if line.strip()]

def solve_puzzle_1(instructions):
    """
    Solves Puzzle 1: Count how many times the dial ENDS at 0
    after a complete rotation instruction.
    """
    position = 50  # Dial starts at 50
    password_count = 0
    
    for instruction in instructions:
        direction = instruction[0]
        amount = int(instruction[1:])
        
        if direction == 'R':
            position = (position + amount) % 100
        elif direction == 'L':
            position = (position - amount) % 100
            
        if position == 0:
            password_count += 1
            
    return password_count

def solve_puzzle_2(instructions):
    """
    Solves Puzzle 2: Count how many times the dial points at 0
    at ANY point during the rotation (including the end).
    """
    position = 50 # Dial starts at 50
    password_count = 0
    
    for instruction in instructions:
        direction = instruction[0]
        amount = int(instruction[1:])
        
        # Optimization: A full rotation (100 clicks) guarantees hitting 0 exactly once.
        # We can skip simulating the full loops and just add to the score.
        full_rotations = amount // 100
        password_count += full_rotations
        
        # Simulate the remainder steps to see if we cross 0
        remainder = amount % 100
        
        step_change = 1 if direction == 'R' else -1
        
        for _ in range(remainder):
            position = (position + step_change) % 100
            if position == 0:
                password_count += 1
                
    return password_count

def main():
    input_file = 'input.txt'
    
    # Pre-load data to ensure fair timing of logic only
    try:
        data = read_input(input_file)
    except Exception as e:
        print(f"Failed to read input: {e}")
        return

    # --- Solve Puzzle 1 ---
    t1_start = time.perf_counter()
    result1 = solve_puzzle_1(data)
    t1_end = time.perf_counter()
    t1_duration_ms = (t1_end - t1_start) * 1000

    # --- Solve Puzzle 2 ---
    t2_start = time.perf_counter()
    result2 = solve_puzzle_2(data)
    t2_end = time.perf_counter()
    t2_duration_ms = (t2_end - t2_start) * 1000

    # --- Output ---
    print(f"Puzzle 1: {result1}")
    print(f"Puzzle 2: {result2}")
    print(f"Total Duration: {t1_duration_ms + t2_duration_ms:.4f}ms")

if __name__ == "__main__":
    main()