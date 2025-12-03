# Day 3: Lobby - Implementation Comparison

## Problem Summary
Given lines of digits (battery banks), find the maximum number possible by selecting exactly **k** digits while preserving their original order:
- **Puzzle 1**: Select exactly **2 digits** per bank (e.g., "234234234234278" → 78)
- **Puzzle 2**: Select exactly **12 digits** per bank (e.g., "234234234234278" → 434234234278)

Sum all maximum values across all banks.

## Implementations Overview

| Implementation | Language | Puzzle 1 Strategy | Puzzle 2 Strategy | Complexity |
|---------------|----------|-------------------|-------------------|------------|
| Claude CLI | Python | Monotonic Stack | Monotonic Stack | O(N) both |
| Google Gemini | Python | Brute Force (O(N²)) | Monotonic Stack | O(N²) / O(N) |
| Chat GPT | Rust | Monotonic Stack | Monotonic Stack | O(N) both |
| Human | C# | Simplified Greedy | Recursive Greedy | O(N) / O(K×N) |

**Legend**: N = line length (~15 chars typical), K = digits to select

## Key Similarities

All implementations:
- Read input line by line from `input.txt`
- Process each battery bank independently
- Sum results across all banks
- Time execution and output in standardized format
- Recognize this as a **maximum subsequence selection** problem

## Core Algorithm: Maximum K-Subsequence

This is a classic problem: **find the lexicographically largest subsequence of length k** from a sequence while preserving order.

### Optimal Solution: Monotonic Stack (Greedy)

**Used by**: Claude CLI, Google Gemini (P2), Chat GPT

**Algorithm**:
1. We can remove `n - k` digits to keep `k` digits
2. Iterate through digits, maintaining a stack
3. Pop smaller digits from stack when seeing a larger digit (if removals remain)
4. This builds the lexicographically largest subsequence

**Claude CLI implementation**:
```python
def find_max_k_digits(digits_str, k):
    n = len(digits_str)
    to_remove = n - k
    stack = []

    for digit in digits_str:
        # Remove smaller digits when we see a larger one
        while stack and to_remove > 0 and stack[-1] < digit:
            stack.pop()
            to_remove -= 1
        stack.append(digit)

    return int(''.join(stack[:k]))
```

**Time**: O(N) - each digit pushed/popped at most once
**Space**: O(K) - stack size limited to k

### Alternative Approaches

#### Brute Force (Google Gemini - Puzzle 1 only)

**For k=2**: Try all pairs `(i, j)` where `i < j`

```python
for i in range(len(line) - 1):
    for j in range(i + 1, len(line)):
        val = int(line[i] + line[j])
        current_max = max(current_max, val)
```

**Time**: O(N²) - acceptable for k=2 and small N
**Trade-off**: Simpler to understand, but doesn't scale to larger k

#### Simplified Greedy (Human - Puzzle 1)

**For k=2**: Find the max digit (excluding last), then find max after it

```csharp
largest = voltageArray.SkipLast(1).Max();  // Max from first n-1 digits
index = voltageArray.IndexOf(largest);
secondLargest = voltageArray.GetRange(index + 1, ...).Max();  // Max after it
```

**Why it works for k=2**: First digit should be largest possible with room for second digit
**Limitation**: Doesn't generalize well to k > 2

#### Recursive Greedy (Human - Puzzle 2)

```csharp
public static string FindLargest(char[] batteryBank, int maxSize) {
    if (maxSize == -1) return string.Empty;
    if (batteryBank.Length == maxSize) return batteryBank.ToString();

    // Find max in first (n - maxSize) positions
    var largest = batteryBank.Take(batteryBank.Length - maxSize).Distinct().Max();
    var indexOfLargest = Array.IndexOf(batteryBank, largest);

    // Recursively solve for remaining
    return largest + FindLargest(batteryBank.Skip(indexOfLargest + 1).ToArray(), maxSize - 1);
}
```

**Approach**: For each position, find the largest digit that leaves enough digits for remaining positions
**Issue**: Uses `Distinct()` which is unnecessary (we want first occurrence of max)
**Time**: O(K × N) recursive calls with linear scans

## Major Differences

### Language Diversity

Day 3 introduces **Rust** (Chat GPT) - first non-Python/C# solution:
- **3 Python implementations**: Claude CLI, Google Gemini
- **1 Rust implementation**: Chat GPT (demonstrating systems programming choice)
- **1 C# implementation**: Human

### Puzzle 1 Strategy Divergence

**Monotonic Stack** (Claude CLI, Chat GPT):
- Uses the optimal algorithm even for k=2
- Generalizable, consistent with Puzzle 2
- Code reuse between puzzles

**Brute Force** (Google Gemini):
- Pragmatic for k=2 with small input
- "Brute-force O(N²) approach is perfectly performant" (comment)
- Easier to verify correctness

