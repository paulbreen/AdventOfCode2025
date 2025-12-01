using Human;
using System.Diagnostics;

string filename = "input.txt";
int max = 99;
int startPosition = 50;

var rotations = File.ReadAllLines(filename);

var timer = new Stopwatch();
timer.Start();

var puzzleOneAnswer =  PuzzleOne.Solve(max, startPosition, rotations);
Console.WriteLine($"Answer is {puzzleOneAnswer}");

var puzzleTwoAnswer = PuzzleTwo.Solve(max, startPosition, rotations);
Console.WriteLine($"Answer is {puzzleTwoAnswer}");

timer.Stop();
Console.WriteLine($"Duration : {timer.ElapsedMilliseconds} ms");