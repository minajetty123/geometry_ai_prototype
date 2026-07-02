using System;

namespace GeometryComponent
{
    /// <summary>
    /// Represents a square shape.
    /// Input:  sideLength (double) — the length of one side, must be > 0.
    /// Output: Area, Perimeter, Diagonal (all doubles).
    /// </summary>
    public class Square
    {
        // Input parameter: side length of the square.
        // Must be a positive number. Throws ArgumentException if <= 0.
        public double SideLength { get; private set; }

        /// <summary>
        /// Creates a Square.
        /// </summary>
        /// <param name="sideLength">Length of one side. Must be greater than 0.</param>
        /// <exception cref="ArgumentException">Thrown when sideLength is zero or negative.</exception>
        public Square(double sideLength)
        {
            if (sideLength <= 0)
                throw new ArgumentException(
                    $"sideLength must be greater than 0. You provided: {sideLength}. " +
                    "Common mistake: passing 0 or a negative number.");
            SideLength = sideLength;
        }

        /// <summary>
        /// Makes the square bigger by increasing the side length.
        /// </summary>
        /// <param name="amount">How much to add to the side length. Must be > 0.</param>
        public void MakeBigger(double amount)
        {
            if (amount <= 0)
                throw new ArgumentException($"amount must be > 0. You provided: {amount}.");
            SideLength += amount;
        }

        /// <summary>
        /// Makes the square smaller by decreasing the side length.
        /// </summary>
        /// <param name="amount">How much to subtract from the side length. Must be > 0 and less than current SideLength.</param>
        public void MakeSmaller(double amount)
        {
            if (amount <= 0)
                throw new ArgumentException($"amount must be > 0. You provided: {amount}.");
            if (amount >= SideLength)
                throw new ArgumentException(
                    $"amount ({amount}) must be less than current SideLength ({SideLength}). " +
                    "Reducing by this much would result in a zero or negative side length.");
            SideLength -= amount;
        }

        // Algorithm: Area = side * side
        public double Area => SideLength * SideLength;

        // Algorithm: Perimeter = 4 * side
        public double Perimeter => 4 * SideLength;

        // Algorithm: Diagonal = side * sqrt(2)  (Pythagorean theorem on a right triangle inside the square)
        public double Diagonal => SideLength * Math.Sqrt(2);

        public override string ToString() =>
            $"Square(SideLength={SideLength}, Area={Area:F2}, Perimeter={Perimeter:F2}, Diagonal={Diagonal:F2})";
    }
}
