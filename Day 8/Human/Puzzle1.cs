
namespace Human
{
    public static class Puzzle1
    {
        public static Int64 Solve(string[] fileInput)
        {
            var total = 0;
            var target_pairs = 1000;

            // Parse junction boxes
            var boxes = new List<Point3D>();
            foreach (var line in fileInput)
            {
                if (string.IsNullOrWhiteSpace(line)) continue;

                var parts = line.Split(',');
                int x = int.Parse(parts[0].Trim());
                int y = int.Parse(parts[1].Trim());
                int z = int.Parse(parts[2].Trim());
                boxes.Add(new Point3D(x, y, z));
            }

            int n = boxes.Count;
            //Console.WriteLine($"Found {n} junction boxes");

            // Calculate all pairwise distances
            var pairs = new List<(int i, int j, double distance)>();
            for (int i = 0; i < n; i++)
            {
                for (int j = i + 1; j < n; j++)
                {
                    double dist = boxes[i].DistanceTo(boxes[j]);
                    pairs.Add((i, j, dist));
                }
            }

            // Sort pairs by distance
            pairs.Sort((a, b) => a.distance.CompareTo(b.distance));

            // Use Union-Find to process the closest pairs
            var uf = new UnionFind(n);
            int pairsProcessed = 0;
            

            foreach (var pair in pairs)
            {
                if (pairsProcessed >= 1000)
                    break;

                int i = pair.i;
                int j = pair.j;
                double dist = pair.distance;

                uf.Union(i, j); // Connect them (or try to if already connected)
                pairsProcessed++;
            }

            //Console.WriteLine($"\nProcessed {pairsProcessed} pairs");

            // Get circuit sizes
            var circuitSizes = uf.GetCircuitSizes();
            circuitSizes.Sort((a, b) => b.CompareTo(a)); // Sort descending

            // Multiply the three largest circuit sizes
            if (circuitSizes.Count >= 3)
            {
                long result = (long)circuitSizes[0] * circuitSizes[1] * circuitSizes[2];
                return result; 
            }
            else
            {
                return 0;
            }
        }
    }
}
