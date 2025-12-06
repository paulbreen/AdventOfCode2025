# Cephalopod Math Solver

This project solves both parts of the “Trash Compactor / Cephalopod math” worksheet:

- Part One rules: `puzzle1.txt` :contentReference[oaicite:5]{index=5}  
- Part Two rules: `puzzle2.txt` :contentReference[oaicite:6]{index=6}  
- Worksheet input: `input.txt` :contentReference[oaicite:7]{index=7}  

The worksheet is a wide ASCII grid where:

- The top **numeric rows** contain the digits of the numbers.
- The bottom row contains the operator (`+` or `*`) for each problem.
- Problems are separated by **a full column of spaces**.

The solver:

- Parses the grid into independent problem blocks.
- Computes the Part One grand total.
- Reinterprets the same grid using cephalopod right-to-left column rules for Part Two.
- Prints both answers and the combined compute time.

---

## Language Choice

**Language:** Python 3

**Reasons:**

- Strong built-in support for:
  - String handling and 2D text grids.
  - Arbitrary-precision integers (important for large products).
- No compilation step; single-file script runnable with one command.
- Standard library provides:
  - `time.perf_counter` for precise timing.
  - `math.prod` for clean product computations.
- Minimal boilerplate while keeping the logic clear and readable.

This matches the puzzle requirements in `Prompt.md` for:

- Efficient string/data manipulation.
- Simple command-line execution.
- Minimizing external dependencies. :contentReference[oaicite:8]{index=8}  

---

## Files

- `solver.py` – main script implementing both puzzle solutions.
- `input.txt` – worksheet input grid (required at runtime).
- `puzzle1.txt`, `puzzle2.txt` – human-readable puzzle descriptions; not read by the program.

---

## Prerequisites

- **Python**: Version **3.8+** recommended  
  (Script uses only standard library modules: `sys`, `time`, `math`, `typing`.)

No external packages or frameworks are required.

---

## Build Instructions

No build/compile step is required.

Just ensure `solver.py` and `input.txt` are in the same directory.

---

## Run Command

From the directory containing `solver.py` and `input.txt`:

```bash
python solver.py
