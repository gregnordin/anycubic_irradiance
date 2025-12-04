import marimo

__generated_with = "0.18.2"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(10, 10))

    # Grid parameters
    grid_size: int = 5
    shift: float = 0.5
    alpha: float = 0.3

    # Define shifts for each grid copy
    shifts = [
        (0, 0),           # Original
        (shift, 0),       # Shift in +x
        (0, shift),       # Shift in +y
        (shift, shift)    # Shift in both +x and +y
    ]

    colors = ['blue', 'red', 'green', 'orange']

    # Draw each shifted grid
    for (dx, dy), color in zip(shifts, colors):
        # Vertical lines
        for i in range(grid_size + 1):
            x = i + dx
            ax.plot([x, x], [dy, grid_size + dy], color=color, alpha=alpha, linewidth=2)
    
        # Horizontal lines
        for i in range(grid_size + 1):
            y = i + dy
            ax.plot([dx, grid_size + dx], [y, y], color=color, alpha=alpha, linewidth=2)

    # Set axis properties
    ax.set_xlim(-0.5, 6)
    ax.set_ylim(-0.5, 6)
    ax.set_aspect('equal')
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_title('Superimposed 5x5 Grids with Half-Cell Shifts', fontsize=14, fontweight='bold')

    # Add legend
    legend_labels = [
        'Original (0, 0)',
        'Shifted (+0.5, 0)',
        'Shifted (0, +0.5)',
        'Shifted (+0.5, +0.5)'
    ]
    legend_elements = [plt.Line2D([0], [0], color=color, alpha=alpha, linewidth=2, label=label) 
                       for color, label in zip(colors, legend_labels)]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

    ax.grid(False)

    plt.gca()
    return


if __name__ == "__main__":
    app.run()
