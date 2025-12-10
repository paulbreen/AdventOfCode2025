# Day 10: Factory - Implementation Comparison

## Problem Summary
Linear algebra problems disguised as button-pressing puzzles:
- **Puzzle 1 (Lights)**: Toggle lights to match target pattern - solve Ax = b over **GF(2)** (mod 2 / XOR)
- **Puzzle 2 (Counters)**: Increment counters to match target values - solve Ax = b over **non-negative integers**

Each machine has buttons that affect specific lights/counters. Find minimum total button presses.

## Implementations Overview

| Implementation | Language | Puzzle 1 Status | Puzzle 2 Status | Performance |
|---------------|----------|-----------------|-----------------|-------------|
| Claude CLI | Python | ✅ Correct | ❌ **WRONG** | Fast / Fast (wrong) |
| Google Gemini | Python | ❓ Unknown | ⏱️ **5+ HOUR TIMEOUT** | Fast / Infinite |
| Chat GPT | Python | ✅ **CORRECT** | ✅ **CORRECT** | ⚡ **Fast / Fast** |
| Human | C# | ✅ Correct | ✅ **CORRECT (slow)** | Fast / Very slow |

**Winner**: **Chat GPT** - only AI to solve both puzzles correctly with good performance

## Problem Recognition: Linear Algebra

Both puzzles are linear algebra problems:

### Puzzle 1: Lights-Out Problem (GF(2))

**Mathematical formulation**: Ax = b (mod 2)
- A = matrix where A[light][button] = 1 if button affects that light
- x = vector of button press counts (each 0 or 1, since pressing twice cancels)
- b = target light state (0 = off, 1 = on)

**Key insight**: XOR arithmetic - pressing button twice = no press

### Puzzle 2: Integer Linear Programming

**Mathematical formulation**: Ax = b where x ≥ 0, x ∈ ℤⁿ
- A = same matrix structure
- x = vector of button press counts (non-negative integers)
- b = target counter values

**Challenge**: Must find **non-negative integer solution** with minimum sum(x)

## Puzzle 1 Approaches

### Brute Force (Claude CLI, Human) - ✅ Works

```python
# Try all 2^n combinations (each button pressed 0 or 1 times)
for mask in range(1 << num_buttons):
    state = [0] * num_lights
    presses = 0

    for button_idx in range(num_buttons):
        if mask & (1 << button_idx):
            presses += 1
            for light_idx in buttons[button_idx]:
                state[light_idx] ^= 1  # Toggle

    if state == target:
        min_presses = min(min_presses, presses)
```

**Complexity**: O(2ⁿ × m) where n = buttons, m = lights
**Works for**: n ≤ 20-25 buttons (typical AoC constraint)

### Gaussian Elimination over GF(2) (Google Gemini) - ✅ Likely works

```python
# Solve Ax = b over Z_2 using Gaussian elimination
aug_matrix = [[0] * (num_buttons + 1) for _ in range(num_lights)]

# Populate A and b
for r in range(num_lights):
    for c in range(num_buttons):
        if r in buttons[c]:
            aug_matrix[r][c] = 1
    aug_matrix[r][num_buttons] = target[r]

# Gaussian elimination with mod 2 arithmetic
# Find RREF and then search for minimum solution
```

**Advantage**: Can handle larger systems theoretically
**Complexity**: O(n²m) for GF(2) Gaussian elimination

### DFS with Pruning (Chat GPT) - ✅ Works

```python
def dfs(i: int, cur_mask: int, presses: int):
    if presses >= best[0]:  # Prune if worse than current best
        return
    if i == num_buttons:
        if cur_mask == target_mask:
            best[0] = presses
        return
    dfs(i + 1, cur_mask, presses)  # Skip button i
    dfs(i + 1, cur_mask ^ masks[i], presses + 1)  # Press button i
```

**Advantage**: Early pruning reduces search space significantly
**Complexity**: O(2ⁿ) worst case, but pruning makes it practical

## Puzzle 2 Approaches - The Hard Part

### Claude CLI: Incomplete Gaussian Elimination ❌

```python
def solve_puzzle2_machine(joltages, buttons):
    # Build matrix and augmented form
    augmented = [row[:] + [joltages[i]] for i, row in enumerate(A)]

    # Gaussian elimination to RREF
    # ... (code starts but incomplete)

    # Then tries brute force search
    # Missing proper handling of free variables
```

