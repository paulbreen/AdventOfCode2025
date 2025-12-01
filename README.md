# Advent of Code 2024 - AI Agent Comparison

## Overview

This project compares how different AI agents generate code to solve [Advent of Code 2025](https://adventofcode.com/2025) problems. Each agent receives the same prompt and their generated solutions are evaluated based on:

- **Programming Language** used
- **Average Execution Time** (in milliseconds)

The goal is to analyze the approaches, efficiency, and language choices of various AI coding assistants when faced with identical programming challenges.

## Participating Agents

- **Claude CLI** - Anthropic's Claude via command line interface
- **Google Gemini** - Google's Gemini AI assistant
- **ChatGPT** - OpenAI's ChatGPT
- **Human** - Human-written baseline solutions

## Results

| Day | Claude CLI | Google Gemini | Human | ChatGPT |
|-----|------------|---------------|-------|---------|
| **Day 1** | Python<br>30.34ms |- |** 🟢 30.1ms** |- |
| **Day 2** | - | - | - | - |
| **Day 3** | - | - | - | - |
| **Day 4** | - | - | - | - |
| **Day 5** | - | - | - | - |
| **Day 6** | - | - | - | - |
| **Day 7** | - | - | - | - |
| **Day 8** | - | - | - | - |
| **Day 9** | - | - | - | - |
| **Day 10** | - | - | - | - |
| **Day 11** | - | - | - | - |
| **Day 12** | - | - | - | - |

**🟢** = Fastest solution for that day

## Methodology

1. Each agent receives an identical prompt containing:
   - The problem description from Advent of Code
   - Input/output requirements
   - Any relevant constraints

2. Solutions are executed on the same hardware with:
   - Consistent test inputs
   - Multiple runs to calculate average execution time
   - Validation against expected outputs

3. Results are recorded for both correctness and performance


## Analysis

Detailed analysis and insights will be added as more solutions are collected, including:
- Language preference trends
- Performance patterns across problem types
- Code quality and readability comparisons
- Interesting approaches or optimizations

## Contributing

If you'd like to add more AI agents to this comparison, please open an issue or submit a pull request!

## License

This project is for educational and comparison purposes. Advent of Code problems are created by [Eric Wastl](http://was.tl/).