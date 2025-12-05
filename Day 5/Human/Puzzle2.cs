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

                    continue;
                }
            }

            var sortedRanges  = ranges.OrderBy(x => x.min).ToArray();

            long currentMin = sortedRanges[0].min;
            long currentMax = sortedRanges[0].max;

            for(int i = 1; i < sortedRanges.Count(); i++)
            {
                var range = sortedRanges[i];

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