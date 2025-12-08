using System;

namespace Human
{
    public class UnionFind
    {
        private int[] parent;
        private int[] size;
        private int numSets;

        public UnionFind(int n)
        {
            parent = new int[n];
            size = new int[n];
            numSets = n;
            for (int i = 0; i < n; i++)
            {
                parent[i] = i;
                size[i] = 1;
            }
        }

        public int Find(int x)
        {
            if (parent[x] != x)
            {
                parent[x] = Find(parent[x]); 
            }
            return parent[x];
        }

        public bool Union(int x, int y)
        {
            int rootX = Find(x);
            int rootY = Find(y);

            if (rootX == rootY)
                return false; // Already in the same set

            // Union by size
            if (size[rootX] < size[rootY])
            {
                parent[rootX] = rootY;
                size[rootY] += size[rootX];
            }
            else
            {
                parent[rootY] = rootX;
                size[rootX] += size[rootY];
            }

            numSets--;
            return true;
        }

        public int GetNumSets()
        {
            return numSets;
        }

        public List<int> GetCircuitSizes()
        {
            var sizeMap = new Dictionary<int, int>();
            for (int i = 0; i < parent.Length; i++)
            {
                int root = Find(i);
                if (!sizeMap.ContainsKey(root))
                {
                    sizeMap[root] = size[root];
                }
            }
            return sizeMap.Values.ToList();
        }
    }
}
