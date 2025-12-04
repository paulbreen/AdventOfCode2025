using System.Data;

namespace Human
{
    public static class Puzzle2
    {
        public static int Solve(string[] fileInput)
        {
            // convert to 2d array;
            char[][] grid = new char[fileInput.Length][];
            char[][] completedGrid = new char[fileInput.Length][];
            for (int i = 0; i < fileInput.Length; i++)
            {
                grid[i] = fileInput[i].ToCharArray();
                completedGrid[i] = fileInput[i].ToCharArray();
            }

            var totalCount = 0;
            var iterationCount = 0;

            do 
            {
                iterationCount = 0;
                for (int i = 0; i < grid.Length; i++)
                {
                    for (int j = 0; j < grid[i].Length; j++)
                    {
                        if (grid[i][j] != '@') continue;

                        var adjacent = FindNeighbours(grid, i, j);

                        if (adjacent < 4)
                        {
                            totalCount++;
                            iterationCount++;

                            completedGrid[i][j] = 'x';
                        }
                    }
                }

                grid = completedGrid.Select(row => row.ToArray()).ToArray();
            } while(iterationCount > 0);
          
            return totalCount;
        }

        private static int FindNeighbours(char[][] grid, int row, int col)
        {
            int count = 0;

            // 8 directions: NW, N, NE, W, E, SW, S, SE
            int[] dRow = { -1, -1, -1, 0, 0, 1, 1, 1 };
            int[] dCol = { -1, 0, 1, -1, 1, -1, 0, 1 };

            for (int i = 0; i < 8; i++)
            {
                int newRow = row + dRow[i];
                int newCol = col + dCol[i];

                if (newRow >= 0 && newRow < grid.Length &&
                    newCol >= 0 && newCol < grid[newRow].Length &&
                    grid[newRow][newCol] == '@')
                {
                    count++;
                }
            }

            return count;
        }
    }
}