namespace Human
{
    public static class PuzzleOne
    {

        public static int Solve(int max, int startPosition, string[] rotations)
        {
            int position = startPosition;
            int counter = 0;

            foreach (var item in rotations)
            {
                var direction = item.ToLower().First();
                var steps = int.Parse(item[1..]);

                if (direction == 'l')
                {
                    position = (position - steps) % (max + 1);

                    if (position < 0)
                        position += (max + 1);
                }

                if (direction == 'r')
                {
                    position = (position + steps) % (max + 1);
                }

                if (position == 0) counter++;
            }

            return counter;
        }
    }
}