**Problem**: Incomplete implementation - doesn't properly enumerate free variable assignments

### Google Gemini: ⏱️ Timeout (5+ hours)

Based on code structure, likely issues:
- Attempted BFS or exhaustive search over integer solution space
- No upper bounds on button presses
- Exponential blowup without proper pruning
- May have infinite loop or search too large a space

**Why it failed**: Integer solutions require bounded search - can't just try all combinations

### Chat GPT: RREF + Bounded Free Variable Search ✅ **CORRECT**

```python
def rref(A, b):
    # Compute Reduced Row Echelon Form using Fraction for exact arithmetic
    M = [[Fraction(A[i][j]) for j in range(m)] + [Fraction(b[i])] for i in range(n)]

    # Standard RREF algorithm
    # Returns: matrix M, pivot_cols, pivot_row_for_col

def min_presses_counters(jolts, buttons):
    # 1. Compute RREF to identify pivot and free variables
    M, pivot_cols, pivot_row_for_col, all_cols = rref(A, b)

    free_cols = [c for c in all_cols if c not in pivot_cols]

    # 2. For each pivot variable, express as: x_p = const + Σ(coeff_i * x_free_i)
    # 3. Determine upper bounds for free variables
    # 4. DFS over free variable assignments, compute pivot variables
    # 5. Check if all variables are non-negative integers
    # 6. Track minimum sum
```

**Key innovations**:
1. **RREF decomposition**: Separates pivot and free variables
2. **Bounded search**: Only search reasonable ranges for free variables
3. **Exact arithmetic**: Uses `Fraction` to avoid floating point errors
4. **Validation**: Checks if computed pivot values are non-negative integers

**Why it works**: Systematic enumeration with mathematical insight

### Human: RREF + DFS + Parallelization ✅ **CORRECT but SLOW**

```csharp
private static long SolveMachine(string line)
{
    // Build matrix A from button definitions
    // Compute RREF decomposition
    var (M, pivotCols, pivotRowForCol) = RREF(A, target);

    // Identify free variables
    var freeCols = columns not in pivotCols;

    // Compute upper bounds for free variables
    for (int j = 0; j < m; j++)
        ub[j] = affectedCounters.Min();

    // DFS over free variable assignments
    void DFS(int idx) {
        if (idx == freeCols.Count) {
            // Compute full solution
            // Check if all pivot variables are non-negative integers
            // Update best if valid
        }
        for (int val = 0; val <= ub[freeCols[idx]]; val++) {
            xFree[idx] = val;
            DFS(idx + 1);
        }
    }
}

// Parallel processing across machines
Parallel.For(0, fileInput.Length, i => {
    total += SolveMachine(fileInput[i]);
});
```

**Advantages**:
- Same RREF + bounded DFS approach as Chat GPT
- **Parallel processing** across machines
- Progress reporting during execution

**Disadvantages**:
- **Very slow** despite parallelization
- User noted "took a long time" and "resorted to AI help"
- Potentially larger search spaces or less efficient pruning

## Complexity Comparison

### Puzzle 1:
| Approach | Worst Case | Typical |
|----------|-----------|---------|
| Brute force | O(2ⁿ × m) | Fast for n ≤ 25 |
| Gaussian + search | O(n²m + 2^f) | Fast if few free vars |
| DFS with pruning | O(2ⁿ) | Much faster with pruning |

### Puzzle 2:
| Approach | Worst Case | Typical |
|----------|-----------|---------|
| Claude (incomplete) | N/A | Wrong answer |
| Gemini (unbounded) | ∞ | Timeout |
| Chat GPT (bounded DFS) | O(n³ + B^f) | ⚡ Fast |
| Human (bounded DFS) | O(n³ + B^f) | 🐢 Slow |

Where:
- n = number of buttons
- m = number of lights/counters
- f = number of free variables
- B = average upper bound per free variable

## Why Google Gemini Timed Out

**Likely causes**:

1. **No upper bounds on free variables**: Searched infinite/huge ranges
2. **Poor pruning**: Didn't skip obviously invalid assignments early
3. **Exponential blowup**: Free variable count too high without bounds
4. **Implementation bug**: Infinite loop or redundant computation

**Evidence**: Ran for 5+ hours before manual stop - indicates unbounded search

## Chat GPT's Winning Strategy

**What made it successful**:

