namespace Human
{
    public static class PuzzleOne
    {

        public static int Solve(string path, int max, int startPosition)
        {
            int position = startPosition;
            int counter = 0;

            foreach (var item in File.ReadLines(path))
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
