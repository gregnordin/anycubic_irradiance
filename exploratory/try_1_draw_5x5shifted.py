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
    return (plt,)


@app.cell
def _():
    import marimo as mo

    grid_selector = mo.ui.multiselect(
        options={
            "original": "Original (0, 0)",
            "shift_x": "Shifted (+0.5, 0)",
            "shift_y": "Shifted (0, +0.5)",
            "shift_both": "Shifted (+0.5, +0.5)"
        },
        value=["original", "shift_x", "shift_y", "shift_both"],
        label="Select grids to display:"
    )

    return grid_selector, mo


@app.cell
def _(grid_selector, mo, plt):
    fig2, ax2 = plt.subplots(figsize=(6, 6))

    # Grid parameters
    grid_size_interactive: int = 5
    shift_interactive: float = 0.5
    alpha_interactive: float = 0.3

    # Define all possible grids
    all_grids = {
        "Original (0, 0)": ((0, 0), 'blue'),
        "Shifted (+0.5, 0)": ((shift_interactive, 0), 'red'),
        "Shifted (0, +0.5)": ((0, shift_interactive), 'green'),
        "Shifted (+0.5, +0.5)": ((shift_interactive, shift_interactive), 'orange')
    }

    # Get selected grids
    selected_grids = grid_selector.value

    # Draw only selected grids
    for grid_key in selected_grids:
        print(grid_key)
        (dx, dy), color = all_grids[grid_key]
    
        # Vertical lines
        for i in range(grid_size_interactive + 1):
            x = i + dx
            ax2.plot([x, x], [dy, grid_size_interactive + dy], 
                    color=color, alpha=alpha_interactive, linewidth=2)
    
        # Horizontal lines
        for i in range(grid_size_interactive + 1):
            y = i + dy
            ax2.plot([dx, grid_size_interactive + dx], [y, y], 
                    color=color, alpha=alpha_interactive, linewidth=2)

    # Set axis properties
    ax2.set_xlim(-0.5, 6)
    ax2.set_ylim(-0.5, 6)
    ax2.set_aspect('equal')
    ax2.set_xlabel('X', fontsize=12)
    ax2.set_ylabel('Y', fontsize=12)
    ax2.set_title('Superimposed 5x5 Grids with Half-Cell Shifts (Interactive)', 
                 fontsize=14, fontweight='bold')

    # Add legend for selected grids
    # if selected_grids:
    #     legend_map = {
    #         "original": "Original (0, 0)",
    #         "shift_x": "Shifted (+0.5, 0)",
    #         "shift_y": "Shifted (0, +0.5)",
    #         "shift_both": "Shifted (+0.5, +0.5)"
    #     }
    
    #     legend_elements = [
    #         plt.Line2D([0], [0], color=all_grids[grid_key][1], 
    #                   alpha=alpha_interactive, linewidth=2, label=legend_map[grid_key])
    #         for grid_key in selected_grids
    #     ]
    #     ax2.legend(handles=legend_elements, loc='upper right', fontsize=10)

    ax2.grid(False)

    mo.vstack([grid_selector, plt.gca()])

    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
