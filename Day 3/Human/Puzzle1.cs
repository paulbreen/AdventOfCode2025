namespace Human
{
    public static class Puzzle1
    {
        public static int Solve(string[] fileInput)
        {
            int total = 0;

            foreach (var batteryBank in fileInput)
            {
                char largest ;
                char secondLargest;

                List<char> voltageArray = batteryBank.Select(c => c).ToList();

                largest = voltageArray.SkipLast(1).Max();

                var index = voltageArray.IndexOf((char)largest);
                secondLargest = voltageArray.GetRange(index + 1, voltageArray.Count - index - 1).Max();

                total = total + ((largest - '0') * 10) + (secondLargest - '0');
            }

            return total;
        }
    }
}
