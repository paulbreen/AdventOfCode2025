# Day 2: Gift Shop - Implementation Comparison

## Problem Summary
Given comma-separated ID ranges, find invalid product IDs:
- **Puzzle 1**: IDs made of a digit sequence repeated **exactly twice** (e.g., 55, 123123)
- **Puzzle 2**: IDs made of a digit sequence repeated **at least twice** (e.g., 111, 12341234, 565656)

Sum all invalid IDs found in the ranges.

## Implementations Overview

| Implementation | Language | Strategy | Complexity | Key Feature |
|---------------|----------|----------|------------|-------------|
| Claude CLI | Python | Brute force iteration | O(N × L) | Clean, readable validation |
| Google Gemini | Python | Combined iteration | O(N × L) | Single-pass for both puzzles |
| Chat GPT | Python | Pre-generation | O(C log C + R) | Mathematical candidate generation |
| Human | C# | Brute force with LINQ | O(N × L²) | Functional-style chunking |

**Legend**: N = total numbers in ranges, L = average number length, C = candidates, R = ranges

## Key Similarities

All implementations:
- Parse comma-separated ranges from input
- Handle range format `start-end,start-end,...`
- Use string manipulation to check repeating patterns
- Time execution and output in standardized format
- Convert numbers to strings for pattern detection

## Major Differences

### Core Algorithm Strategy

#### Brute Force Approach (Claude CLI, Google Gemini, Human)
**Method**: Iterate every number in every range, check each for invalid patterns

**Claude CLI - Sequential solving**:
```python
def is_invalid_puzzle1(num_str):
    if len(num_str) % 2 != 0: return False
    mid = len(num_str) // 2
    return num_str[:mid] == num_str[mid:]

def is_invalid_puzzle2(num_str):
    for pattern_len in range(1, len(num_str) // 2 + 1):
        if len(num_str) % pattern_len == 0:
            pattern = num_str[:pattern_len]
            if pattern * (len(num_str) // pattern_len) == num_str:
                return True
    return False
```

**Google Gemini - Combined iteration**:
- Processes both puzzles in single loop through ranges
- Checks same number against both rule sets simultaneously
- Reduces redundant range iteration

#### Pre-Generation Approach (Chat GPT)
**Method**: Generate all possible repeated numbers mathematically, then find which fall in ranges

**Key innovation**: Instead of checking every number, generates only candidates:
```python
def generate_repeated_numbers(min_value, max_value):
    for total_len in range(len_min, len_max + 1):
        for k in range(2, total_len + 1):  # k repetitions
            if total_len % k != 0: continue
            block_len = total_len // k

            # Generate all blocks (no leading zeros)
            for block in range(10**(block_len-1), 10**block_len):
                n = int(str(block) * k)
                if min_value <= n <= max_value:
                    candidates.add(n)
```

**Advantages**:
- Generates only valid candidates (much smaller set than full range)
- Merges overlapping ranges for efficiency
- Uses sorted matching to find candidates in ranges
- More efficient when ranges are sparse or very large

**Trade-off**: More complex code, higher upfront cost for small inputs

### Puzzle 2 Pattern Detection

**Claude CLI & Google Gemini**: Try all pattern lengths 1 to L/2
```python
for pattern_len in range(1, length // 2 + 1):
    if length % pattern_len == 0:
        if pattern * (length // pattern_len) == num_str:
            return True
```

**Chat GPT**: Pre-generates by construction (pattern inherently repeated)

**Human (C#)**: LINQ-based chunking approach
```csharp
for (int i = 1; i <= halfLength; i++) {
    var chunks = stringId.Chunk(i).Select(x => new string(x));
    var groupedChunks = chunks.GroupBy(x => x);
    if (groupedChunks.Count() == 1) return false;  // All chunks identical
}
```

### Code Organization

**Python Implementations**:
- Single-file solutions
- Separate validation functions per puzzle
- Functional style with helper functions

**C# Implementation**:
- Multi-class structure: `Program.cs`, `Puzzle1.cs`, `Puzzle2.cs`
- Static methods returning Int64
- Inverted boolean logic (returns `true` = valid, `false` = invalid)

### Performance Optimization

| Feature | Claude CLI | Google Gemini | Chat GPT | Human |
|---------|-----------|---------------|----------|-------|
| Range merging | ❌ | ❌ | ✅ | ❌ |
| Candidate pre-generation | ❌ | ❌ | ✅ | ❌ |
| Combined iteration | ❌ | ✅ | N/A | ❌ |
| Early termination | ❌ | ❌ | ✅ | ❌ |

## Complexity Analysis

For typical AoC input (~1.5M numbers across ranges):

**Time Complexity**:
- **Claude CLI**: O(N × L) per puzzle = O(2N × L)
- **Google Gemini**: O(N × L) for both puzzles combined
- **Chat GPT**: O(C × k + C log R) where C = candidates (~10K-100K), k = max repetitions
- **Human**: O(N × L²) due to repeated chunking operations

**Space Complexity**:
- **Claude/Gemini/Human**: O(1) - processes numbers one at a time
- **Chat GPT**: O(C) - stores all candidates in memory

## Code Quality

| Aspect | Claude CLI | Google Gemini | Chat GPT | Human |
|--------|-----------|---------------|----------|-------|
| Readability | Excellent | Very Good | Moderate | Good |
| Documentation | Excellent docstrings | Good comments | Extensive docs | Minimal |
| Complexity | Low | Low | High | Medium |
| Error Handling | Good | Good | Excellent | Basic |
| Type Safety | No types | No types | Full type hints | Static typing |
| Cleverness | Low | Low | Very High | Medium |

## Algorithm Trade-offs

### When Brute Force Wins (Claude, Gemini, Human)
- Small to medium input sizes (AoC typical)
- Dense ranges (most numbers must be checked anyway)
- Simplicity valued over micro-optimization
- Easier to understand and debug

### When Pre-Generation Wins (Chat GPT)
- Very large ranges with sparse coverage
- Multiple range queries on same dataset
- When candidate count << total range size
- Theoretical elegance valued

## Interesting Implementation Details

**Chat GPT's Range Merging**:
```python
def merge_ranges(ranges):
    # Merges [1-10, 5-15, 20-25] -> [1-15, 20-25]
    # Eliminates redundant checking
```

**Human's LINQ Chunking**:
```csharp
stringId.Chunk(i)           // Split into chunks of size i
    .Select(x => new string(x))  // Convert to strings
    .GroupBy(x => x)            // Group identical chunks
    .Count() == 1               // All chunks the same?
```

**Google Gemini's Combined Iteration**:
```python
for num in range(start, end + 1):
    if is_invalid_p1(s_num): p1_sum += num
    if is_invalid_p2(s_num): p2_sum += num
# Check both puzzles per number
```

## Conclusion

Day 2 showcases contrasting philosophies:

- **Claude CLI**: Prioritizes clarity—separate, focused functions for each puzzle
- **Google Gemini**: Balances simplicity with practical efficiency (combined iteration)
- **Chat GPT**: Demonstrates algorithmic sophistication with pre-generation strategy
- **Human**: Leverages language features (LINQ) for expressive pattern matching

For Advent of Code's constraints, **all approaches perform adequately** (sub-second execution). The **brute force solutions** excel in maintainability and are easier to verify for correctness. The **pre-generation approach** is intellectually impressive and would scale better for much larger inputs, but adds significant complexity.

**Best for understanding**: Claude CLI (clearest logic)
**Best for efficiency**: Chat GPT (fewest total operations)
**Best balance**: Google Gemini (simple + practical optimization)
**Most idiomatic**: Human (language-specific features)
