using System.Data;

namespace Human
{
    public static class Puzzle2
    {
        public static Int64 Solve(string[] fileInput)
        {
            Int64 total = 0;
            int maxSize = 11;

            foreach (var batteryBank in fileInput)
            {
                var voltageArray = batteryBank.Select(c => c).ToArray();

                var result = FindLargest(voltageArray, maxSize);

                total += Int64.Parse(result);
            }

            return total;
        }

        public static string FindLargest(char[] batteryBank, int maxSize)
        {
            if (maxSize == -1) return string.Empty;

            var largest = batteryBank.Take(batteryBank.Length - maxSize).Distinct().Max(c => c);

            var indexOfLargest = Array.IndexOf(batteryBank, largest);

            batteryBank = batteryBank.Skip(indexOfLargest + 1).ToArray();

            return string.Concat(largest, FindLargest(batteryBank, maxSize - 1));
        }
    }
}