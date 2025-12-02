using Human;
using System.Diagnostics;

var file = "input.txt";

var productIdRanges = File.ReadAllText(file);

var stopWatch = new Stopwatch();

stopWatch.Start();

var solution1 = Puzzle1.Solve(productIdRanges);

var solution2 = Puzzle2.Solve(productIdRanges);

stopWatch.Stop();

Console.WriteLine($"Puzzle 1 ans {solution1}");

Console.WriteLine($"Puzzle 2 ans {solution2}");

Console.WriteLine($"Duration : {stopWatch.ElapsedMilliseconds} ms");