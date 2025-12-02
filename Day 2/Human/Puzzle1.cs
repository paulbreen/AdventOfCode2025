namespace Human
{
    public static class Puzzle1
    {

        public static Int64 Solve(string fileInput)
        {
            var list = fileInput.Split(',');

            Int64 total = 0;

            foreach (var item in list)
            {
                var range = item.Split("-");

                var startingRange = Int64.Parse(range[0]);
                var endingRange = Int64.Parse(range[1]);

                for (Int64 i = startingRange; i <= endingRange; i++)
                {
                    if (!Validate(i))
                    {
                        total += i;
                    }
                }
            }

            return total;
        }


        private static bool Validate(Int64 id)
        {
            var stringId = id.ToString();

            // rule 1, has odd number of digits
            if ((stringId.Length % 2) == 1) return true;


            //rule 2, repeated twice
            var halfLength = (stringId.Length / 2);
            var firstHalf = stringId.Substring(0, halfLength);
            var secondHalf = stringId.Substring(halfLength);

            if (firstHalf == secondHalf) return false;

            return true;
        }
    }
}
