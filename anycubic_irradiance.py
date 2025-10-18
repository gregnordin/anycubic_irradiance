# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///

import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    import numpy as np
    return Rectangle, mo, np, plt


@app.cell
def _():
    # # Matrix settings
    # n = 10  # Size of the matrix (n x n)

    # # Create n x n matrix of ones, multiply by 0.5
    # matrix = np.ones((n, n)) * 0.5

    # # Set center element to 0
    # center = n // 2
    # matrix[center, center] = 0

    # # Create a figure and axis
    # fig, ax = plt.subplots()

    # # Set the background color to black
    # fig.patch.set_facecolor('black')
    # ax.set_facecolor('black')

    # # Square size settings
    # full_size = 1.0  # Full cell size in matrix coordinates
    # square_size = full_size * 0.8  # 80% reduction (20% of original size)
    # offset = (full_size - square_size) / 2  # Offset to center the square

    # # Draw individual squares for each matrix element
    # for i in range(n):
    #     for j in range(n):
    #         # Convert matrix value (0 to 0.5) to grayscale (0 to 1 for Matplotlib)
    #         gray_value = matrix[i, j]
    #         # Calculate bottom-left corner of the square to center it
    #         x = j + offset
    #         y = n - 1 - i + offset  # Flip y-axis to match matrix indexing
    #         # Create a square (Rectangle) with the grayscale color
    #         square = Rectangle((x, y), square_size, square_size, 
    #                           facecolor=(gray_value, gray_value, gray_value))
    #         ax.add_patch(square)

    # # Set axis limits to show the entire grid
    # ax.set_xlim(0, n)
    # ax.set_ylim(0, n)

    # # Remove axis ticks and labels
    # ax.set_xticks([])
    # ax.set_yticks([])

    # # Ensure the plot is square
    # ax.set_aspect('equal')

    # # Show the plot
    # plt.show()
    return


@app.cell
def _(Rectangle):
    def add_squares_to_plot(ax, n_size, matrix, shift_x, shift_y, _square_offset, _square_size):
        for i in range(n_size):
            for j in range(n_size):
                # Use matrix value as both grayscale and alpha for blending
                gray_value = matrix[i, j]
                # Calculate bottom-left corner of the square to center it
                x = j + _square_offset + shift_x
                y = n_size - 1 - i + _square_offset + shift_y  # Flip y-axis to match matrix indexing
                # Create a square (Rectangle) with white color and alpha blending
                square = Rectangle((x, y), _square_size, _square_size, 
                                  facecolor=(1, 1, 1), alpha=gray_value)
                ax.add_patch(square)

    return (add_squares_to_plot,)


@app.cell
def _(add_squares_to_plot, n_on, n_size, np, plt):
    # Matrix settings
    # n = 5  # Size of the matrix (n x n)

    center = n_size.value // 2
    matrix = np.zeros((n_size.value, n_size.value))

    # Single 102 um pixel in center
    # matrix[center, center] = 1

    # 2x2 102 um pixels in center
    if n_on.value == 1:
        matrix[center, center] = 1
    if (n_on.value % 2) != 0:
        matrix[center-(n_on.value - 1):center, center-(n_on.value):center] = 1
    else:
        matrix[center-(n_on.value):center, center-(n_on.value):center] = 1
    
    # Set matrix element values
    matrix *= 0.25

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Set the background color to black
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Square size settings
    full_size = 1.0  # Full cell size in matrix coordinates
    square_size = full_size * 0.825  # 20% reduction (80% of original size)
    offset = (full_size - square_size) / 2  # Offset to center the square

    # Draw individual squares for the original positions
    add_squares_to_plot(
        ax, 
        n_size=n_size.value, 
        matrix=matrix, 
        shift_x=0, 
        shift_y=0, 
        _square_offset=offset, 
        _square_size=square_size
    )

    # Draw individual squares for the shifted positions (y + 0.5)
    add_squares_to_plot(
        ax, 
        n_size=n_size.value, 
        matrix=matrix, 
        shift_x=0, 
        shift_y=0.5, 
        _square_offset=offset, 
        _square_size=square_size
    )

    # Draw individual squares for the shifted positions (x + 0.5)
    add_squares_to_plot(
        ax, 
        n_size=n_size.value, 
        matrix=matrix, 
        shift_x=0.5, 
        shift_y=0, 
        _square_offset=offset, 
        _square_size=square_size
    )

    # Draw individual squares for the shifted positions (x+0.5, y+0.5)
    add_squares_to_plot(
        ax, 
        n_size=n_size.value, 
        matrix=matrix, 
        shift_x=0.5, 
        shift_y=0.5, 
        _square_offset=offset, 
        _square_size=square_size
    )

    # Add red vertical and horizontal lines at integer + 0.5 positions
    line_positions = np.arange(0, n_size.value + 2, 0.5)  # Positions: 0.0, 0.5, 1.0, 1.5, ...
    ax.vlines(line_positions, ymin=0, ymax=n_size.value + 0.5, colors='red', linewidth=1)
    ax.hlines(line_positions, xmin=0, xmax=n_size.value, colors='red', linewidth=1)

    eps = 0.02
    # Set axis limits to show the entire grid
    ax.set_xlim(0 - eps, n_size.value + eps)
    ax.set_ylim(0 - eps, n_size.value + eps)

    # Remove axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])

    # Ensure the plot is square
    ax.set_aspect('equal')

    # Show the plot
    plt.show()
    return line_positions, matrix


@app.cell
def _(mo):
    n_size_min = 3
    n_size_max = 15
    n_size = mo.ui.slider(n_size_min, n_size_max, value=9)
    n_size
    return (n_size,)


@app.cell
def _(mo, n_size):
    n_on_min = 1
    n_on_max = n_size.value - 1
    n_on = mo.ui.slider(n_on_min, n_on_max, value=n_on_min)
    n_on
    return (n_on,)


@app.cell
def _(n_on, n_size):
    n_size.value, n_on.value
    return


@app.cell
def _(matrix):
    matrix
    return


@app.cell
def _(line_positions):
    line_positions
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
