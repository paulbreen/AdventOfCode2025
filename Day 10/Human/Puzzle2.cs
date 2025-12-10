using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Diagnostics;

namespace Human
{
    public static class Puzzle2
    {
        public static Int64 Solve(string[] fileInput)
        {
            var stopwatch = Stopwatch.StartNew();
            Console.WriteLine($"Processing {fileInput.Length} machines...");

            var total = 0L;
            var lockObj = new object();
            var completed = 0;

            Parallel.For(0, fileInput.Length, new ParallelOptions
            {
                MaxDegreeOfParallelism = Environment.ProcessorCount
            }, i =>
            {
                var result = SolveMachine(fileInput[i]);

                lock (lockObj)
                {
                    total += result;
                    completed++;

                    if (completed % 20 == 0 || completed == fileInput.Length)
                    {
                        var elapsed = stopwatch.Elapsed;
                        var progress = completed * 100.0 / fileInput.Length;
                        Console.WriteLine($"{completed}/{fileInput.Length} ({progress:F1}%) - {elapsed:mm\\:ss} - Total: {total}");
                    }
                }
            });

            stopwatch.Stop();
            Console.WriteLine($"Completed in {stopwatch.Elapsed:mm\\:ss}. Final Total: {total}");

            return total;
        }

        private static long SolveMachine(string line)
        {
            // Parse
            var braceMatch = Regex.Match(line, @"\{([0-9,]+)\}");
            var target = braceMatch.Groups[1].Value.Split(',').Select(int.Parse).ToArray();

            var buttonMatches = Regex.Matches(line, @"\(([0-9,]+)\)");
            var buttons = buttonMatches.Cast<Match>()
                .Select(m => m.Groups[1].Value.Split(',').Select(int.Parse).ToArray())
                .ToArray();

            var n = target.Length;
            var m = buttons.Length;

            // Build matrix A
            var A = new int[n][];
            for (int i = 0; i < n; i++)
            {
                A[i] = new int[m];
                for (int j = 0; j < m; j++)
                {
                    A[i][j] = buttons[j].Contains(i) ? 1 : 0;
                }
            }

            // Calculate upper bounds for each button
            var ub = new int[m];
            for (int j = 0; j < m; j++)
            {
                var affectedCounters = new List<int>();
                for (int i = 0; i < n; i++)
                {
                    if (A[i][j] == 1)
                    {
                        affectedCounters.Add(target[i]);
                    }
                }
                ub[j] = affectedCounters.Count > 0 ? affectedCounters.Min() : 0;
            }

            // RREF decomposition
            var (M, pivotCols, pivotRowForCol) = RREF(A, target);

            var freeCols = new List<int>();
            for (int c = 0; c < m; c++)
            {
                if (!pivotCols.Contains(c))
                {
                    freeCols.Add(c);
                }
            }

            // Express pivot variables in terms of free variables
            var constTerm = new Dictionary<int, Rational>();
            var coeffs = new Dictionary<int, Dictionary<int, Rational>>();

            foreach (var c in pivotCols)
            {
                var r = pivotRowForCol[c];
                constTerm[c] = M[r][m]; // RHS
                coeffs[c] = new Dictionary<int, Rational>();

                foreach (var fc in freeCols)
                {
                    var val = M[r][fc];
                    if (!val.IsZero())
                    {
                        coeffs[c][fc] = -val;
                    }
                }
            }

            // DFS over free variables
            var xFree = new int[freeCols.Count];
            var bestSum = long.MaxValue;

            void DFS(int idx)
            {
                if (idx == freeCols.Count)
                {
                    // Build full solution
                    var x = new long[m];

                    // Assign free variables
                    for (int k = 0; k < freeCols.Count; k++)
                    {
                        x[freeCols[k]] = xFree[k];
                    }

                    // Compute pivot variables
                    foreach (var c in pivotCols)
                    {
                        var val = constTerm[c];
                        foreach (var kvp in coeffs[c])
                        {
                            val = val + kvp.Value * new Rational(x[kvp.Key]);
                        }

                        // Must be non-negative integer
                        if (!val.IsInteger() || val.Numerator < 0)
                        {
                            return;
                        }
                        x[c] = val.Numerator;
                    }

                    // Verify solution
                    for (int i = 0; i < n; i++)
                    {
                        long sum = 0;
                        for (int j = 0; j < m; j++)
                        {
                            if (A[i][j] == 1)
                            {
                                sum += x[j];
                            }
                        }
                        if (sum != target[i])
                        {
                            return;
                        }
                    }

                    var total = x.Sum();
                    if (total < bestSum)
                    {
                        bestSum = total;
                    }
                    return;
                }

                // Pruning
                var partialSum = xFree.Take(idx).Sum();
                if (partialSum >= bestSum)
                {
                    return;
                }

                var col = freeCols[idx];
                var maxV = ub[col];

                for (int v = 0; v <= maxV; v++)
                {
                    xFree[idx] = v;
                    DFS(idx + 1);
                }
                xFree[idx] = 0;
            }

            DFS(0);
            return bestSum == long.MaxValue ? 0 : bestSum;
        }

