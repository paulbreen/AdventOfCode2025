
namespace Human
{
    public static class Puzzle1
    {
        public static Int64 Solve(string[] fileInput)
        {
            var total = 0;

            var tachyon = new char[fileInput.Length][];

            for (int i = 0; i < fileInput.Length; i++)
            {
                tachyon[i] = fileInput[i].ToArray();
            }

            var startPosition = fileInput[0].IndexOf('S');

            for (int i = 0; i < tachyon.Length; i++)
            {
                if(i == 1)
                {
                    tachyon[i][startPosition] = '|';
                }


                for (var j = 0; j < tachyon[i].Length; j++)
                {
                    if (i == 0) break;

                    //check position directly above
                    if (tachyon[i - 1][j] == '|'){

                        //if we are a splitter, then split
                        if (tachyon[i][j] == '^')
                        {
                            tachyon[i][j - 1] = '|';
                            tachyon[i][j + 1] = '|';
                            total++;
                        }
                        else
                        {
                            //change to beam
                            tachyon[i][j] = '|';
                        }
                    }
                }

                //Print(tachyon);
            }

            return total;
        }


        private static void Print(char[][] tachyon)
        {
            Console.SetCursorPosition(0, 0);
            for (int i = 0; i < tachyon.Length; i++)
            {
                for (var j = 0; j < tachyon[i].Length; j++)
                {
                    Console.Write(tachyon[i][j]);

                    Thread.Sleep(1);
                }
                Console.WriteLine();
            }

            Console.WriteLine();
        }
    }
}
