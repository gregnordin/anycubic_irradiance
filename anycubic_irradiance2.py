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
    def create_grid_pattern(grid_size=5, square_size=1.0, fill_factor=1.0, pattern=None):
        """
        Create a list of rectangles based on a 5x5 grid pattern.
    
        Parameters:
        - grid_size: size of the grid (5 for 5x5)
        - square_size: size of each grid cell (spacing between squares)
        - fill_factor: 1D fraction of the grid cell that is filled (0 to 1)
        - pattern: 2D array of 0s and 1s indicating which squares are active
    
        Returns:
        - List of rectangle tuples (x, y, width, height)
        """
        if pattern is None:
            # Default pattern - checkerboard
            pattern = np.zeros((grid_size, grid_size))
            pattern[::2, ::2] = 1
            pattern[1::2, 1::2] = 1
    
        rectangles = []
        actual_square_size = square_size * fill_factor
        offset = (square_size - actual_square_size) / 2  # Center the square in the grid cell
    
        for i in range(grid_size):
            for j in range(grid_size):
                if pattern[i, j] == 1:
                    x = j * square_size + offset
                    y = i * square_size + offset
                    rectangles.append((x, y, actual_square_size, actual_square_size))
    
        return rectangles

    def shift_rectangles(rectangles, shift_x=0, shift_y=0):
        """
        Shift all rectangles by given amounts.
        """
        return [(x + shift_x, y + shift_y, w, h) for x, y, w, h in rectangles]

    def render_rectangles_direct(rectangles, img_size=(500, 500), xlim=(0, 5), ylim=(0, 5)):
        """
        Directly rasterize rectangles to count overlaps.
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
            overlap_image[y_start:y_end, x_start:x_end] += 1
    
        return overlap_image

    # Define your pattern (5x5 grid, 1 = square present, 0 = empty)
    pattern = np.array([
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1]
    ])

    # Parameters
    grid_size = 5
    square_size = 1.0  # Grid spacing
    fill_factor_2D = 0.68  # 68% 2D fill factor
    fill_factor_1D = np.sqrt(fill_factor_2D)  # 1D fill factor
    pixels_per_square = 50  # Number of pixels per grid square

    # Calculate image size based on pixels per square
    xlim = (0, grid_size * square_size + 0.5 * square_size)
    ylim = (0, grid_size * square_size + 0.5 * square_size)
    img_width = int((xlim[1] - xlim[0]) * pixels_per_square)
    img_height = int((ylim[1] - ylim[0]) * pixels_per_square)
    img_size = (img_height, img_width)

    # Create the base grid with fill factor
    rectangles_base = create_grid_pattern(grid_size, square_size, fill_factor_1D, pattern)

    # Create shifted grids
    shift_amount = 0.5 * square_size
    rectangles_shifted_x = shift_rectangles(rectangles_base, shift_x=shift_amount, shift_y=0)
    rectangles_shifted_y = shift_rectangles(rectangles_base, shift_x=0, shift_y=shift_amount)
    rectangles_shifted_xy = shift_rectangles(rectangles_base, shift_x=shift_amount, shift_y=shift_amount)

    # Combine all four grids
    all_rectangles = rectangles_base + rectangles_shifted_x + rectangles_shifted_y + rectangles_shifted_xy

    overlap_image = render_rectangles_direct(all_rectangles, img_size, xlim, ylim)

    # Visualize
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # Original pattern
    img1 = render_rectangles_direct(rectangles_base, img_size, xlim, ylim)
    axes[0, 0].imshow(img1, cmap='gray', interpolation='nearest', origin='lower', extent=[xlim[0], xlim[1], ylim[0], ylim[1]])
    axes[0, 0].set_title(f'Original Grid (fill={fill_factor_2D*100:.0f}%)')
    axes[0, 0].set_xlabel('x')
    axes[0, 0].set_ylabel('y')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].set_aspect('equal')

    # Shifted pattern (x direction)
    img2 = render_rectangles_direct(rectangles_shifted_x, img_size, xlim, ylim)
    axes[0, 1].imshow(img2, cmap='gray', interpolation='nearest', origin='lower', extent=[xlim[0], xlim[1], ylim[0], ylim[1]])
    axes[0, 1].set_title('Shifted Grid (0.5 squares in +x)')
    axes[0, 1].set_xlabel('x')
    axes[0, 1].set_ylabel('y')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].set_aspect('equal')

    # Shifted pattern (y direction)
    img3 = render_rectangles_direct(rectangles_shifted_y, img_size, xlim, ylim)
    axes[0, 2].imshow(img3, cmap='gray', interpolation='nearest', origin='lower', extent=[xlim[0], xlim[1], ylim[0], ylim[1]])
    axes[0, 2].set_title('Shifted Grid (0.5 squares in +y)')
    axes[0, 2].set_xlabel('x')
    axes[0, 2].set_ylabel('y')
    axes[0, 2].grid(True, alpha=0.3)
    axes[0, 2].set_aspect('equal')

    # Shifted pattern (x and y direction)
    img4 = render_rectangles_direct(rectangles_shifted_xy, img_size, xlim, ylim)
    axes[1, 0].imshow(img4, cmap='gray', interpolation='nearest', origin='lower', extent=[xlim[0], xlim[1], ylim[0], ylim[1]])
    axes[1, 0].set_title('Shifted Grid (0.5 squares in +x and +y)')
    axes[1, 0].set_xlabel('x')
    axes[1, 0].set_ylabel('y')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].set_aspect('equal')

    # Overlap: all patterns combined (excluding diagonal shift)
    img_overlap_3 = render_rectangles_direct(rectangles_base + rectangles_shifted_x + rectangles_shifted_y, 
                                             img_size, xlim, ylim)
    im1 = axes[1, 1].imshow(img_overlap_3, cmap='gray', interpolation='nearest', origin='lower', extent=[xlim[0], xlim[1], ylim[0], ylim[1]])
    axes[1, 1].set_title('Original + X-Shifted + Y-Shifted')
    axes[1, 1].set_xlabel('x')
    axes[1, 1].set_ylabel('y')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].set_aspect('equal')
    plt.colorbar(im1, ax=axes[1, 1], label='Overlap Count')

    # Overlap result (all four)
    im2 = axes[1, 2].imshow(overlap_image, cmap='gray', interpolation='nearest', origin='lower', extent=[xlim[0], xlim[1], ylim[0], ylim[1]])
    axes[1, 2].set_title('All Four Patterns Overlapped')
    axes[1, 2].set_xlabel('x')
    axes[1, 2].set_ylabel('y')
    axes[1, 2].grid(True, alpha=0.3)
    axes[1, 2].set_aspect('equal')
    plt.colorbar(im2, ax=axes[1, 2], label='Overlap Count')

    plt.tight_layout()
    plt.show()

    print(f"Maximum overlap: {overlap_image.max():.0f} squares")
    print(f"Unique overlap values: {np.unique(overlap_image)}")
    print(f"Number of active squares in pattern: {np.sum(pattern)}")
    print(f"Grid spacing: {square_size}, Actual square size: {square_size * fill_factor_1D:.3f}")
    print(f"2D fill factor: {fill_factor_2D*100:.0f}%")
    print(f"Pixels per grid square: {pixels_per_square}")
    print(f"Image size: {img_size} ({img_width} x {img_height} pixels)")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
