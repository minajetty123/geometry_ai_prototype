using System;

namespace GeometryComponent
{
    /// <summary>
    /// Represents a rectangle shape.
    /// Input:  width (double) and height (double), both must be > 0.
    /// Output: Area, Perimeter, Diagonal (all doubles).
    /// </summary>
    public class Rectangle
    {
        // Input parameters: width and height of the rectangle.
        // Both must be positive numbers. Throws ArgumentException otherwise.
        public double Width  { get; private set; }
        public double Height { get; private set; }

        /// <summary>
        /// Creates a Rectangle.
        /// </summary>
        /// <param name="width">Width of the rectangle. Must be greater than 0.</param>
        /// <param name="height">Height of the rectangle. Must be greater than 0.</param>
        /// <exception cref="ArgumentException">Thrown when width or height is zero or negative.</exception>
        public Rectangle(double width, double height)
        {
            if (width <= 0)
                throw new ArgumentException(
                    $"width must be greater than 0. You provided: {width}.");
            if (height <= 0)
                throw new ArgumentException(
                    $"height must be greater than 0. You provided: {height}.");
            Width  = width;
            Height = height;
        }

        /// <summary>
        /// Scales the rectangle uniformly (makes it bigger or smaller).
        /// </summary>
        /// <param name="factor">Scale factor. Greater than 1 = bigger, between 0 and 1 = smaller. Must be > 0.</param>
        public void Scale(double factor)
        {
            if (factor <= 0)
                throw new ArgumentException(
                    $"factor must be > 0. You provided: {factor}. " +
                    "To make smaller use a value between 0 and 1 (e.g. 0.5 halves the size). " +
                    "To make bigger use a value > 1 (e.g. 2.0 doubles the size).");
            Width  *= factor;
            Height *= factor;
        }

        // Algorithm: Area = width * height
        public double Area => Width * Height;

        // Algorithm: Perimeter = 2 * (width + height)
        public double Perimeter => 2 * (Width + Height);

        // Algorithm: Diagonal = sqrt(width² + height²)  (Pythagorean theorem)
        public double Diagonal => Math.Sqrt(Width * Width + Height * Height);

        public override string ToString() =>
            $"Rectangle(Width={Width}, Height={Height}, Area={Area:F2}, Perimeter={Perimeter:F2}, Diagonal={Diagonal:F2})";
    }
}
