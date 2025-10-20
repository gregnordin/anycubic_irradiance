import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import numpy as np
    return np, plt


@app.cell
def _(np, plt):
    def render_rectangles_direct(rectangles, img_size=(500, 500), xlim=(0, 1), ylim=(0, 1)):
        """
        Directly rasterize rectangles to count overlaps without matplotlib rendering.
        """
        overlap_image = np.zeros(img_size)
    
        for x, y, width, height in rectangles:
            # Convert rectangle coordinates to pixel coordinates
            x_start = int((x - xlim[0]) / (xlim[1] - xlim[0]) * img_size[1])
            x_end = int((x + width - xlim[0]) / (xlim[1] - xlim[0]) * img_size[1])
            y_start = int((y - ylim[0]) / (ylim[1] - ylim[0]) * img_size[0])
            y_end = int((y + height - ylim[0]) / (ylim[1] - ylim[0]) * img_size[0])
        
            # Clamp to image boundaries
            x_start = max(0, min(x_start, img_size[1]))
            x_end = max(0, min(x_end, img_size[1]))
            y_start = max(0, min(y_start, img_size[0]))
            y_end = max(0, min(y_end, img_size[0]))
        
            # Add 1 to the overlap count in this rectangle region
            # Note: y-axis is typically inverted in images
            overlap_image[img_size[0] - y_end:img_size[0] - y_start, x_start:x_end] += 1
    
        return overlap_image

    # Example usage
    rectangles = [
        (0.2, 0.2, 0.4, 0.3),
        (0.3, 0.3, 0.4, 0.3),
        (0.5, 0.4, 0.3, 0.4),
        (0.4, 0.5, 0.3, 0.3),
    ]

    overlap_image = render_rectangles_direct(rectangles)

    plt.figure(figsize=(8, 6))
    plt.imshow(overlap_image, cmap='gray', interpolation='nearest', origin='lower')
    plt.colorbar(label='Number of Overlapping Rectangles')
    plt.title('Rectangle Overlap Count')
    plt.show()

    print(f"Maximum overlap: {overlap_image.max():.0f} rectangles")
    print(f"Unique values: {np.unique(overlap_image)}")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
