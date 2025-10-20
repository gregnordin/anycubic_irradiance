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
    - Convert overlapping rectangular patches into an image and map to grayscale [threshold, 1]
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
    from functools import partial
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
def _(ToggleGrid, mo):
    # Create widgets
    rawimage0 = mo.ui.anywidget(ToggleGrid())
    rawimage1 = mo.ui.anywidget(ToggleGrid())
    rawimage2 = mo.ui.anywidget(ToggleGrid())
    rawimage3 = mo.ui.anywidget(ToggleGrid())

    irradiance_threshold = mo.ui.dropdown(options=[0, 0.3, 0.6, 0.8], label="Irradiance threshold", value=0)
    return rawimage0, rawimage1, rawimage2, rawimage3


@app.cell
def _(
    create_irradiance_pattern,
    mo,
    overlap_image,
    rawimage0,
    rawimage1,
    rawimage2,
    rawimage3,
    xlim,
    ylim,
):
    # plot_fig, plot_ax = create_plot() #irradiance_threshold.value)
    plot_fig, plot_ax = create_irradiance_pattern(overlap_image, xlim, ylim)

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
def _(np):
    def extract_np_array(rawimage_grid, max_value=1):
        return np.array(rawimage_grid[::-1]).astype(float) * max_value
    return (extract_np_array,)


@app.cell
def _(
    create_grid_pattern,
    extract_np_array,
    np,
    rawimage0,
    rawimage1,
    rawimage2,
    rawimage3,
    render_rectangles_direct,
    shift_rectangles,
):
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
    rectangles_unshifted = create_grid_pattern(
        grid_size, square_size, fill_factor_1D, extract_np_array(rawimage0.value["grid"]))

    # Create shifted grids
    shift_amount = 0.5 * square_size
    rectangles_shifted_x = shift_rectangles(
        create_grid_pattern(
            grid_size, 
            square_size, 
            fill_factor_1D, 
            extract_np_array(rawimage3.value["grid"])
        ), 
        shift_x=shift_amount, 
        shift_y=0
    )
    rectangles_shifted_y = shift_rectangles(
        create_grid_pattern(
            grid_size, 
            square_size, 
            fill_factor_1D, 
            extract_np_array(rawimage1.value["grid"])
        ), 
        shift_x=0, 
        shift_y=shift_amount)
    rectangles_shifted_xy = shift_rectangles(
        create_grid_pattern(
            grid_size, 
            square_size, 
            fill_factor_1D, 
            extract_np_array(rawimage2.value["grid"])
        ), 
        shift_x=shift_amount, 
        shift_y=shift_amount
    )

    # print(rectangles_unshifted)

    # Combine all four grids
    all_rectangles = rectangles_unshifted + rectangles_shifted_x + rectangles_shifted_y + rectangles_shifted_xy

    overlap_image = render_rectangles_direct(all_rectangles, img_size, xlim, ylim)

    return overlap_image, xlim, ylim


@app.cell
def _(plt):
    def create_irradiance_pattern(img_data, xlim, ylim):
        fig, ax = plt.subplots() # 2, 3, figsize=(15, 10))
        img = ax.imshow(img_data, cmap='gray', interpolation='nearest', origin='lower', extent=[xlim[0], xlim[1], ylim[0], ylim[1]])
        ax.set_title('All Four Patterns Overlapped')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        return fig, ax
    return (create_irradiance_pattern,)


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
def _(np):
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

    return create_grid_pattern, render_rectangles_direct, shift_rectangles


@app.cell
def _():
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
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
