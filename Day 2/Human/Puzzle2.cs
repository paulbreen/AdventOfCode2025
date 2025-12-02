using System.Data;

namespace Human
{
    public static class Puzzle2
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
            var halfLength = (stringId.Length / 2);

            // rule 
            // ID is invalid if it is made only of some sequence of digits repeated at least twice
            for (int i = 1; i <= halfLength; i++)
            {
                // split string into increasing length of chunks
                var chunk = stringId.Chunk(i).Select (x => new string(x)).ToList();

                // group the chunks
                var groupChunk = chunk.GroupBy(x => x);
                
                //if there is more than one group, we know there is more than one sequence.
                if(groupChunk.Count() == 1) return false;
            }

            return true;
        }
    }
}