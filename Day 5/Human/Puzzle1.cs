
namespace Human
{
    public static class Puzzle1
    {
        public static int Solve(string[] fileInput)
        {
            var ranges = new List<(Int64 min, Int64 max)>();
            var count = 0;

            for (int i = 0; i < fileInput.Length; i++)
            {
                if (string.IsNullOrEmpty(fileInput[i])) continue;

                if (fileInput[i].Contains('-'))
                {
                    var s = fileInput[i].Split('-');

                    ranges.Add((Int64.Parse(s[0]), Int64.Parse(s[1])));

                    continue;
                }

                var id = Int64.Parse(fileInput[i]);

                if(ranges.Any(x => x.min <= id && x.max >= id)) count++;
            }

            return count;
        }
    }
}
