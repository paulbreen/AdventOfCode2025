# North Pole Safe Cracker

This tool autonomously solves the "Secret Entrance" puzzles to determine the safe combination and the secondary security protocol password.

## Language Choice: Python 3
Python was selected for its superior string processing capabilities and readability. Given the input size (~1000 lines) and the modulo arithmetic domain (0-99), Python's performance is more than sufficient, allowing for a solution that is both concise and easily maintainable without complex compilation steps.

## Prerequisites
* **Python 3.6+** installed on your system.
* The input file `input.txt` must be in the same directory as the script.

## Dependencies
* Standard Library only (`sys`, `time`, `os`). No external `pip` packages required.

## Build Instructions
No compilation is necessary. Python is an interpreted language.

## Run Command
Execute the solution from your terminal with a single command:

```bash
python solve.py