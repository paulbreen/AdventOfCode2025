import time

def parse_input(filename):
    """Parse the input file into ranges and ingredient IDs."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    # Find the blank line separator
    separator_index = lines.index('')

    # Parse ranges (before blank line)
    ranges = []
    for line in lines[:separator_index]:
        start, end = map(int, line.split('-'))
        ranges.append((start, end))

    # Parse ingredient IDs (after blank line)
    ingredient_ids = [int(line) for line in lines[separator_index + 1:] if line]

    return ranges, ingredient_ids

def is_fresh(ingredient_id, ranges):
    """Check if an ingredient ID falls within any fresh range."""
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False

def solve_puzzle1(ranges, ingredient_ids):
    """Count how many available ingredient IDs are fresh."""
    fresh_count = sum(1 for id in ingredient_ids if is_fresh(id, ranges))
    return fresh_count

def merge_ranges(ranges):
    """Merge overlapping ranges and return list of non-overlapping ranges."""
    if not ranges:
        return []

    # Sort ranges by start position
    sorted_ranges = sorted(ranges)

    merged = [sorted_ranges[0]]

    for current_start, current_end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]

        # Check if current range overlaps or is adjacent to last merged range
        if current_start <= last_end + 1:
            # Merge by extending the end if necessary
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            # No overlap, add as new range
            merged.append((current_start, current_end))

    return merged

def count_ids_in_ranges(ranges):
    """Count total IDs covered by a list of ranges."""
    total = 0
    for start, end in ranges:
        total += (end - start + 1)
    return total

def solve_puzzle2(ranges):
    """Count total unique ingredient IDs considered fresh by the ranges."""
    merged = merge_ranges(ranges)
    return count_ids_in_ranges(merged)

def main():
    # Start timing
    start_time = time.time()

    # Parse input
    ranges, ingredient_ids = parse_input('input.txt')

    # Solve Puzzle 1
    puzzle1_start = time.time()
    result1 = solve_puzzle1(ranges, ingredient_ids)
    puzzle1_time = time.time() - puzzle1_start

    # Solve Puzzle 2
    puzzle2_start = time.time()
    result2 = solve_puzzle2(ranges)
    puzzle2_time = time.time() - puzzle2_start

    # Calculate total time
    total_time = time.time() - start_time

    # Output results in required format
    print(f"Puzzle 1: {result1}")
    print(f"Puzzle 2: {result2}")
    print(f"Total Duration: {total_time * 1000:.2f}ms")

if __name__ == "__main__":
    main()
