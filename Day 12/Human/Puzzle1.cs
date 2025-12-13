using System.Text.RegularExpressions;

namespace Human
{
    public static class Puzzle1
    {
        public static List<Shape> Shapes { get; set; }
        public static List<Region> Regions { get; set; }

        // Cache for shape variations to avoid recalculating
        private static Dictionary<Shape, List<char[][]>> variationsCache = new Dictionary<Shape, List<char[][]>>();

        // Counter for tracking attempts (for debugging/optimization)
        private static long attemptCounter = 0;

        public static Int64 Solve(string[] fileInput)
        {
            Shapes = new List<Shape>();
            Regions = new List<Region>();
            var total = 0;

            ParseInput(fileInput);

            //Console.WriteLine($"Found {Shapes.Count} shapes and {Regions.Count} regions\n");

            // Display all shapes
            //Console.WriteLine("Available Shapes:");
            //Console.WriteLine(new string('-', 60));
            //for (int i = 0; i < Shapes.Count; i++)
            //{
            //    Console.WriteLine($"\nShape {i}:");
            //    PrintShapeColored(Shapes[i], i);
            //}
            //Console.WriteLine(new string('-', 60));
            //Console.WriteLine();

            int regionNum = 1;
            foreach (var region in Regions)
            {
                // Clear cache for new region
                variationsCache.Clear();
                attemptCounter = 0;

                //Console.WriteLine(new string('=', 60));
                //Console.WriteLine($"REGION {regionNum}: {region.width}x{region.height}");
                //Console.WriteLine(new string('=', 60));

                var grid = InitialGrid(region.height, region.width);
                var shapesToAdd = new List<Shape>();

                // Build list of all shapes needed for this region
                foreach (var shapesQuantity in region.ShapesQuantity)
                {
                    var shape = Shapes[shapesQuantity.ShapeIndex];
                    for (var i = 0; i < shapesQuantity.Quantity; i++)
                    {
                        shapesToAdd.Add(shape);
                    }
                }

                // OPTIMIZATION: Sort shapes by size (largest first) to reduce search space
                shapesToAdd = shapesToAdd.OrderByDescending(s => GetShapeArea(s)).ToList();

                //Console.WriteLine($"Shapes to place: {shapesToAdd.Count}");
                //Console.WriteLine("\nInitial grid:");
                //PrintGrid(grid);

                // Try to place all shapes - if successful, increment total
                // Set showProgress to true to see solving progress (can slow down for large grids)
                bool showProgress = false; // Change to true to see progress

                var startTime = DateTime.Now;
                if (TryPlaceAllShapes(grid, shapesToAdd, 0, showProgress))
                {
                    var elapsed = (DateTime.Now - startTime).TotalSeconds;
                    total++;
                    //Console.ForegroundColor = ConsoleColor.Green;
                    //Console.WriteLine($"\n✓ Region {regionNum}: SUCCESS! (solved in {elapsed:F2}s, {attemptCounter:N0} attempts)");
                    //Console.ResetColor();
                    //Console.WriteLine("\nFinal solution:");
                    //PrintGridColored(grid);
                }
                else
                {
                    var elapsed = (DateTime.Now - startTime).TotalSeconds;
                    //Console.ForegroundColor = ConsoleColor.Red;
                    //Console.WriteLine($"\n✗ Region {regionNum}: FAILED - Cannot fit all shapes (checked in {elapsed:F2}s, {attemptCounter:N0} attempts)");
                    //Console.ResetColor();
                }

                //Console.WriteLine();
                regionNum++;
            }

            //Console.WriteLine(new string('=', 60));
            //Console.WriteLine($"FINAL RESULT: {total} out of {Regions.Count} regions can fit all presents");
            //Console.WriteLine(new string('=', 60));

            return total;
        }

