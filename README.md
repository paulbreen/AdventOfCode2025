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

## Code Results

| Day | Claude CLI | Google Gemini | Human | ChatGPT 5.1 |
|-----|------------|---------------|-------|---------|
| **Day 1** | Python<br>30.34ms |🟢 Python <br>  ** 8.92 ms ** 🟢|C# <br> 21.1ms | Python <br> 23.73 ms |
| **Day 2** | Python<br> 1155ms | Python<br>1056ms | C# <br> 2756ms | 🟢Python<br>60.3ms 🟢|
| **Day 3** | Python<br> 7.73ms | Python<br> 115.32ms | C# <br> 20ms | 🟢Rust <br> 0.290ms 🟢|
| **Day 4** | Python<br> 45ms | Python<br> 402.974ms |🟢 C# <br> 32 ms 🟢 |Python <br> 357.77ms |
| **Day 5** | Python<br> 4ms | Go<br> 503µs |🟢 C# <br> 14 ms 🟢 |Python <br> 566µs |
| **Day 6** | 🔴 | Python<br> 124ms |🟢 C# <br> 19 ms 🟢 |Python <br> 7.77ms |
| **Day 7** | Python<br> 🟢 🔴 | Python<br> 2.3ms  |🟢 C# <br> 19 ms 🟢 | Python<br> 🟢 🔴|
| **Day 8** | - | - | - | - |
| **Day 9** | - | - | - | - |
| **Day 10** | - | - | - | - |
| **Day 11** | - | - | - | - |
| **Day 12** | - | - | - | - |

**🟢** = Fastest solution for that day

## Correct Results
Simply given the problem, are the agents able to return the correct results via chat?

Prompt : "Help me solve the following problem, what is the correct answer to all puzzles?"

| Day | Claude Web | Google Gemini  | ChatGPT 5.1 |
|-----|------------|---------------|---------|
| **Day 1** | 🟢 🟢 | 🔴 🟢 | 🟢 🟢| 
| **Day 2** | 🟢 🟢 | 🔴 🔴 | 🟢 🟢 | 
| **Day 3** | 🟢 🟢 | 🔴 🔴 | 🟢 🟢 | 
| **Day 3** | 🟢 🟢 | 🔴 🔴 | 🟢 🟢 | 
| **Day 5** | 🟢 🟢 | 🔴 🔴 | 🟢 🟢 | 
| **Day 6** | 🟢 🟢 | 🔴 🔴 | 🟢 🟢 | 
| **Day 7** | 🟢 🟢 | 🔴 🔴 | 🟢 🟢 | 
| **Day 8** | - | - | - | 
| **Day 9** | - | - | - | 
| **Day 10** | - | - | - | 
| **Day 11** | - | - | - | 
| **Day 12** | - | - | - | 

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