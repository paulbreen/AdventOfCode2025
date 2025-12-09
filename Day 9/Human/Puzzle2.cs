
namespace Human
{
    public static class Puzzle2
    {
        public static Int64 Solve(string[] fileInput)
        {
            var redTiles = new List<Location>();

            foreach (var line in fileInput)
            {
                var s = line.Split(',');
                redTiles.Add(new Location
                {
                    x = int.Parse(s[1]),
                    y = int.Parse(s[0])
                });
            }

            long largest = 0;
            int count = redTiles.Count;

            // Create a HashSet for faster red tile lookups
            var redTileSet = new HashSet<(int x, int y)>(
                redTiles.Select(t => (t.x, t.y))
            );

            for (int i = 0; i < count; i++)
            {
                for (int j = i + 1; j < count; j++)
                {
                    var corner1 = redTiles[i];
                    var corner2 = redTiles[j];

                    // Get rectangle bounds
                    int minX = Math.Min(corner1.x, corner2.x);
                    int maxX = Math.Max(corner1.x, corner2.x);
                    int minY = Math.Min(corner1.y, corner2.y);
                    int maxY = Math.Max(corner1.y, corner2.y);

                    // Check if rectangle is valid (all tiles are red or green)
                    if (IsValidRectangle(minX, maxX, minY, maxY, redTiles, redTileSet))
                    {
                        long area = (long)(maxX - minX + 1) * (maxY - minY + 1);
                        if (area > largest)
                        {
                            largest = area;
                        }
                    }
                }
            }

            return largest;
        }

        private static bool IsValidRectangle(int minX, int maxX, int minY, int maxY,
            List<Location> redTiles, HashSet<(int x, int y)> redTileSet)
        {
            // Check the 4 corners first (fast check)
            var corners = new[]
            {
        (minX, minY),
        (minX, maxY),
        (maxX, minY),
        (maxX, maxY)
    };

            foreach (var corner in corners)
            {
                if (!redTileSet.Contains(corner) && !IsInsideOrOnPolygon(corner.Item1, corner.Item2, redTiles))
                {
                    return false;
                }
            }

            // For a more thorough check, sample points along edges
            // Check top and bottom edges
            for (int x = minX; x <= maxX; x++)
            {
                if (!IsGreenOrRed((x, minY), redTiles, redTileSet)) return false;
                if (!IsGreenOrRed((x, maxY), redTiles, redTileSet)) return false;
            }

            // Check left and right edges
            for (int y = minY; y <= maxY; y++)
            {
                if (!IsGreenOrRed((minX, y), redTiles, redTileSet)) return false;
                if (!IsGreenOrRed((maxX, y), redTiles, redTileSet)) return false;
            }

            return true;
        }

        private static bool IsGreenOrRed((int x, int y) point, List<Location> redTiles,
            HashSet<(int x, int y)> redTileSet)
        {
            // Check if it's a red tile
            if (redTileSet.Contains(point))
                return true;

            // Check if it's on an edge between consecutive red tiles
            for (int i = 0; i < redTiles.Count; i++)
            {
                var from = redTiles[i];
                var to = redTiles[(i + 1) % redTiles.Count];

                if (IsOnEdge(point, from, to))
                    return true;
            }

            // Check if it's inside the polygon
            if (IsInsidePolygon(point.x, point.y, redTiles))
                return true;

            return false;
        }

        private static bool IsOnEdge((int x, int y) point, Location from, Location to)
        {
            // Check if point is on the line segment between from and to
            if (from.x == to.x) // Vertical line
            {
                if (point.x != from.x) return false;
                int minY = Math.Min(from.y, to.y);
                int maxY = Math.Max(from.y, to.y);
                return point.y >= minY && point.y <= maxY;
            }
            else if (from.y == to.y) // Horizontal line
            {
                if (point.y != from.y) return false;
                int minX = Math.Min(from.x, to.x);
                int maxX = Math.Max(from.x, to.x);
                return point.x >= minX && point.x <= maxX;
            }

            return false;
        }

        private static bool IsInsidePolygon(int x, int y, List<Location> polygon)
        {
            // Ray casting algorithm for point-in-polygon test
            bool inside = false;
            int n = polygon.Count;

            for (int i = 0, j = n - 1; i < n; j = i++)
            {
                if ((polygon[i].y > y) != (polygon[j].y > y) &&
                    x < (polygon[j].x - polygon[i].x) * (y - polygon[i].y) /
                        (double)(polygon[j].y - polygon[i].y) + polygon[i].x)
                {
                    inside = !inside;
                }
            }

            return inside;
        }

        private static bool IsInsideOrOnPolygon(int x, int y, List<Location> polygon)
        {
            // Check if on edge first
            for (int i = 0; i < polygon.Count; i++)
            {
                var from = polygon[i];
                var to = polygon[(i + 1) % polygon.Count];
                if (IsOnEdge((x, y), from, to))
                    return true;
            }

            return IsInsidePolygon(x, y, polygon);
        }
    }
}