        // Main recursive backtracking function
        private static bool TryPlaceAllShapes(char[][] grid, List<Shape> shapes, int shapeIndex, bool showProgress = false)
        {
            // Base case: all shapes placed successfully
            if (shapeIndex >= shapes.Count)
            {
                return true;
            }

            // OPTIMIZATION: Check if remaining shapes can fit in remaining space
            int remainingArea = 0;
            for (int i = shapeIndex; i < shapes.Count; i++)
            {
                remainingArea += GetShapeArea(shapes[i]);
            }

            int emptySpace = GetEmptySpace(grid);
            if (remainingArea > emptySpace)
            {
                return false; // Impossible to fit remaining shapes
            }

            var shape = shapes[shapeIndex];

            // OPTIMIZATION: Use cached variations
            if (!variationsCache.ContainsKey(shape))
            {
                variationsCache[shape] = GetAllVariations(shape);
            }
            var variations = variationsCache[shape];

            // OPTIMIZATION: Find the first empty cell to start from (reduces search space)
            int startRow = -1, startCol = -1;
            bool foundEmpty = false;
            for (int row = 0; row < grid.Length && !foundEmpty; row++)
            {
                for (int col = 0; col < grid[0].Length && !foundEmpty; col++)
                {
                    if (grid[row][col] == '.')
                    {
                        startRow = row;
                        startCol = col;
                        foundEmpty = true;
                    }
                }
            }

            // If no empty cell found, something went wrong
            if (!foundEmpty)
            {
                return false;
            }

            // Try placing this shape starting from the first empty cell
            for (int row = startRow; row < grid.Length; row++)
            {
                int colStart = (row == startRow) ? startCol : 0;
                for (int col = colStart; col < grid[0].Length; col++)
                {
                    // Try each variation (rotation/flip) of the shape
                    foreach (var variation in variations)
                    {
                        attemptCounter++;

                        // Try to place the shape
                        if (CanPlaceShape(grid, row, col, variation))
                        {
                            // Place the shape
                            char label = (char)('A' + shapeIndex);
                            PlaceShape(grid, row, col, variation, label);

                            // Optional: Show progress
                            if (showProgress)
                            {
                               // Console.SetCursorPosition(0, Console.CursorTop);
                              //  Console.Write($"Trying shape {shapeIndex + 1}/{shapes.Count} at ({row},{col})...     ");
                            }

                            // Recursively try to place remaining shapes
                            if (TryPlaceAllShapes(grid, shapes, shapeIndex + 1, showProgress))
                            {
                                return true; // Solution found!
                            }

                            // Backtrack: remove the shape
                            RemoveShape(grid, row, col, variation);
                        }
                    }
                }
            }

            return false; // No valid placement found
        }

        // Check if a shape can be placed at the given position
        private static bool CanPlaceShape(char[][] grid, int startRow, int startCol, char[][] pattern)
        {
            int height = pattern.Length;
            int width = pattern[0].Length;

            // Check bounds
            if (startRow + height > grid.Length || startCol + width > grid[0].Length)
                return false;

            // Check each cell of the pattern
            for (int i = 0; i < height; i++)
            {
                for (int j = 0; j < width; j++)
                {
                    if (pattern[i][j] == '#')
                    {
                        // Check if the grid cell is already occupied
                        if (grid[startRow + i][startCol + j] != '.')
                        {
                            return false;
                        }
                    }
                }
            }

            return true;
        }

        // Place a shape on the grid
        private static void PlaceShape(char[][] grid, int startRow, int startCol, char[][] pattern, char label)
        {
            int height = pattern.Length;
            int width = pattern[0].Length;

            for (int i = 0; i < height; i++)
            {
                for (int j = 0; j < width; j++)
                {
                    if (pattern[i][j] == '#')
                    {
                        grid[startRow + i][startCol + j] = label;
                    }
                }
            }
        }

        // Remove a shape from the grid (backtracking)
        private static void RemoveShape(char[][] grid, int startRow, int startCol, char[][] pattern)
        {
            int height = pattern.Length;
            int width = pattern[0].Length;

            for (int i = 0; i < height; i++)
            {
                for (int j = 0; j < width; j++)
                {
                    if (pattern[i][j] == '#')
                    {
                        grid[startRow + i][startCol + j] = '.';
                    }
                }
            }
        }

        // Get all rotations and flips of a shape
        private static List<char[][]> GetAllVariations(Shape shape)
        {
            var variations = new List<char[][]>();
            var current = shape.pattern;

            // Original
            variations.Add(CopyPattern(current));

            // Rotate 90, 180, 270
            for (int i = 0; i < 3; i++)
            {
                current = Rotate90(current);
                variations.Add(CopyPattern(current));
            }

            // Flip and repeat rotations
            current = FlipHorizontal(shape.pattern);
            variations.Add(CopyPattern(current));

            for (int i = 0; i < 3; i++)
            {
                current = Rotate90(current);
                variations.Add(CopyPattern(current));
            }

            // Remove duplicates
            return RemoveDuplicatePatterns(variations);
        }

        // Calculate the number of cells occupied by a shape
        private static int GetShapeArea(Shape shape)
        {
            int area = 0;
            for (int i = 0; i < shape.pattern.Length; i++)
            {
                for (int j = 0; j < shape.pattern[i].Length; j++)
                {
                    if (shape.pattern[i][j] == '#')
                    {
                        area++;
                    }
                }
            }
            return area;
        }

        // Calculate empty space remaining in grid
        private static int GetEmptySpace(char[][] grid)
        {
            int empty = 0;
            for (int i = 0; i < grid.Length; i++)
            {
                for (int j = 0; j < grid[i].Length; j++)
                {
                    if (grid[i][j] == '.')
                    {
                        empty++;
                    }
                }
            }
            return empty;
        }

        // Rotate pattern 90 degrees clockwise
        private static char[][] Rotate90(char[][] pattern)
        {
            int height = pattern.Length;
            int width = pattern[0].Length;
            var rotated = new char[width][];

            for (int i = 0; i < width; i++)
            {
                rotated[i] = new char[height];
                for (int j = 0; j < height; j++)
                {
                    rotated[i][j] = pattern[height - 1 - j][i];
                }
            }

            return rotated;
        }

