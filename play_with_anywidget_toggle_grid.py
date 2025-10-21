import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Calculate Irradiance for TI XPR Projector

    ### Basic Idea

    See [Understanding the XPR Technology](https://awolvision.com/blogs/awol-vision-blog/understanding-xpr-technology-for-4k-dlp-projectors) and the image below for an explanation of how XPR works. In summary, the technique is intended to double the apparent resolution of a projected image compared to the actual physical resolution of the projected micromirror array. For example, our Anycubic DLP 3D printer projects an image with a 102 &mu;m pixel pitch. However, the claimed resolution is 51 &mu;m, which is achieved by rapidly projecting four sequential 102 &mu;m pixel images to construct each 51 &mu;m image. As shown in the right panel of the image below. The four-image sequence is

    1. Unshifted image
    2. Shifted up by 1/2 pixel (i.e., 1/2 of a 102 &mu;m pixel)
    3. Shifted up and right by 1/2 pixel
    4. Shifted right by 1/2 pixel
    """
    )
    return


@app.cell
def _(mo):
    mo.image(src="xpr_visual.jpg")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ### Visualization

    Below are four 5x5 arrays of 102 &mu;m pixels, one for each of the XPR shifts, and the output image created by their temporal overlap.
    """
    )
    return


@app.cell
def _(
    fill_factor_2D,
    irradiance_threshold,
    mo,
    overlap_image,
    plot_irradiance_pattern,
    rawimage0,
    rawimage1,
    rawimage2,
    rawimage3,
    set_all_to_black,
    set_all_to_white,
    xlim,
    ylim,
):
    # plot_fig, plot_ax = create_plot() #irradiance_threshold.value)
    plot_fig, plot_ax = plot_irradiance_pattern(overlap_image, xlim, ylim, irradiance_threshold.value)

    # Display it
    mo.vstack([
        mo.md("### Individual 102 &mu;m Pixel Images"),
        mo.md("Shift +y" + "&nbsp;"*38 +"Shift +xy"),
        mo.hstack([rawimage1, rawimage2], justify="start"),
        mo.md("Unshifted" + "&nbsp;"*37 +"Shift +x"),
        mo.hstack([rawimage0, rawimage3], justify="start"),
        mo.hstack([plot_ax, 
                   mo.vstack(
                       [
                           set_all_to_black, 
                           set_all_to_white, 
                           fill_factor_2D,
                           irradiance_threshold, 
                       ], 
                       justify="center")], justify="start")
    ])
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
    return anywidget, mo, np, plt, traitlets


@app.cell
def _(anywidget, traitlets):
    class ToggleGrid(anywidget.AnyWidget):
        _esm = """
        function render({ model, el }) {
          const size = 5;
          const squareSize = 40;

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
                model.save_changes();
                grid = newGrid;
              });

              squares[i][j] = square;
              gridEl.appendChild(square);
            }
          }

          // Listen for reset_trigger changes
          model.on("change:reset_trigger", () => {
            // Reset the grid
            grid = Array(size).fill().map(() => Array(size).fill(false));
            model.set("grid", grid);
            model.save_changes();

            // Update visual
            for (let i = 0; i < size; i++) {
              for (let j = 0; j < size; j++) {
                squares[i][j].style.backgroundColor = "black";
              }
            }
          });

          // Listen for set_all_trigger changes
          model.on("change:set_all_trigger", () => {
            // Set all to true
            grid = Array(size).fill().map(() => Array(size).fill(true));
            model.set("grid", grid);
            model.save_changes();

            // Update visual
            for (let i = 0; i < size; i++) {
              for (let j = 0; j < size; j++) {
                squares[i][j].style.backgroundColor = "white";
              }
            }
          });

          // Listen for model changes
          model.on("change:grid", () => {
            const newGrid = model.get("grid");
            grid = newGrid;
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
        reset_trigger = traitlets.Int(0).tag(sync=True)
        set_all_trigger = traitlets.Int(0).tag(sync=True)

        def __init__(self):
            # Initialize with 5x5 grid of False (black)
            self.grid = [[False for _ in range(5)] for _ in range(5)]
            super().__init__()
    return (ToggleGrid,)


@app.cell
def _(ToggleGrid, mo):
    # Create widgets
    _toggle_grid_instance0 = ToggleGrid()
    rawimage0 = mo.ui.anywidget(_toggle_grid_instance0)
    _toggle_grid_instance1 = ToggleGrid()
    rawimage1 = mo.ui.anywidget(_toggle_grid_instance1)
    _toggle_grid_instance2 = ToggleGrid()
    rawimage2 = mo.ui.anywidget(_toggle_grid_instance2)
    _toggle_grid_instance3 = ToggleGrid()
    rawimage3 = mo.ui.anywidget(_toggle_grid_instance3)

    fill_factor_2D = mo.ui.number(start=0.2, stop=1.0, label="Pixel fill factor", value=0.68)

    def reset_grid():
        """Call this function to reset the grid"""
        _toggle_grid_instance0.reset_trigger += 1
        _toggle_grid_instance1.reset_trigger += 1
        _toggle_grid_instance2.reset_trigger += 1
        _toggle_grid_instance3.reset_trigger += 1

    # Set all function
    def set_all_grid():
        """Call this function to set all grid values to True"""
        _toggle_grid_instance0.set_all_trigger += 1
        _toggle_grid_instance1.set_all_trigger += 1
        _toggle_grid_instance2.set_all_trigger += 1
        _toggle_grid_instance3.set_all_trigger += 1

    set_all_to_black = mo.ui.button(label="All pixels off", on_click=lambda _: reset_grid())
    set_all_to_white = mo.ui.button(label="All pixels on", on_click=lambda _: set_all_grid())

    irradiance_threshold = mo.ui.dropdown(options=["1 or more", "2 or more", "3 or more", "4"], label="Threshold: overlapping images", value="1 or more")
    return (
        fill_factor_2D,
        irradiance_threshold,
        rawimage0,
        rawimage1,
        rawimage2,
        rawimage3,
        set_all_to_black,
        set_all_to_white,
    )


@app.cell
def _(np):
    def extract_np_array(rawimage_grid, max_value=1):
        return np.array(rawimage_grid[::-1]).astype(float) * max_value
    return (extract_np_array,)


@app.cell
def _(
    create_grid_pattern,
    extract_np_array,
    fill_factor_2D,
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
    # fill_factor_2D = 0.68  # 68% 2D fill factor
    fill_factor_1D = np.sqrt(fill_factor_2D.value)  # 1D fill factor
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
    def plot_irradiance_pattern(img_data, xlim, ylim, threshold):
        eps = 1e-1
        if threshold == "1 or more":
            vmin = 0
        elif threshold == "2 or more":
            vmin = 1 + eps
        elif threshold == "3 or more":
            vmin = 2 + eps
        elif threshold == "4":
            vmin = 3 + eps
        else:
            raise ValueError(f"Incorrect threshold: {threshold}")
        fig, ax = plt.subplots() # 2, 3, figsize=(15, 10))
        img = ax.imshow(
            img_data, 
            cmap='gray', 
            interpolation='nearest', 
            origin='lower', 
            extent=[xlim[0], xlim[1], ylim[0], ylim[1]],
            vmin=vmin,
            vmax=4
        )
        ax.set_title('All Four Patterns Overlapped')
        ax.set_xlabel('x (102 $\mu$m pixels)')
        ax.set_ylabel('y (102 $\mu$m pixels)')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        return fig, ax
    return (plot_irradiance_pattern,)


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


if __name__ == "__main__":
    app.run()
