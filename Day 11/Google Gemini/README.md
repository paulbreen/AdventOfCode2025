# Device Path Solver

This project solves two related path-counting puzzles on a directed acyclic graph (DAG) representing electrical conduits and devices.

## 🛠️ Language Chosen

**Python 3**

### Why Python?
Python was selected for its ease of use in **graph construction** (using `defaultdict` for the adjacency list) and for the simplicity of implementing the core algorithm: **Depth-First Search (DFS) with Memoization (Dynamic Programming)**. This approach is highly efficient for counting paths in a DAG, providing a clean and performant solution without the need for complex compilation or external libraries.

## 📋 Prerequisites

* **Language Version:** Python 3.6+
* **Runtime:** Standard Python 3 runtime environment.

## 📦 Dependencies

* **None.** Only standard built-in Python modules (`sys`, `time`, `collections`) are used.

## 🚀 Run Command

This single command executes the script, which reads `input.txt` and solves both puzzles sequentially.

```bash
python3 solution.py