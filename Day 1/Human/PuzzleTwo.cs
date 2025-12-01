namespace Human
{
    public static class PuzzleTwo
    {
        public static int Solve(int max, int startPosition, string[] rotations)
        {
            var position = startPosition;
            var counter = 0;

            foreach (var item in rotations)
            {
                var direction = item.ToLower().First();
                var steps = int.Parse(item[1..]);

                if (direction == 'l')
                {
                    if (position == 0)
                    {
                        counter += steps / (max + 1);
                    }
                    else if (steps >= position)
                    {
                        counter += (1 + (steps - position) / (max + 1));
                    }

                    position = (position - steps) % (max + 1);

                    if (position < 0)
                    {
                        position += (max + 1);
                    }
                }
                else if (direction == 'r')
                {
                    var newPosition = (position + steps);

                    counter += (newPosition) / (max + 1);
                    position = +newPosition % (max + 1);
                }
            }

            return counter;
        }
    }
}