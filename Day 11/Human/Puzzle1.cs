
namespace Human
{
    public static class Puzzle1
    {
        public static Int64 Solve(string[] fileInput)
        {
            // Build adjacency list
            var graph = new Dictionary<string, List<string>>();

            foreach (var line in fileInput)
            {
                var parts = line.Split(':');
                var node = parts[0].Trim();
                var outputs = parts[1].Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries);

                graph[node] = new List<string>(outputs);
            }

            // Count all paths from "you" to "out"
            var pathCount = CountPaths(graph, "you", "out", new HashSet<string>());

            return pathCount;
        }

        private static long CountPaths(Dictionary<string, List<string>> graph, string current,
            string target, HashSet<string> visited)
        {
            // Reached destination
            if (current == target)
            {
                return 1;
            }

            // Dead end - no outputs
            if (!graph.ContainsKey(current))
            {
                return 0;
            }

            // Cycle detection - already visited this node in current path
            if (visited.Contains(current))
            {
                return 0;
            }

            // Mark as visited for this path
            visited.Add(current);

            // Explore all outputs
            long count = 0;
            foreach (var next in graph[current])
            {
                count += CountPaths(graph, next, target, visited);
            }

            // Backtrack - remove from visited so other paths can use this node
            visited.Remove(current);

            return count;
        }
    }
}