        // Flip pattern horizontally
        private static char[][] FlipHorizontal(char[][] pattern)
        {
            int height = pattern.Length;
            int width = pattern[0].Length;
            var flipped = new char[height][];

            for (int i = 0; i < height; i++)
            {
                flipped[i] = new char[width];
                for (int j = 0; j < width; j++)
                {
                    flipped[i][j] = pattern[i][width - 1 - j];
                }
            }

            return flipped;
        }

        // Copy a pattern
        private static char[][] CopyPattern(char[][] pattern)
        {
            return pattern.Select(row => row.ToArray()).ToArray();
        }

        // Remove duplicate patterns from the list
        private static List<char[][]> RemoveDuplicatePatterns(List<char[][]> patterns)
        {
            var unique = new List<char[][]>();

            foreach (var pattern in patterns)
            {
                bool isDuplicate = false;
                foreach (var existing in unique)
                {
                    if (PatternsEqual(pattern, existing))
                    {
                        isDuplicate = true;
                        break;
                    }
                }

                if (!isDuplicate)
                {
                    unique.Add(pattern);
                }
            }

            return unique;
        }

        // Check if two patterns are equal
        private static bool PatternsEqual(char[][] p1, char[][] p2)
        {
            if (p1.Length != p2.Length) return false;
            if (p1[0].Length != p2[0].Length) return false;

            for (int i = 0; i < p1.Length; i++)
            {
                for (int j = 0; j < p1[0].Length; j++)
                {
                    if (p1[i][j] != p2[i][j])
                        return false;
                }
            }

            return true;
        }




        private static void PrintShapeColored(Shape shape, int shapeIndex)
        {
            ConsoleColor[] colors = new ConsoleColor[]
            {
                ConsoleColor.Cyan,
                ConsoleColor.Yellow,
                ConsoleColor.Magenta,
                ConsoleColor.Green,
                ConsoleColor.Blue,
                ConsoleColor.Red,
                ConsoleColor.DarkCyan,
                ConsoleColor.DarkYellow,
                ConsoleColor.DarkMagenta,
                ConsoleColor.DarkGreen,
                ConsoleColor.DarkBlue,
                ConsoleColor.DarkRed
            };

            int colorIndex = shapeIndex % colors.Length;

            for (int i = 0; i < shape.pattern.Length; i++)
            {
                for (int j = 0; j < shape.pattern[i].Length; j++)
                {
                    if (shape.pattern[i][j] == '#')
                    {
                        Console.ForegroundColor = colors[colorIndex];
                        Console.Write('█');
                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.DarkGray;
                        Console.Write('·');
                    }
                }
                Console.WriteLine();
            }
            Console.ResetColor();
        }

        private static char[][] InitialGrid(int height, int width)
        {
            var grid = new char[height][];
            for (int i = 0; i < height; i++)
            {
                grid[i] = new string('.', width).ToArray();
            }
            return grid;
        }

        private static void ParseInput(string[] fileInput)
        {
            string shapePattern = @"^[#.]+$";
            string regionPattern = @"^\d+x\d+:( \d+)+$";

            for (int i = 0; i < fileInput.Length; i++)
            {
                // Check if this is the start of a shape definition
                if (i < fileInput.Length - 2 &&
                    fileInput[i].Contains(':') &&
                    Regex.IsMatch(fileInput[i + 1], shapePattern))
                {
                    Shape shape = new Shape();
                    shape.pattern = new char[3][];

                    for (var j = 0; j < 3; j++)
                    {
                        shape.pattern[j] = fileInput[i + 1 + j].ToArray();
                    }

                    Shapes.Add(shape);
                    i += 3; // Skip the shape lines
                }
                else if (Regex.IsMatch(fileInput[i], regionPattern))
                {
                    var s = fileInput[i];
                    var region = new Region();

                    region.width = int.Parse(s.Substring(0, s.IndexOf('x')));
                    region.height = int.Parse(s.Substring(s.IndexOf('x') + 1, s.IndexOf(':') - (s.IndexOf('x') + 1)));

                    var q = s.Substring(s.IndexOf(':') + 1).Trim();
                    var split = q.Split(' ');

                    for (var j = 0; j < split.Length; j++)
                    {
                        var quantity = int.Parse(split[j]);
                        if (quantity > 0) // Only add if quantity > 0
                        {
                            var shapeQuantity = new ShapesQuantity
                            {
                                ShapeIndex = j,
                                Quantity = quantity
                            };
                            region.ShapesQuantity.Add(shapeQuantity);
                        }
                    }

                    Regions.Add(region);
                }
            }
        }
    }

    public class Region
    {
        public int width { get; set; }
        public int height { get; set; }
        public List<ShapesQuantity> ShapesQuantity { get; set; }

        public Region()
        {
            ShapesQuantity = new List<ShapesQuantity>();
        }
    }

    public class ShapesQuantity
    {
        public int ShapeIndex { get; set; }
        public int Quantity { get; set; }
    }

    public class Shape
    {
        public char[][] pattern { get; set; }

        public Shape()
        {
            pattern = new char[3][];
        }
    }
}