**Simplified Greedy** (Human):
- Custom logic specific to k=2
- Works correctly but less generalizable
- Shows problem-specific optimization

### Code Organization

**Python Solutions** (Claude, Gemini):
- Single file, function-based
- Reusable helper functions

**Rust Solution** (Chat GPT):
- Single file with strong typing
- Functional iterators and pattern matching
- Memory-safe with zero-cost abstractions

**C# Solution** (Human):
- Multi-file: `Program.cs`, `Puzzle1.cs`, `Puzzle2.cs`
- Puzzle 1 and 2 use completely different algorithms
- Recursive approach for Puzzle 2

## Complexity Analysis

| Implementation | Puzzle 1 Time | Puzzle 2 Time | Space |
|---------------|---------------|---------------|-------|
| Claude CLI | O(N) | O(N) | O(K) |
| Google Gemini | O(N²) | O(N) | O(1) / O(K) |
| Chat GPT | O(N) | O(N) | O(K) |
| Human | O(N) | O(K×N) | O(N) recursive |

**For typical input** (200 lines, ~15 chars each):
- **Claude/Chat GPT**: ~3,000 operations total
- **Google Gemini P1**: ~45,000 operations (still fast)
- **Human P2**: ~36,000 operations (recursive overhead)

All execute in < 5ms, so practical differences are negligible.

## Code Quality

| Aspect | Claude CLI | Google Gemini | Chat GPT | Human |
|--------|-----------|---------------|----------|-------|
| Documentation | Excellent docstrings | Good comments | Good docs | Minimal |
| Algorithm Choice | Optimal | Pragmatic | Optimal | Mixed |
| Consistency | High (same algo both) | Mixed approaches | High | Low (different algos) |
| Readability | Excellent | Very Good | Good | Moderate |
| Type Safety | No types | No types | Full static typing | Static typing |
| Error Handling | Good | Good | Excellent | Basic |

## Interesting Implementation Details

### Chat GPT's Safety Checks (Rust)

```rust
while let Some(&last) = stack.last() {
    if remove_left > 0 && last < d && (stack.len() - 1 + (n - i)) >= k {
        stack.pop();
        remove_left -= 1;
    } else {
        break;
    }
}

if stack.len() < k {
    stack.push(d);
} else if remove_left > 0 {
    remove_left -= 1;  // Discard if stack full
}
```
Additional check ensures we can still fill k slots after popping.

### Google Gemini's Pragmatic Comment

```python
# Since the line length is small (~100 chars), a brute-force O(N^2)
# approach is perfectly performant and ensures we don't miss
# edge cases with duplicate high digits.
```
Explicitly acknowledges algorithm choice based on constraints.

### Human's Recursive Pattern

```csharp
return string.Concat(largest, FindLargest(batteryBank, maxSize - 1));
```
Builds result by recursively selecting one digit at a time.

### Claude CLI's Clean Abstraction

```python
def solve_puzzle1(lines):
    return sum(find_max_k_digits(line, 2) for line in lines)

def solve_puzzle2(lines):
    return sum(find_max_k_digits(line, 12) for line in lines)
```
Single function handles both puzzles with different k values.

## Algorithm Correctness Note

**Human Puzzle 2 has a subtle inefficiency**:
```csharp
var largest = batteryBank.Take(n - maxSize).Distinct().Max();
```

The `Distinct()` call is unnecessary and potentially problematic:
- We want the **first occurrence** of the maximum digit in the valid range
- `Distinct()` just removes duplicates from the search space
- Should use `Max()` directly, then find first index with `Array.IndexOf()`

The algorithm still produces correct results but with extra overhead.

## Conclusion

Day 3 showcases **algorithm selection trade-offs**:

- **Claude CLI**: Demonstrates consistency—uses optimal O(N) algorithm for both puzzles
- **Google Gemini**: Shows pragmatism—uses brute force where it's "good enough," optimal where needed
- **Chat GPT**: Introduces Rust with careful attention to edge cases and safety
- **Human**: Uses problem-specific optimizations but lacks consistency between puzzles

**Key Insight**: The **monotonic stack** algorithm is the theoretically optimal solution (O(N)), but for small inputs:
- Brute force (O(N²)) for k=2 is perfectly acceptable
- Custom greedy approaches can be simpler for specific k values
- Performance differences are negligible in practice

**Best theoretical approach**: Claude CLI or Chat GPT (consistent optimal algorithm)
**Best pragmatic approach**: Google Gemini (complexity matches problem scale)
**Most interesting**: Chat GPT (Rust, systems-level efficiency)
**Most variable**: Human (different strategies per puzzle)

The choice between these approaches reflects different engineering philosophies: algorithmic purity vs. practical simplicity vs. language-specific idioms.
