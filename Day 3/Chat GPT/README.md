# Day 3 – Lobby – Puzzle Solver

This repository contains a single executable that solves both parts of the "Lobby" puzzle using the same `input.txt` file. 

- **Puzzle 1**: For each line (“bank”) of digits, pick exactly **2 digits** in order to form the largest possible 2-digit number, then sum over all banks. :contentReference[oaicite:2]{index=2}  
- **Puzzle 2**: For each bank, pick exactly **12 digits** in order to form the largest possible 12-digit number, then sum over all banks. :contentReference[oaicite:3]{index=3}  

The program also measures execution time for each puzzle and prints the total runtime in milliseconds.

## Language Choice

**Language:** Rust

**Why Rust?**

- **Performance**: Compiles to native code and has predictable, zero-cost abstractions; ideal for micro-benchmarks and Advent-of-Code-style comparisons.
- **Memory safety without GC**: No runtime pauses, no surprises from allocation patterns when chasing sub-millisecond runtimes.
- **Strong type system**: Reduces the chance of subtle integer overflows or lifetime bugs, with good compiler diagnostics.

Given that the puzzles are dominated by tight loops over digit sequences and simple arithmetic, Rust provides both high performance and straightforward, readable code.

## Algorithm Overview

Each bank is a string of digits. For a fixed `k` (2 for puzzle 1, 12 for puzzle 2), we must:

- Select a **subsequence** of digits of length `k` (order preserved).
- Maximize the resulting `k`-digit number (equivalently, maximize the subsequence **lexicographically**).

This is the classic “maximum subsequence of length `k`” problem:

1. Convert the line into a vector of digits.
2. Let `remove_left = n - k` (how many digits we’re allowed to discard).
3. Iterate digits from left to right, maintaining a monotonic stack:
   - While the top of the stack is less than the current digit, and we still have `remove_left > 0`, and we can still fill `k` digits with the remaining items, pop the stack.
   - Push the current digit if the stack length is `< k`; otherwise, discard it and decrement `remove_left`.
4. The stack now holds the lexicographically maximal subsequence of length `k`.
5. Convert the digits in the stack to an integer and sum over all banks.

This algorithm is **O(n)** per line and avoids quadratic behavior, which keeps runtimes negligible even for larger inputs.

## Prerequisites

- **Rust toolchain** (stable)
  - Recommended: latest stable (e.g. 1.80+)
- A standard OS shell (Linux, macOS, or Windows PowerShell / CMD)

No external libraries or crates are required beyond the Rust standard library.

## Files

- `main.rs` – Single-file Rust solution implementing both puzzles.
- `input.txt` – Puzzle input, one battery bank per line. :contentReference[oaicite:4]{index=4}

## Build Instructions

### Option 1: Using Cargo (recommended)

If you have a Cargo project, put `main.rs` in `src/main.rs`, then:

```bash
cargo build --release
