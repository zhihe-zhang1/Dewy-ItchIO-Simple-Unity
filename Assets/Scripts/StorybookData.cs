// Positions and destinations are measured from the user's supplied index.html
// at a 430 x 862 CSS-pixel book size, rather than estimated by hand.
public static class StorybookData
{
    public const int PageCount = 6;
    public const float BookWidth = 430f;
    public const float BookHeight = 862f;

    public readonly struct Hotspot
    {
        public readonly int Destination;
        public readonly float X;
        public readonly float Y;
        public readonly float Width;
        public readonly float Height;

        public Hotspot(int destination, float x, float y, float width, float height)
        {
            Destination = destination;
            X = x;
            Y = y;
            Width = width;
            Height = height;
        }
    }

    public static readonly Hotspot[][] Buttons =
    {
        new [] { new Hotspot(1, 19f, 793f, 392f, 50f) },
        new [] { new Hotspot(0, 19f, 793f, 191f, 50f), new Hotspot(2, 220f, 793f, 191f, 50f) },
        new [] { new Hotspot(1, 19f, 793f, 191f, 50f), new Hotspot(3, 220f, 793f, 191f, 50f) },
        new [] { new Hotspot(2, 19f, 793f, 191f, 50f), new Hotspot(4, 220f, 793f, 191f, 50f) },
        new [] { new Hotspot(3, 19f, 793f, 191f, 50f), new Hotspot(5, 220f, 793f, 191f, 50f) },
        new [] { new Hotspot(4, 19f, 793f, 191f, 50f), new Hotspot(0, 220f, 793f, 191f, 50f) },
    };
}
