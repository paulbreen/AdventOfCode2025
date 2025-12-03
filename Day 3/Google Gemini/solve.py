import time
import sys
import os

def solve_part1(data):
    """
    Finds the largest possible joltage by turning on exactly two batteries per bank.
    [cite_start]Rule: You cannot rearrange batteries[cite: 13].
    """
    total_joltage = 0
    
    for line in data:
        line = line.strip()
        if not line:
            continue
            
        current_max = -1
        
        # Since the line length is small (~100 chars), a brute-force O(N^2) 
        # approach is perfectly performant and ensures we don't miss 
        # edge cases with duplicate high digits.
        for i in range(len(line) - 1):
            for j in range(i + 1, len(line)):
                # [cite_start]Form the number from digits at i and j [cite: 11]
                val = int(line[i] + line[j])
                if val > current_max:
                    current_max = val
                    
        total_joltage += current_max
        
    return total_joltage

def solve_part2(data):
    """
    Finds the largest possible joltage by turning on exactly twelve batteries per bank.
    [cite_start]Rule: Select subsequence of length 12 to maximize value[cite: 22].
    """
    total_joltage = 0
    TARGET_LENGTH = 12
    
    for line in data:
        line = line.strip()
        if not line:
            continue
            
        # We need the lexicographically largest subsequence of length K.
        # We use a greedy stack approach.
        # We iterate through the digits and maintain a stack of chosen digits.
        # If we see a digit larger than the top of the stack, and we have 
        # enough remaining digits to still reach length K, we pop the smaller 
        # digit to make room for the larger one.
        
        stack = []
        n = len(line)
        # Calculate how many characters we can afford to drop to end up with exactly 12
        attempts_remaining = n - TARGET_LENGTH
        
        for digit in line:
            # While stack not empty, current digit is bigger than stack top,
            # and we still have "drops" available:
            while attempts_remaining > 0 and stack and stack[-1] < digit:
                stack.pop()
                attempts_remaining -= 1
            stack.append(digit)
            
        # Truncate to exactly target length (in case we didn't drop enough)
        result_digits = "".join(stack[:TARGET_LENGTH])
        total_joltage += int(result_digits)
        
    return total_joltage

def main():
    start_time = time.time()
    
    # Check for input file
    input_filename = 'input.txt'
    if not os.path.exists(input_filename):
        print(f"Error: {input_filename} not found.")
        sys.exit(1)
        
    with open(input_filename, 'r') as f:
        data = f.readlines()
        
    # Solve Puzzle 1
    p1_start = time.time()
    result_p1 = solve_part1(data)
    p1_duration = (time.time() - p1_start) * 1000
    
    # Solve Puzzle 2
    p2_start = time.time()
    result_p2 = solve_part2(data)
    p2_duration = (time.time() - p2_start) * 1000
    
    total_duration = (time.time() - start_time) * 1000
    
    # Format output as requested
    print(f"Puzzle 1: {result_p1}")
    print(f"Puzzle 2: {result_p2}")
    print(f"Total Duration: {total_duration:.2f}ms")

if __name__ == "__main__":
    main()