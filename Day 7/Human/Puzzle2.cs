
namespace Human
{
    public static class Puzzle2
    {
        public static Int64 Solve(string[] fileInput)
        {
            var tachyon = new char[fileInput.Length][];

            for (int i = 0; i < fileInput.Length; i++)
            {
                tachyon[i] = fileInput[i].ToArray();
            }

            var startPosition = fileInput[0].IndexOf('S');

            var cache = new Dictionary<(int row, int col), long>();

            return CountTimelines(tachyon, 1, startPosition, cache);
        }


        private static long CountTimelines(char[][] manifold, int row, int col, Dictionary<(int, int), long> cache)
        {
            // reached the bottom
            if (row >= manifold.Length)
                return 1;

            // out of bounds
            if (col < 0 || col >= manifold[row].Length)
                return 0;

            // pre calculated
            if (cache.ContainsKey((row, col)))
                return cache[(row, col)];

            long result;

            // is splitter
            if (manifold[row][col] == '^')
            {
                long leftTimelines = CountTimelines(manifold, row + 1, col - 1, cache);
                long rightTimelines = CountTimelines(manifold, row + 1, col + 1, cache);
                result = leftTimelines + rightTimelines;
            }
            else
            {
                // Continue straight down
                result = CountTimelines(manifold, row + 1, col, cache);
            }

            // Cache the result
            cache[(row, col)] = result;

            return result;
        }
    }
}

