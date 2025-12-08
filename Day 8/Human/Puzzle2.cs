
namespace Human
{
    public static class Puzzle2
    {
        public static Int64 Solve(string[] fileInput)
        {
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

            //Console.WriteLine($"Total pairs: {pairs.Count}");

            // Sort pairs by distance
            pairs.Sort((a, b) => a.distance.CompareTo(b.distance));

            // Use Union-Find to connect pairs until all are in one circuit
            var uf = new UnionFind(n);
            int pairsProcessed = 0;
            int lastConnectedI = -1;
            int lastConnectedJ = -1;

            foreach (var pair in pairs)
            {
                int i = pair.i;
                int j = pair.j;
                double dist = pair.distance;

                if (uf.Union(i, j))
                {
                    // This pair was successfully connected
                    lastConnectedI = i;
                    lastConnectedJ = j;
                    pairsProcessed++;

                    // Check if all boxes are now in one circuit
                    if (uf.GetNumSets() == 1)
                    {
                        break;
                    }
                }
            }

            if (lastConnectedI >= 0 && lastConnectedJ >= 0)
            {
                int x1 = boxes[lastConnectedI].X;
                int x2 = boxes[lastConnectedJ].X;
                long result = (long)x1 * x2;

                return result;
            }
            else
            {
                return 0;
            }
        }
    }
}

