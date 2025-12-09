
namespace Human
{
    public static class Puzzle1
    {
        public static Int64 Solve(string[] fileInput)
        {
            var redTiles = new Location[fileInput.Length];

            for (int i = 0; i < fileInput.Length; i++)
            {
                var s = fileInput[i].Split(',');

                redTiles[i] = new Location { x = int.Parse(s[1]), y = int.Parse(s[0]) };
            }

            long largest = 0L;

            int count = redTiles.Length;

            for (int i = 0; i < count; i++)
            {
                var tile1 = redTiles[i];
                for (int j = i + 1; j < count; j++)
                {
                    var tile2 = redTiles[j];

                    long x = Math.Abs(tile1.x - tile2.x) + 1;
                    long y = Math.Abs(tile1.y - tile2.y) + 1;

                    long ans = x * y;

                    if (ans > largest)
                    {
                        largest = ans;
                    }
                }
            }

            return largest;
        }
    }


}
