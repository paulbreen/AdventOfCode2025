
using System.Text;

namespace Human
{
    public static class Puzzle2
    {
        public static Int64 Solve(string[] fileInput)
        {
            // Pad all lines to the same width
            int maxWidth = fileInput.Max(line => line.Length);
            for (int i = 0; i < fileInput.Length; i++)
            {
                fileInput[i] = fileInput[i].PadRight(maxWidth);
            }

            int numRows = fileInput.Length - 1; // Last row is operators
            int width = fileInput[0].Length;

            // Find problem blocks 
            var blocks = FindProblemBlocks(fileInput, numRows, width);

            long grandTotal = 0;

            foreach (var block in blocks)
            {
                int start = block.Item1;
                int end = block.Item2;

                // Get the operator for this block
                char op = GetOperator(fileInput[numRows], start, end);

                List<long> columnNumbers = new List<long>();

                // Process columns from RIGHT to LEFT within this block
                for (int col = end - 1; col >= start; col--)
                {
                    // Read this column TOP to BOTTOM to build one number
                    StringBuilder digits = new StringBuilder();

                    for (int row = 0; row < numRows; row++)
                    {
                        char ch = fileInput[row][col];
                        if (char.IsDigit(ch))
                        {
                            digits.Append(ch);
                        }
                    }

                    if (digits.Length > 0)
                    {
                        long number = long.Parse(digits.ToString());
                        columnNumbers.Add(number);
                    }
                }

                if (columnNumbers.Count > 0)
                {
                    long result = CalculateProblem(columnNumbers, op);
                    grandTotal += result;
                }
            }

            return grandTotal;
        }

        static List<Tuple<int, int>> FindProblemBlocks(string[] lines, int numRows, int width)
        {
            var blocks = new List<Tuple<int, int>>();

            int col = 0;
            while (col < width)
            {
                // Check if this is a separator column (all spaces in all rows including operator row)
                bool isSeparator = true;
                for (int row = 0; row <= numRows; row++)
                {
                    if (lines[row][col] != ' ')
                    {
                        isSeparator = false;
                        break;
                    }
                }

                if (isSeparator)
                {
                    col++;
                    continue;
                }

                // Start of a problem block
                int start = col;
                col++;

                // Find the end of this block
                while (col < width)
                {
                    bool allSpaces = true;
                    for (int row = 0; row <= numRows; row++)
                    {
                        if (lines[row][col] != ' ')
                        {
                            allSpaces = false;
                            break;
                        }
                    }

                    if (allSpaces)
                        break;

                    col++;
                }

                blocks.Add(Tuple.Create(start, col));
            }

            return blocks;
        }

        static char GetOperator(string operatorLine, int start, int end)
        {
            // Find the operator in this block
            for (int i = start; i < end; i++)
            {
                char ch = operatorLine[i];
                if (ch == '+' || ch == '*')
                {
                    return ch;
                }
            }
            return '+'; // Default fallback
        }

        static long CalculateProblem(List<long> numbers, char op)
        {
            if (numbers.Count == 0) return 0;

            long result = numbers[0];
            for (int i = 1; i < numbers.Count; i++)
            {
                if (op == '*')
                    result *= numbers[i];
                else if (op == '+')
                    result += numbers[i];
            }
            return result;
        }
    }
}