namespace Human
{
    public class Point3D
    {
        public int X { get; set; }
        public int Y { get; set; }
        public int Z { get; set; }

        public Point3D(int x, int y, int z)
        {
            X = x;
            Y = y;
            Z = z;
        }

        public double DistanceTo(Point3D other)
        {
            long dx = (long)X - other.X;
            long dy = (long)Y - other.Y;
            long dz = (long)Z - other.Z;

            return Math.Sqrt(dx * dx + dy * dy + dz * dz);
        }
    }
}
