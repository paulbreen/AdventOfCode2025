# Playground Circuit Solver

## Language Choice
Go was selected for these reasons:
- Efficient handling of ~2 million distance computations and sorting.
- Simple, dependency-free compilation to a single binary.
- Fast execution and minimal memory overhead.
- Clean, maintainable syntax.

## Requirements
- Go 1.22 or later

## Build Instructions
go build -o solver main.go


## Run Command
Place `input.txt` in the same directory, then run:
./solver


## Output Format
The program prints:
Puzzle 1: <result>
Puzzle 2: <result>
Total Duration: <time>ms


## Dependencies
No external libraries. Only Go standard library.

## Notes
- The program computes all pairwise distances, sorts them, and performs Union-Find merges.
- Puzzle 1 stops after the first 1000 successful merges.
- Puzzle 2 continues until exactly one connected component remains.