        private static (Rational[][] M, List<int> pivotCols, Dictionary<int, int> pivotRowForCol) RREF(int[][] A, int[] b)
        {
            var n = A.Length;
            var m = A[0].Length;

            // Build augmented matrix with rationals
            var M = new Rational[n][];
            for (int i = 0; i < n; i++)
            {
                M[i] = new Rational[m + 1];
                for (int j = 0; j < m; j++)
                {
                    M[i][j] = new Rational(A[i][j]);
                }
                M[i][m] = new Rational(b[i]);
            }

            var pivotCols = new List<int>();
            var pivotRowForCol = new Dictionary<int, int>();
            var row = 0;

            for (int col = 0; col < m; col++)
            {
                // Find pivot
                int? pivotRow = null;
                for (int r = row; r < n; r++)
                {
                    if (!M[r][col].IsZero())
                    {
                        pivotRow = r;
                        break;
                    }
                }

                if (pivotRow == null) continue;

                // Swap rows
                if (pivotRow.Value != row)
                {
                    var temp = M[row];
                    M[row] = M[pivotRow.Value];
                    M[pivotRow.Value] = temp;
                }

                // Scale to make pivot = 1
                var factor = M[row][col];
                if (!factor.IsOne())
                {
                    for (int c = col; c <= m; c++)
                    {
                        M[row][c] = M[row][c] / factor;
                    }
                }

                // Eliminate column from all other rows
                for (int r = 0; r < n; r++)
                {
                    if (r != row && !M[r][col].IsZero())
                    {
                        var f = M[r][col];
                        for (int c = col; c <= m; c++)
                        {
                            M[r][c] = M[r][c] - f * M[row][c];
                        }
                    }
                }

                pivotCols.Add(col);
                pivotRowForCol[col] = row;
                row++;
                if (row == n) break;
            }

            return (M, pivotCols, pivotRowForCol);
        }

        private struct Rational
        {
            public long Numerator;
            public long Denominator;

            public Rational(long num, long den = 1)
            {
                if (den == 0) throw new DivideByZeroException();

                var g = GCD(Math.Abs(num), Math.Abs(den));
                Numerator = num / g;
                Denominator = den / g;

                if (Denominator < 0)
                {
                    Numerator = -Numerator;
                    Denominator = -Denominator;
                }
            }

            public bool IsZero() => Numerator == 0;
            public bool IsOne() => Numerator == 1 && Denominator == 1;
            public bool IsInteger() => Denominator == 1;

            public static Rational operator +(Rational a, Rational b)
            {
                return new Rational(a.Numerator * b.Denominator + b.Numerator * a.Denominator,
                                   a.Denominator * b.Denominator);
            }

            public static Rational operator -(Rational a, Rational b)
            {
                return new Rational(a.Numerator * b.Denominator - b.Numerator * a.Denominator,
                                   a.Denominator * b.Denominator);
            }

            public static Rational operator *(Rational a, Rational b)
            {
                return new Rational(a.Numerator * b.Numerator, a.Denominator * b.Denominator);
            }

            public static Rational operator /(Rational a, Rational b)
            {
                return new Rational(a.Numerator * b.Denominator, a.Denominator * b.Numerator);
            }

            public static Rational operator -(Rational a)
            {
                return new Rational(-a.Numerator, a.Denominator);
            }

            private static long GCD(long a, long b)
            {
                while (b != 0)
                {
                    var temp = b;
                    b = a % b;
                    a = temp;
                }
                return a;
            }
        }
    }
}