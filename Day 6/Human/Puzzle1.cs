
namespace Human
{
    public static class Puzzle1
    {
        public static Int64 Solve(string[] fileInput)
        {
            var problems = new Int64[fileInput.Length][];

            for (int i = 0; i < fileInput.Length - 1; i++)
            {
                problems[i] = fileInput[i].Trim().Split(' ').Where(x => !string.IsNullOrWhiteSpace(x)).Select(Int64.Parse).ToArray();
            }

            var operation = fileInput[fileInput.Length - 1].Trim().Split(' ').Where(x => !string.IsNullOrWhiteSpace(x)).Select(x => x).ToArray();

            long total = ApplyOperations(problems, operation);

            return total;
        }

        private static long ApplyOperations(long[][] problems, string[] operation)
        {
            Int64 total = 0;

            var width = problems[0].Length;
            var height = problems.Length;

            for (int i = 0; i < width; i++)
            {
                var digits = new List<long>();
                for (int j = 0; j < height - 1; j++)
                {
                    digits.Add(problems[j][i]);
                }

                if (operation[i] == "*")
                {
                    var ans = digits.Aggregate(1L, (acc, num) => (acc * num));
                    total += ans;
                }
                if (operation[i] == "+")
                {
                    var ans = digits.Aggregate(0L, (acc, num) => (acc + num));
                    total += ans;
                }
            }

            return total;
        }
    }
}
