# Day 5: Cafeteria - Implementation Comparison

## Problem Summary
Given fresh ingredient ID ranges and available IDs:
- **Puzzle 1**: Count how many **available IDs** fall within **any** fresh range
- **Puzzle 2**: Count **total unique IDs** covered by the union of all fresh ranges (ignoring available IDs)

This is a **range/interval** problem requiring overlap detection and range merging.

## Implementations Overview

| Implementation | Language | Puzzle 1 Strategy | Puzzle 2 Strategy | Sort Algorithm |
|---------------|----------|-------------------|-------------------|----------------|
| Claude CLI | Python | Linear search | Merge ranges | Built-in O(n log n) |
| Google Gemini | **Go** | Linear search | Merge ranges | Bubble sort O(n²) |
| Chat GPT | Python | **Binary search** | Merge ranges | Built-in O(n log n) |
| Human | C# | LINQ Any() | Merge ranges | Built-in O(n log n) |

## Key Similarities

All implementations:
- Parse input into two sections: ranges and available IDs
- Recognize Puzzle 2 requires **range merging** to avoid double-counting
- Use the "merge overlapping intervals" algorithm for Puzzle 2
- Check for overlap/adjacency with `start <= last_end + 1`
- Count IDs in range as `end - start + 1`

## Language Diversity

