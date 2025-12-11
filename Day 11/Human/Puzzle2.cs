using System.Diagnostics;

namespace Human
{
    public static class Puzzle2
    {
        public static Int64 Solve(string[] fileInput)
        {
            var graph = new Dictionary<string, List<string>>();

            foreach (var line in fileInput)
            {
                var parts = line.Split(':');
                var node = parts[0].Trim();
                var outputs = parts[1].Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries);
                graph[node] = new List<string>(outputs);
            }

            Console.WriteLine("Starting path search with memoization...");
            var sw = Stopwatch.StartNew();

            // Use memoization: cache results for (node, visitedDac, visitedFft)
            var memo = new Dictionary<string, long>();

            var pathCount = CountPathsMemo(graph, "svr", "out", false, false, memo);

            sw.Stop();
            Console.WriteLine($"Completed in {sw.Elapsed:mm\\:ss}");
            Console.WriteLine($"Total paths visiting both dac and fft: {pathCount}");

            return pathCount;
        }

        private static long CountPathsMemo(Dictionary<string, List<string>> graph,
            string current, string target, bool visitedDac, bool visitedFft,
            Dictionary<string, long> memo)
        {
            // Update visited flags
            if (current == "dac") visitedDac = true;
            if (current == "fft") visitedFft = true;

            // Reached destination
            if (current == target)
            {
                return (visitedDac && visitedFft) ? 1 : 0;
            }

            // Create memoization key
            var key = $"{current}|{visitedDac}|{visitedFft}";
            if (memo.ContainsKey(key))
            {
                return memo[key];
            }

            // Dead end
            if (!graph.ContainsKey(current))
            {
                memo[key] = 0;
                return 0;
            }

            // Explore all paths
            long count = 0;
            foreach (var next in graph[current])
            {
                count += CountPathsMemo(graph, next, target, visitedDac, visitedFft, memo);
            }

            memo[key] = count;
            return count;
        }
    }
}