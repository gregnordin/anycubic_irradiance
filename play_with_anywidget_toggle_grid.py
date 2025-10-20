import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
    # Current state
    - Single grid works with `widget.get_grid_state()` returning the 2D grid array which accurately contains clicked grid tiles
    - Position grid inside a marimo container
    - Make 4 grids and layout as 2x2 in marimo containers
    - Convert `widget.grid` into a numpy boolean array, then into a numpy float array in range [0,1] and multiply by 0.25
    - Plot data from 4 grids in matplotlib map of irradiance and show underneath 2x2 toggle grids array

    # Next steps
    - make grid size a variable, n_size, and pass it into `ToggleGrid.__init__()`?
    - Input to set threshold value for irradiance map
    - Make ToggleGrid smaller in the UI
    - Make output plot smaller in UI
    - Add float input widget to set micromirror array fill factor
    - Put `mo.ui.anywidget` wrapper in a function to make it easy to create fully reactive `ToggleGrid` widget
    - Save state to file?
    - Load state from file?
    - How make image of UI and irradiance map?

    """
    )
    return


@app.cell
def _():
    import marimo as mo
    import anywidget
    import traitlets
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    return Rectangle, anywidget, mo, np, plt, traitlets


@app.cell
def _(anywidget, traitlets):
    class ToggleGrid(anywidget.AnyWidget):
        _esm = """
        function render({ model, el }) {
          const size = 5;
          const squareSize = 50;
      
          // Initialize grid state from model or create new
          let grid = model.get("grid");
          if (!grid || grid.length === 0) {
            grid = Array(size).fill().map(() => Array(size).fill(false));
            model.set("grid", grid);
            model.save_changes();
          }
      
          // Create container
          const container = document.createElement("div");
          container.style.display = "inline-block";
          container.style.border = "2px solid #333";
      
          // Create grid
          const gridEl = document.createElement("div");
          gridEl.style.display = "grid";
          gridEl.style.gridTemplateColumns = `repeat(${size}, ${squareSize}px)`;
          gridEl.style.gap = "0";
      
          // Create squares
          const squares = [];
          for (let i = 0; i < size; i++) {
            squares[i] = [];
            for (let j = 0; j < size; j++) {
              const square = document.createElement("div");
              square.style.width = `${squareSize}px`;
              square.style.height = `${squareSize}px`;
              square.style.border = "1px solid #666";
              square.style.cursor = "pointer";
              square.style.backgroundColor = grid[i][j] ? "white" : "black";
          
              square.addEventListener("click", () => {
                grid[i][j] = !grid[i][j];
                square.style.backgroundColor = grid[i][j] ? "white" : "black";
                // Create a new array to trigger change detection
                const newGrid = grid.map(row => [...row]);
                model.set("grid", newGrid);
                model.set("version", model.get("version") + 1);
                model.save_changes();
                grid = newGrid;
              });
          
              squares[i][j] = square;
              gridEl.appendChild(square);
            }
          }
      
          // Listen for model changes
          model.on("change:grid", () => {
            const newGrid = model.get("grid");
            for (let i = 0; i < size; i++) {
              for (let j = 0; j < size; j++) {
                squares[i][j].style.backgroundColor = newGrid[i][j] ? "white" : "black";
              }
            }
          });
      
          container.appendChild(gridEl);
          el.appendChild(container);
        }
        export default { render };
        """
    
        grid = traitlets.List([]).tag(sync=True)
        version = traitlets.Int(0).tag(sync=True)
    
        def __init__(self):
            # Initialize with 5x5 grid of False (black)
            self.grid = [[False for _ in range(5)] for _ in range(5)]
            super().__init__()
    
        def get_grid_state(self):
            """Return the current state of the grid"""
            return self.grid
    
        def reset(self):
            """Reset all squares to black (False)"""
            self.grid = [[False for _ in range(5)] for _ in range(5)]
            self.version += 1

    return (ToggleGrid,)


@app.cell
def _(np):
    def extract_np_array(rawimage_grid, max_value=0.25):
        return np.array(rawimage_grid).astype(float) * max_value
    return (extract_np_array,)


@app.cell
def _(ToggleGrid, mo):
    # Create widgets
    rawimage0 = mo.ui.anywidget(ToggleGrid())
    rawimage1 = mo.ui.anywidget(ToggleGrid())
    rawimage2 = mo.ui.anywidget(ToggleGrid())
    rawimage3 = mo.ui.anywidget(ToggleGrid())

    irradiance_threshold = mo.ui.dropdown(options=[0, 0.3, 0.6, 0.8], label="Irradiance threshold", value=0)
    return rawimage0, rawimage1, rawimage2, rawimage3


@app.cell
def _(create_plot, mo, rawimage0, rawimage1, rawimage2, rawimage3):
    plot_fig, plot_ax = create_plot() #irradiance_threshold.value)

    # Display it
    mo.vstack([
        mo.hstack([rawimage1, rawimage2], justify="start"),
        mo.hstack([rawimage0, rawimage3], justify="start"),
        mo.hstack([plot_ax]) #, irradiance_threshold], justify="start")
    ])

    return


@app.cell
def _():
    # rawimage0.value["grid"]
    return


@app.cell
def _():
    # extract_np_array(rawimage0.value["grid"])
    return


@app.cell
def _():
    # extract_np_array(rawimage3.value["grid"])
    return


@app.cell
def _(
    Rectangle,
    extract_np_array,
    np,
    plt,
    rawimage0,
    rawimage1,
    rawimage2,
    rawimage3,
):
    def add_squares_to_plot(ax, n_size, matrix, shift_x, shift_y, _square_offset, _square_size):
        for i in range(n_size):
            for j in range(n_size):
                # Use matrix value as both grayscale and alpha for blending
                gray_value = matrix[i, j] # * 2
                # Calculate bottom-left corner of the square to center it
                x = j + _square_offset + shift_x
                y = n_size - 1 - i + _square_offset + shift_y  # Flip y-axis to match matrix indexing
                # Create a square (Rectangle) with white color and alpha blending
                square = Rectangle((x, y), _square_size, _square_size, 
                                  facecolor=(1, 1, 1), alpha=gray_value)
                ax.add_patch(square)

    def create_plot(
        # threshold=0,
        n_size=5, 
        image0=rawimage0, 
        image1=rawimage1, 
        image2=rawimage2, 
        image3=rawimage3):
        
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
            n_size=n_size, 
            matrix=extract_np_array(image0.value["grid"]), 
            shift_x=0, 
            shift_y=0, 
            _square_offset=offset, 
            _square_size=square_size
        )
    
        # Draw individual squares for the shifted positions (y + 0.5)
        add_squares_to_plot(
            ax, 
            n_size=n_size, 
            matrix=extract_np_array(image1.value["grid"]), 
            shift_x=0, 
            shift_y=0.5, 
            _square_offset=offset, 
            _square_size=square_size
        )
    
        # Draw individual squares for the shifted positions (x + 0.5)
        add_squares_to_plot(
            ax, 
            n_size=n_size, 
            matrix=extract_np_array(image3.value["grid"]), 
            shift_x=0.5, 
            shift_y=0, 
            _square_offset=offset, 
            _square_size=square_size
        )
    
        # Draw individual squares for the shifted positions (x+0.5, y+0.5)
        add_squares_to_plot(
            ax, 
            n_size=n_size, 
            matrix=extract_np_array(image2.value["grid"]), 
            shift_x=0.5, 
            shift_y=0.5, 
            _square_offset=offset, 
            _square_size=square_size
        )
    
        # Add red vertical and horizontal lines at integer + 0.5 positions
        line_positions = np.arange(0, n_size + 2, 0.5)  # Positions: 0.0, 0.5, 1.0, 1.5, ...
        ax.vlines(line_positions, ymin=0, ymax=n_size + 0.5, colors='red', linewidth=1)
        ax.hlines(line_positions, xmin=0, xmax=n_size, colors='red', linewidth=1)
    
        eps = 0.02
        # Set axis limits to show the entire grid
        ax.set_xlim(0 - eps, n_size + eps)
        ax.set_ylim(0 - eps, n_size + eps)
    
        # Remove axis ticks and labels
        ax.set_xticks([])
        ax.set_yticks([])
    
        # Ensure the plot is square
        ax.set_aspect('equal')
    
        # Return figure and axes objects
        return fig, ax
    return (create_plot,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
