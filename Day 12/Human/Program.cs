using Human;
using System.Diagnostics;

var file = "input.txt";

var input = File.ReadAllLines(file);

var stopWatch = new Stopwatch();

stopWatch.Start();

var solution1 = Puzzle1.Solve(input);

stopWatch.Stop();

Console.WriteLine($"Puzzle 1 ans {solution1}");


Console.WriteLine($"Duration : {stopWatch.ElapsedMilliseconds} ms");