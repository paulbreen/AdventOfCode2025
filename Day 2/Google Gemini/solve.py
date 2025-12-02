import sys
import time
import os

def parse_input(filename):
    """Reads the input file and returns a list of (start, end) tuples."""
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
        
    ranges = []
    with open(filename, 'r') as f:
        content = f.read().replace('\n', '').strip()
        # Input format is "start-end,start-end,..."
        parts = content.split(',')
        for part in parts:
            if '-' in part:
                start_str, end_str = part.split('-')
                ranges.append((int(start_str), int(end_str)))
    return ranges

def is_invalid_p1(num_str):
    """
    Puzzle 1 Rule: ID is made ONLY of some sequence repeated strictly TWICE.
    e.g., 55 (5-5), 123123 (123-123).
    """
    length = len(num_str)
    
    # Must be even length to be split exactly in half
    if length % 2 != 0:
        return False
        
    mid = length // 2
    # Check if first half equals second half
    return num_str[:mid] == num_str[mid:]

def is_invalid_p2(num_str):
    """
    Puzzle 2 Rule: ID is made ONLY of some sequence repeated AT LEAST twice.
    e.g., 111 (1-1-1), 121212 (12-12-12).
    """
    length = len(num_str)
    
    # Try all possible pattern lengths from 1 up to half the string
    for pattern_len in range(1, (length // 2) + 1):
        # The total length must be divisible by the pattern length
        if length % pattern_len == 0:
            pattern = num_str[:pattern_len]
            repeats = length // pattern_len
            
            # Reconstruct the string using the pattern
            if pattern * repeats == num_str:
                return True
                
    return False

def solve():
    input_file = 'input.txt'
    
    try:
        ranges = parse_input(input_file)
    except Exception as e:
        print(f"Error parsing input: {e}")
        return

    # Initialize counters
    p1_sum = 0
    p2_sum = 0

    t_start = time.perf_counter()

    # Process all ranges
    # Since the total range coverage is ~1.5 million numbers, 
    # brute force iteration is efficient enough and ensures correctness.
    for start_num, end_num in ranges:
        for num in range(start_num, end_num + 1):
            s_num = str(num)
            
            # Check Puzzle 1
            if is_invalid_p1(s_num):
                p1_sum += num
            
            # Check Puzzle 2
            # Note: Logic for P2 covers P1 cases as well, but definitions 
            # in the prompt imply checking specific rules for specific totals.
            if is_invalid_p2(s_num):
                p2_sum += num

    t_end = time.perf_counter()
    duration_ms = (t_end - t_start) * 1000

    print(f"Puzzle 1: {p1_sum}")
    print(f"Puzzle 2: {p2_sum}")
    print(f"Total Duration: {duration_ms:.4f}ms")

if __name__ == "__main__":
    solve()