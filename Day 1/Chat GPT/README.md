# Secret Entrance Puzzle Solver

This repository contains a solution for two related puzzles involving a circular
dial (positions `0`–`99`) and a sequence of left/right rotations. The puzzles
and input format are defined in the provided puzzle description files and
`input.txt`. 

## Overview

- **Puzzle 1**:  
  Starting from position `50` on a 0–99 dial, follow all rotations. Count how
  many times, after completing each rotation, the dial is left pointing at `0`.

- **Puzzle 2 (method `0x434C49434B`)**:  
  Again start from position `50`. For each rotation, consider every single
  click as the dial moves one step at a time. Count how many times the dial
  points to `0` at any click (including when a rotation ends on `0`).

Both puzzles are solved against the same input (`input.txt`).

The program prints results and total runtime in the following format:

```text
Puzzle 1: [result]
Puzzle 2: [result]
Total Duration: [time]ms