Day 5 introduces **Go** (Google Gemini's choice):
- **2 Python implementations**: Claude CLI, Chat GPT
- **1 Go implementation**: Google Gemini (systems programming language)
- **1 C# implementation**: Human

## Core Algorithms

### Puzzle 1: Range Membership Check

**Challenge**: Determine if each available ID falls in any range

#### Linear Search Approach (Claude, Gemini, Human)

**Claude CLI**:
```python
def is_fresh(ingredient_id, ranges):
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False

fresh_count = sum(1 for id in ingredient_ids if is_fresh(id, ranges))
```

**Google Gemini (Go)**:
```go
func solvePuzzle1(ranges []Range, availableIDs []int) int {
    freshCount := 0
    for _, id := range availableIDs {
        isFresh := false
        for _, r := range ranges {
            if r.isFresh(id) {  // id >= Start && id <= End
                isFresh = true
                break
            }
        }
        if isFresh {
            freshCount++
        }
    }
    return freshCount
}
```

**Human (C#)**:
```csharp
// Inline parsing + checking
if (ranges.Any(x => x.min <= id && x.max >= id)) count++;
```

**Complexity**: O(A × R) where A = available IDs, R = ranges
**Typical**: ~590 IDs × ~30 ranges = ~17,700 checks

#### Binary Search Approach (Chat GPT)

**Strategy**: Merge ranges first, then use binary search

```python
def solve_puzzle1(merged, ids):
    starts = [s for s, _ in merged]  # Extract start points

    def in_any(x):
        idx = bisect_right(starts, x) - 1  # Find rightmost start <= x
        if idx < 0:
            return False
        s, e = merged[idx]
        return s <= x <= e

    return sum(1 for v in ids if in_any(v))
```

**Process**:
1. Merge ranges to eliminate overlaps
2. Extract start positions into sorted array
3. For each ID, binary search to find potential containing range
4. Check if ID falls within that range

**Complexity**: O(R log R + A log R)
- R log R for merging/sorting
- A log R for checking (binary search per ID)

**Optimization**: Reduces ~17,700 checks to ~5,900 (log₂ 30 ≈ 5 per ID)

### Puzzle 2: Total IDs in Union of Ranges

**Universal approach**: Merge overlapping ranges, then count

**Range Merging Algorithm**:

**Claude CLI**:
```python
def merge_ranges(ranges):
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]

    for current_start, current_end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]

        # Check overlap or adjacency
        if current_start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            merged.append((current_start, current_end))

    return merged
```

**Google Gemini (Go)**:
```go
// Bubble sort (O(n²))
for i := 0; i < len(ranges); i++ {
    for j := i + 1; j < len(ranges); j++ {
        if ranges[i].Start > ranges[j].Start {
            ranges[i], ranges[j] = ranges[j], ranges[i]
        }
    }
}

// Merge
for i := 1; i < len(ranges); i++ {
    if current.Start <= lastMerged.End+1 {
        if current.End > lastMerged.End {
            lastMerged.End = current.End
        }
    } else {
        mergedRanges = append(mergedRanges, current)
    }
}
```

**Human (C#)**:
```csharp
ranges.Sort((a, b) => a.min.CompareTo(b.min));

long currentMin = ranges[0].min;
long currentMax = ranges[0].max;

for (int i = 1; i < ranges.Count; i++) {
    if (range.min <= currentMax + 1) {
        currentMax = Math.Max(currentMax, range.max);
    } else {
        total += (currentMax - currentMin + 1);
        currentMin = range.min;
        currentMax = range.max;
    }
}
total += (currentMax - currentMin + 1);  // Add last range
```

**All functionally equivalent** - only syntax/style differences

## Major Differences

### Sorting Algorithm Choice

**Google Gemini - Bubble Sort**:
```go
for i := 0; i < len(ranges); i++ {
    for j := i + 1; j < len(ranges); j++ {
        if ranges[i].Start > ranges[j].Start {
            ranges[i], ranges[j] = ranges[j], ranges[i]
        }
    }
}
```

**Complexity**: O(n²) - 30 ranges = ~900 comparisons

**Others - Built-in Sort**:
- Python: `sorted()` - Timsort O(n log n)
- C#: `Sort()` - Introsort O(n log n)

**Impact**: For 30 ranges:
- Bubble sort: ~900 operations
- Built-in: ~150 operations (30 × log₂ 30)

**Why Gemini chose this**: Simplicity - no library imports, easy to understand
**Trade-off**: Works fine for small inputs, wouldn't scale to 1000+ ranges

### Parsing Strategy

**Claude CLI & Chat GPT - Two-phase**:
```python
separator_index = lines.index('')
ranges = [parse(line) for line in lines[:separator_index]]
ids = [int(line) for line in lines[separator_index + 1:]]
```
Separate parsing from processing

**Human - Inline**:
```csharp
for (int i = 0; i < fileInput.Length; i++) {
    if (fileInput[i].Contains('-')) {
        ranges.Add(...);
    } else {
        var id = Int64.Parse(fileInput[i]);
        if (ranges.Any(...)) count++;  // Check immediately
    }
}
```
Parse and process simultaneously for Puzzle 1

**Google Gemini - State machine**:
```go
parsingRanges := true
for scanner.Scan() {
    if line == "" {
        parsingRanges = false
        continue
    }
    if parsingRanges {
        // parse range
    } else {
        // parse ID
    }
}
```
Boolean flag to track parsing phase

### Data Structures

**Claude & Chat GPT**: Tuples `(start, end)`
**Google Gemini**: Custom struct with methods
```go
type Range struct {
    Start int
    End   int
}

func (r Range) isFresh(id int) bool {
    return id >= r.Start && id <= r.End
}
```

**Human**: Named tuples `(min, max)` for clarity

### Error Handling

**Chat GPT - Most comprehensive**:
```python
if end < start:
    sys.stderr.write(f"Error: range end < start: {line!r}\n")
    sys.exit(1)
```
Validates range ordering, reports detailed errors

**Google Gemini - Good**:
```go
if err := scanner.Err(); err != nil {
    return nil, nil, fmt.Errorf("error reading file: %w", err)
}
```
Proper Go error handling with wrapped errors

**Claude CLI - Basic**:
Simple file not found handling

**Human - None**:
Assumes valid input

## Complexity Analysis

For typical input (~30 ranges, ~590 IDs):

| Implementation | Puzzle 1 | Puzzle 2 | Total |
|---------------|----------|----------|-------|
| Claude CLI | O(A×R) = 17,700 | O(R log R) = 150 | ~17,850 ops |
| Google Gemini | O(A×R) = 17,700 | O(R²) = 900 | ~18,600 ops |
| Chat GPT | O(R log R + A log R) = 3,100 | O(R log R) = 150 | ~3,250 ops |
| Human | O(A×R) = 17,700 | O(R log R) = 150 | ~17,850 ops |

**Chat GPT is ~5.5x more efficient** on Puzzle 1 due to binary search optimization.

However, all complete in **< 1ms**, so practical differences are negligible.

## Code Quality Comparison

| Aspect | Claude CLI | Google Gemini | Chat GPT | Human |
|--------|-----------|---------------|----------|-------|
| Documentation | Good | Minimal | Excellent | None |
| Readability | High | High | Moderate | Good |
| Error Handling | Basic | Good | Excellent | None |
| Algorithm Efficiency | Good | Moderate | Excellent | Good |
| Idiomatic Code | Yes | Yes | Yes | Yes |
| Type Safety | No types | Static | Type hints | Static |

## Interesting Implementation Details

### Google Gemini's Go Patterns

**Struct with methods**:
```go
type Range struct { Start int; End int }
func (r Range) isFresh(id int) bool { ... }
```
Object-oriented style in Go

**Deferred file close**:
```go
file, err := os.Open(filename)
defer file.Close()
```
Ensures cleanup even on error

**Microsecond precision**:
```go
fmt.Printf("Total Duration: %dµs\n", durationTotal.Microseconds())
```
Reports in microseconds vs. milliseconds

### Chat GPT's Binary Search

```python
from bisect import bisect_right

idx = bisect_right(starts, x) - 1
```
Uses Python's built-in binary search module elegantly

### Human's Inline Processing

```csharp
// Single loop handles both parsing and Puzzle 1 solving
if (fileInput[i].Contains('-')) {
    ranges.Add(...);
} else {
    if (ranges.Any(...)) count++;
}
```
Efficient single-pass for Puzzle 1

### Claude CLI's Range Adjacency

```python
if current_start <= last_end + 1:  # Merge adjacent ranges too
```
Correctly merges `[1-5]` and `[6-10]` into `[1-10]`

## Time Unit Reporting

- **Claude CLI**: Milliseconds (ms)
- **Google Gemini**: **Microseconds (µs)**
- **Chat GPT**: **Microseconds (µs)**
- **Human**: Milliseconds (ms)

Google Gemini and Chat GPT report in microseconds, emphasizing sub-millisecond performance for this problem.

## Conclusion

Day 5 showcases **interval/range algorithms** and optimization trade-offs:

- **Claude CLI**: Clean, straightforward implementation prioritizing clarity
- **Google Gemini**: First **Go** solution demonstrating systems programming approach; uses bubble sort (simple but O(n²))
- **Chat GPT**: Most optimized with **binary search** for Puzzle 1; excellent error handling
- **Human**: Pragmatic inline processing; efficient single-pass for Puzzle 1

**Key Insights**:

1. **Binary search optimization** (Chat GPT): Theoretically superior but minimal practical benefit for small inputs
2. **Bubble sort** (Gemini): Perfectly acceptable for ~30 ranges, demonstrates simplicity over optimization
3. **Range merging**: Universal solution for Puzzle 2 - all implementations converge on same algorithm
4. **Language choice**: Go offers strong typing and built-in concurrency (though not needed here)

**Best for learning**: Claude CLI (clearest structure)
**Best for performance**: Chat GPT (binary search optimization)
**Most interesting**: Google Gemini (Go language, bubble sort choice)
**Most pragmatic**: Human (inline processing for efficiency)

All implementations are **correct** and handle the problem effectively. For Advent of Code scale (~30 ranges), the difference between O(A×R) and O(A log R) is imperceptible, validating the engineering principle: **choose the simplest solution that meets requirements**.
