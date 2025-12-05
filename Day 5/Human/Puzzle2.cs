namespace Human
{
    public static class Puzzle2
    {
        public static long Solve(string[] fileInput)
        {
            long total = 0;

            var ranges  = new List<(long min, long max)>();

            for (int i = 0; i < fileInput.Length; i++)
            {
                if (string.IsNullOrEmpty(fileInput[i])) continue;

                if (fileInput[i].Contains('-'))
                {
                    var s = fileInput[i].Split('-');

                    ranges.Add((long.Parse(s[0]), long.Parse(s[1])));
                }
            }

            ranges.Sort((a, b) => a.min.CompareTo(b.min));

            long currentMin = ranges[0].min;
            long currentMax = ranges[0].max;

            for(int i = 1; i < ranges.Count; i++)
            {
                var range = ranges[i];

                if (range.min <= currentMax + 1)
                {
                    currentMax = Math.Max(currentMax, range.max);
                }
                else
                {
                    total += (currentMax - currentMin + 1);
                    currentMin = range.min;
                    currentMax = range.max;
                }
            }

            total += (currentMax - currentMin + 1);  // last one

            return total;
        }
    }
}