🚧 Puzzle Solver: Cafeteria Inventory
This project provides a solution to the two-part inventory management puzzle using the Go programming language.

🎯 Language Chosen and Justification
Language: Go (Golang)

Why Go? Go was selected for its simplicity, efficiency, and strong support for file I/O and string manipulation, which are the core requirements for this data processing task. It compiles to a single, fast binary, ensuring minimal dependencies and quick execution time, which meets the quality and performance standards.

🛠️ Prerequisites
Go Runtime: Version 1.18 or newer.

📦 Dependencies
No external dependencies are required. The solution uses only the Go Standard Library.

🔨 Build Instructions
Ensure you have the Go runtime installed.

Navigate to the directory containing main.go and input.txt.

Execute the following command to compile the Go source file into an executable:

Bash

go build main.go
This will create an executable file named main (or main.exe on Windows).

▶️ Run Command
Execute the compiled binary from the command line:

Bash

./main
(Use .\main.exe on Windows)

The program expects the input data to be in a file named input.txt in the same directory. It will output the results for both puzzles and the total execution time in milliseconds.