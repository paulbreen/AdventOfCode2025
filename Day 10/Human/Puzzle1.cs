using System.Text.RegularExpressions;

namespace Human
{
    public static class Puzzle1
    {
        public static Int64 Solve(string[] fileInput)
        {
            var totalPresses = 0;

            foreach (var line in fileInput)
            {
                var minPresses = SolveMachine(line);
                totalPresses += minPresses;
            }

            return totalPresses;
        }

        private static int SolveMachine(string line)
        {
            // Parse target state
            var bracketMatch = Regex.Match(line, @"\[([.#]+)\]");
            var targetStr = bracketMatch.Groups[1].Value;
            var target = new bool[targetStr.Length];

            for (int i = 0; i < targetStr.Length; i++)
            {
                target[i] = targetStr[i] == '#';
            }

            // Parse buttons
            var buttonMatches = Regex.Matches(line, @"\(([0-9,]+)\)");
            var buttons = new List<List<int>>();

            foreach (Match match in buttonMatches)
            {
                var buttonStr = match.Groups[1].Value;
                var button = new List<int>();
                var parts = buttonStr.Split(',');

                for (int i = 0; i < parts.Length; i++)
                {
                    button.Add(int.Parse(parts[i]));
                }

                buttons.Add(button);
            }

            // Try all combinations of button presses
            var numButtons = buttons.Count;
            var totalCombinations = 1 << numButtons; 
            var minPresses = int.MaxValue;

            for (int combo = 0; combo < totalCombinations; combo++)
            {      
                var state = new bool[target.Length];

                var presses = 0;
                for (int b = 0; b < numButtons; b++)
                {
                    if ((combo & (1 << b)) != 0) // if bit b is set
                    {
                        presses++;

                        for (int i = 0; i < buttons[b].Count; i++)
                        {
                            var lightIndex = buttons[b][i];
                            state[lightIndex] = !state[lightIndex];
                        }
                    }
                }

                var matches = true;
                for (int i = 0; i < target.Length; i++)
                {
                    if (state[i] != target[i])
                    {
                        matches = false;
                        break;
                    }
                }

                if (matches && presses < minPresses)
                {
                    minPresses = presses;
                }
            }

            return minPresses;
        }
    }
}