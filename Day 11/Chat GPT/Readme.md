# Day 11 – Reactor Solver

This project solves both parts of the **“Reactor”** puzzle (Day 11) using the same input graph. 

The input file (`input.txt`) lists devices and the devices their outputs connect to, forming a directed graph. :contentReference[oaicite:6]{index=6}

## Problems

### Puzzle 1

Given the graph and a starting device `you`, count how many different paths lead to the device `out`.

- Each line is of the form: `device: child1 child2 ...`.
- Data only flows along edges in the given direction.
- We need to count all directed paths from `you` to `out`. :contentReference[oaicite:7]{index=7}

### Puzzle 2

Using the **same input graph**, count paths from `svr` (the server rack) to `out`, but only those that visit **both**:

- `dac` (digital-to-analog converter)
- `fft` (fast Fourier transform device)

The required result is:  
“How many of the paths from `svr` to `out` visit both `dac` and `fft` (in any order)?” :contentReference[oaicite:8]{index=8}

## Final Answers (for the provided `input.txt`)

From the provided input graph: :contentReference[oaicite:9]{index=9}

- **Puzzle 1:** `428`
- **Puzzle 2:** `331468292364745`

Running the solver prints:

```text
Puzzle 1: 428
Puzzle 2: 331468292364745
Total Duration: <time>ms