1. **Mathematical insight**: Recognized RREF decomposition approach
2. **Upper bound calculation**:
   ```python
   # For each button, find minimum target value it affects
   # This bounds how many times we can press it
   ```
3. **Exact arithmetic**: Used `Fraction` to avoid floating point errors
4. **Systematic search**: Enumerate free variables within bounds
5. **Early validation**: Check integer constraint before continuing

**Result**: Both puzzles solved correctly in reasonable time

## Human's Performance Issue

**Why slow despite correct approach**:

1. **Similar algorithm to Chat GPT** but slower execution
2. **Upper bounds may be looser**: Could be searching larger spaces
3. **C# vs Python**: Potentially less optimized integer/rational arithmetic
4. **AI assistance needed**: User struggled with implementation

**Mitigating factors**:
- Parallelization across machines helped
- Progress reporting showed it was working
- Eventually got correct answer

## Code Quality Comparison

| Aspect | Claude CLI | Google Gemini | Chat GPT | Human |
|--------|-----------|---------------|----------|-------|
| **P1 Algorithm** | Brute force (works) | Gaussian (works) | DFS pruning (best) | Brute force (works) |
| **P2 Algorithm** | Incomplete | Unbounded (timeout) | ✅ RREF+bounded | ✅ RREF+bounded |
| **P1 Correctness** | ✅ Correct | ✅ Likely correct | ✅ Correct | ✅ Correct |
| **P2 Correctness** | ❌ Wrong | ❌ Timeout | ✅ **Correct** | ✅ Correct |
| Documentation | Good | Moderate | Excellent | Minimal |
| Performance P1 | Fast | Fast | Fast | Fast |
| Performance P2 | Fast (wrong) | Infinite | ⚡ **Fast** | 🐢 Slow |
| Code Clarity | Good | Moderate | Excellent | Good |

## Key Lessons

### 1. Problem Recognition Matters

All implementations recognized this as linear algebra, but approaches differed:
- **Puzzle 1**: All succeeded with various methods (brute force works for small n)
- **Puzzle 2**: Only those with **bounded search** succeeded

### 2. Integer Linear Programming is Hard

Key differences from GF(2):
- **Infinite solution space**: Can't just try 0/1
- **Need upper bounds**: Must limit search range
- **Non-negativity constraints**: Add complexity
- **Rational arithmetic**: Need exact computation

### 3. Chat GPT's Superior Implementation

**What set it apart**:
- Complete mathematical understanding
- Proper bound computation
- Clean, well-documented code
- Efficient pruning strategy

### 4. Google Gemini's Fatal Flaw

**Timeout indicates**:
- Missing bound calculation
- Unbounded search over integers
- No early termination conditions

**5+ hours** is not "slow" - it's **fundamentally broken** (wrong algorithm or infinite loop)

### 5. Human's Struggle Despite AI Help

**Interesting note**: User needed AI assistance but still ended up slow
- Correct algorithm but inefficient implementation
- Shows the gap between knowing approach and efficient execution

## Conclusion

Day 10 demonstrates **linear algebra problem-solving** with varying success:

- **Claude CLI**: ✅ Puzzle 1 correct, ❌ Puzzle 2 wrong (incomplete implementation)
- **Google Gemini**: ⏱️ **Complete failure** on Puzzle 2 (5+ hour timeout)
- **Chat GPT**: ✅ ✅ **Both puzzles correct and fast** - clear winner
- **Human**: ✅ Both correct but slow, needed AI assistance

**Key Insights**:

1. **Puzzle 1 is easy**: Multiple approaches work (brute force, Gaussian, DFS)
2. **Puzzle 2 is hard**: Requires RREF + bounded free variable search
3. **Bounds are critical**: Without upper bounds, search space is infinite
4. **Chat GPT excelled**: Only AI with complete, efficient solution
5. **Mathematical insight wins**: Recognizing structure >> brute force

**Best implementation**: Chat GPT (correct, fast, well-documented)
**Worst failure**: Google Gemini (5+ hour timeout = broken algorithm)
**Most effort**: Human (correct but struggled, needed AI help)

**The critical lesson**: For integer linear programming, you cannot simply enumerate all possibilities. You must:
1. Use RREF to identify free variables
2. **Compute tight upper bounds** for free variables
3. Systematically search bounded space
4. Use exact arithmetic (no floating point)
5. Validate integer constraints

Without proper bounds, you get infinite loops or exponential blowup - as Google Gemini discovered the hard way.
