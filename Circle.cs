using System;

namespace GeometryComponent
{
    /// <summary>
    /// Represents a circle shape.
    /// Input:  radius (double) — the radius of the circle, must be > 0.
    /// Output: Area, Circumference, Diameter (all doubles).
    /// </summary>
    public class Circle
    {
        // Input parameter: radius of the circle.
        // Must be a positive number. Throws ArgumentException if <= 0.
        public double Radius { get; private set; }

        /// <summary>
        /// Creates a Circle.
        /// </summary>
        /// <param name="radius">Radius of the circle. Must be greater than 0.</param>
        /// <exception cref="ArgumentException">Thrown when radius is zero or negative.</exception>
        public Circle(double radius)
        {
            if (radius <= 0)
                throw new ArgumentException(
                    $"radius must be greater than 0. You provided: {radius}. " +
                    "Common mistake: passing diameter instead of radius — try dividing your value by 2.");
            Radius = radius;
        }

        /// <summary>
        /// Makes the circle bigger by increasing the radius.
        /// </summary>
        /// <param name="amount">How much to add to the radius. Must be > 0.</param>
        public void MakeBigger(double amount)
        {
            if (amount <= 0)
                throw new ArgumentException($"amount must be > 0. You provided: {amount}.");
            Radius += amount;
        }

        /// <summary>
        /// Makes the circle smaller by decreasing the radius.
        /// </summary>
        /// <param name="amount">How much to subtract from the radius. Must be > 0 and less than current Radius.</param>
        public void MakeSmaller(double amount)
        {
            if (amount <= 0)
                throw new ArgumentException($"amount must be > 0. You provided: {amount}.");
            if (amount >= Radius)
                throw new ArgumentException(
                    $"amount ({amount}) must be less than current Radius ({Radius}). " +
                    "Reducing by this much would result in a zero or negative radius.");
            Radius -= amount;
        }

        // Algorithm: Area = π * r²
        public double Area => Math.PI * Radius * Radius;

        // Algorithm: Circumference = 2 * π * r
        public double Circumference => 2 * Math.PI * Radius;

        // Algorithm: Diameter = 2 * r
        public double Diameter => 2 * Radius;

        public override string ToString() =>
            $"Circle(Radius={Radius}, Area={Area:F2}, Circumference={Circumference:F2}, Diameter={Diameter:F2})";
    }
}
