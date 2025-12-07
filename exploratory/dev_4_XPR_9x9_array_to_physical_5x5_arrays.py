import marimo

__generated_with = "0.18.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    import mplcursors
    import anywidget
    import traitlets
    return anywidget, go, mo, np, traitlets


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## XPR grid code
    """)
    return


@app.cell
def _(anywidget, traitlets):
    class XPRGridWidget(anywidget.AnyWidget):
        _esm = """
        function render({ model, el }) {
          const container = document.createElement('div');
          container.style.display = 'flex';
          container.style.flexDirection = 'column';
          container.style.alignItems = 'center';
          container.style.fontFamily = 'Arial, sans-serif';

          // Buttons container
          const buttonsContainer = document.createElement('div');
          buttonsContainer.style.display = 'flex';
          buttonsContainer.style.gap = '10px';
          buttonsContainer.style.marginBottom = '10px';

          const allOnButton = document.createElement('button');
          allOnButton.textContent = 'All On';
          allOnButton.style.padding = '8px 16px';
          allOnButton.style.cursor = 'pointer';
          allOnButton.style.fontSize = '12px';
          allOnButton.style.backgroundColor = 'white';
          allOnButton.style.color = 'black';
          allOnButton.style.border = '1px solid black';
          allOnButton.style.borderRadius = '4px';

          const allOffButton = document.createElement('button');
          allOffButton.textContent = 'All Off';
          allOffButton.style.padding = '8px 16px';
          allOffButton.style.cursor = 'pointer';
          allOffButton.style.fontSize = '12px';
          allOffButton.style.backgroundColor = 'white';
          allOffButton.style.color = 'black';
          allOffButton.style.border = '1px solid black';
          allOffButton.style.borderRadius = '4px';

          // Add hover effects
          allOnButton.addEventListener('mouseenter', () => {
            allOnButton.style.backgroundColor = '#F2F2F2';
          });
          allOnButton.addEventListener('mouseleave', () => {
            allOnButton.style.backgroundColor = 'white';
          });

          allOffButton.addEventListener('mouseenter', () => {
            allOffButton.style.backgroundColor = '#F2F2F2';
          });
          allOffButton.addEventListener('mouseleave', () => {
            allOffButton.style.backgroundColor = 'white';
          });

          buttonsContainer.appendChild(allOnButton);
          buttonsContainer.appendChild(allOffButton);

          const gridContainer = document.createElement('div');
          gridContainer.style.display = 'grid';
          gridContainer.style.gridTemplateColumns = 'repeat(9, 20px)';
          gridContainer.style.gridTemplateRows = 'repeat(9, 20px)';
          gridContainer.style.gap = '1px';
          gridContainer.style.backgroundColor = '#333';
          gridContainer.style.padding = '1px';
          gridContainer.style.marginBottom = '20px';

          const info = document.createElement('div');
          info.style.fontSize = '14px';
          info.style.color = '#333';
          info.textContent = 'Click any cell to toggle';

          // Create grid state (all cells start black = 0)
          const gridState = Array(9).fill(null).map(() => Array(9).fill(0));

          // Track mouse state for dragging
          let isMouseDown = false;
          let dragValue = null; // The value to paint while dragging

          // Create cells
          const cells = [];
          for (let displayRow = 0; displayRow < 9; displayRow++) {
            cells[displayRow] = [];
            for (let col = 0; col < 9; col++) {
              const cell = document.createElement('div');
              cell.style.width = '20px';
              cell.style.height = '20px';
              cell.style.backgroundColor = 'black';
              cell.style.cursor = 'pointer';

              // Row index: 0 at bottom, 8 at top
              // displayRow 0 -> actual row 8
              // displayRow 8 -> actual row 0
              const actualRow = 8 - displayRow;

              const toggleCell = () => {
                // Toggle state
                gridState[actualRow][col] = 1 - gridState[actualRow][col];

                // Update color
                cell.style.backgroundColor = gridState[actualRow][col] === 0 ? 'black' : 'white';

                // Update info
                info.textContent = `Last clicked: (${actualRow}, ${col})`;

                // Send to Python
                model.set('last_clicked', [actualRow, col]);
                model.set('grid_values', gridState.map(row => [...row]));
                model.save_changes();

                return gridState[actualRow][col];
              };

              const setCell = (value) => {
                gridState[actualRow][col] = value;
                cell.style.backgroundColor = value === 0 ? 'black' : 'white';
                model.set('last_clicked', [actualRow, col]);
                model.set('grid_values', gridState.map(row => [...row]));
                model.save_changes();
              };

              cell.addEventListener('mousedown', (e) => {
                e.preventDefault();
                isMouseDown = true;
                dragValue = toggleCell();
              });

              cell.addEventListener('mouseenter', () => {
                if (isMouseDown && dragValue !== null) {
                  setCell(dragValue);
                  info.textContent = `Last clicked: (${actualRow}, ${col})`;
                }
              });

              cells[displayRow][col] = cell;
              gridContainer.appendChild(cell);
            }
          }

          // Global mouse up handler to stop dragging
          document.addEventListener('mouseup', () => {
            isMouseDown = false;
            dragValue = null;
          });

          // All On button - sets all cells to 1 (white)
          allOnButton.addEventListener('click', () => {
            for (let row = 0; row < 9; row++) {
              for (let col = 0; col < 9; col++) {
                gridState[row][col] = 1;
                const displayRow = 8 - row;
                cells[displayRow][col].style.backgroundColor = 'white';
              }
            }
            info.textContent = 'All pixels on';
            model.set('grid_values', gridState.map(row => [...row]));
            model.save_changes();
          });

          // All Off button - sets all cells to 0 (black)
          allOffButton.addEventListener('click', () => {
            for (let row = 0; row < 9; row++) {
              for (let col = 0; col < 9; col++) {
                gridState[row][col] = 0;
                const displayRow = 8 - row;
                cells[displayRow][col].style.backgroundColor = 'black';
              }
            }
            info.textContent = 'All pixels off';
            model.set('grid_values', gridState.map(row => [...row]));
            model.save_changes();
          });

          container.appendChild(buttonsContainer);
          container.appendChild(gridContainer);
          container.appendChild(info);
          el.appendChild(container);
        }
        export default { render };
        """


        # Traitlet to track the last clicked cell
        last_clicked = traitlets.List(default_value=None, allow_none=True).tag(sync=True)

        # Traitlet to track all grid values (0 = black, 1 = white)
        grid_values = traitlets.List(default_value=[[0]*9 for _ in range(9)]).tag(sync=True)


    # Create an instance of the widget
    def create_xpr_grid():
        """Create and return a new GridWidget instance."""
        return XPRGridWidget()
    return (create_xpr_grid,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## XPR grid coordinates to physical grid coordinates
    """)
    return


@app.cell
def _():
    def mi(i):
        """
        Given 1D XPR pixel index i, return 1D physical mirror index, i'.
        See handwritten notes.
        """
        return (i + i%2) // 2

    def quadrant(i,j):
        """
        Return which quadrant of a physical mirror the XPR i,j pixel lands on.
        """
        return (0 if j%2 == 1 else 1) if i%2 == 1 else (2 if j%2 == 1 else 3)

    def convert_to_phys_mirror(i,j):
        """
        Given XPR pixel index i,j, return physical mirror index i',j' and
        mirror quadrant as one of [0,1,2,3] (lower left, lower right, 
        upper left, upper right).
        """
        return mi(i), mi(j), quadrant(i,j)

    def xpr_to_phys_mirrors(i, j):
        """
        Determine indices of which 4 physical mirrors must be turned on
        to turn on XPR pixel i,j.

        Parameters
        ----------
        i : int
            Row index of the XPR pixel
        j : int
            Column index of the XPR pixel

        Returns
        -------
        list of tuple
            List of 4 tuples (ip, jp) representing the physical mirror indices
            that need to be turned on. The mapping depends on which quadrant
            of the physical mirror the XPR pixel maps to:
            - Quadrant 0: Mirror ip,jp unshifted and 3 shifted mirrors in negative x, y, and xy directions
            - Quadrant 1: Mirror ip,jp unshifted and x-shifted, and mirror in -y direction shifted in y and xy
            - Quadrant 2: Mirror ip,jp unshifted and y-shifted, and mirror in -x direction shifted in x and xy
            - Quadrant 3: Mirror ip,jp unshifted and x-, y-, and xy-shifted

        Notes
        -----
        Each XPR pixel maps to a location within an unshifted physical mirror, divided
        into 4 quadrants. Depending on the quadrant, different combinations
        of the shifted physical mirrors must be activated to illuminate
        the XPR pixel position.
        """
        ip, jp, quadrant = convert_to_phys_mirror(i,j)
        if quadrant == 0:
            return [(ip, jp), (ip, jp-1), (ip-1, jp), (ip-1, jp-1)]
        elif quadrant == 1:
            return [(ip, jp), (ip, jp), (ip-1, jp), (ip-1, jp)]
        elif quadrant == 2:
            return [(ip, jp), (ip, jp-1), (ip, jp), (ip, jp-1)]
        elif quadrant == 3:
            return [(ip, jp), (ip, jp), (ip, jp), (ip, jp)]
    return (xpr_to_phys_mirrors,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Utilities
    """)
    return


@app.cell
def _(mo):
    def format_array_for_text_print(arr):
        return "\n".join([" ".join(map(str, row)) for row in arr[::-1]])

    def array_to_html_text(arr):
        text = format_array_for_text_print(arr)
        f"<pre>{text}</pre>"
        return mo.Html(f"<pre>{text}</pre>")
    return (array_to_html_text,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Physical pixel arrays
    """)
    return


@app.cell
def _(np, xpr_to_phys_mirrors):
    # Create physical pixel arrays
    phys_px_unshifted = np.zeros((5,5), dtype=int)
    phys_px_shifted_x = np.zeros_like(phys_px_unshifted)
    phys_px_shifted_y = np.zeros_like(phys_px_unshifted)
    phys_px_shifted_xy = np.zeros_like(phys_px_unshifted)

    # Store previous grid state to detect changes
    previous_grid_values = np.zeros((9, 9), dtype=int)

    def update_physical_arrays(current_grid_values):
        """
        Update the 5x5 physical arrays based on changes in the 9x9 grid.

        Args:
            current_grid_values: 9x9 array from grid.value.get("grid_values")
        """
        global phys_px_unshifted, phys_px_shifted_x, phys_px_shifted_y, phys_px_shifted_xy
        global previous_grid_values

        current_grid = np.array(current_grid_values)

        # Find cells that changed
        changed_mask = current_grid != previous_grid_values

        # Get the 4 arrays in a list for easy indexing
        phys_arrays = [phys_px_unshifted, phys_px_shifted_x, phys_px_shifted_y, phys_px_shifted_xy]

        # Loop over each position
        for i in range(9):
            for j in range(9):
                if changed_mask[i, j]:
                    # Get the mapping indices for this grid position
                    indices = xpr_to_phys_mirrors(i, j)

                    # Determine increment or decrement
                    delta = 1 if current_grid[i, j] == 1 else -1

                    # Update each of the 4 arrays
                    for array_idx, (row, col) in enumerate(indices):
                        phys_arrays[array_idx][row, col] += delta

        # Update previous state
        previous_grid_values = current_grid.copy()
    return (
        phys_px_shifted_x,
        phys_px_shifted_xy,
        phys_px_shifted_y,
        phys_px_unshifted,
        update_physical_arrays,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Create widgets
    """)
    return


@app.cell
def _(
    array_to_html_text,
    mo,
    phys_px_shifted_x,
    phys_px_shifted_xy,
    phys_px_shifted_y,
    phys_px_unshifted,
    update_physical_arrays,
    xpr_grid,
):
    current_values = xpr_grid.value.get("grid_values")
    update_physical_arrays(current_values)

    # Create a trigger value that changes when arrays are updated
    arrays_updated = id(current_values)  # Use id as a unique trigger

    phys_arrays_text = mo.hstack(
        [
            mo.vstack([
                mo.md("Shift +y"),
                array_to_html_text(phys_px_shifted_y), 
                mo.md("Unshifted"),
                array_to_html_text(phys_px_unshifted),
            ]),
            mo.vstack([
                mo.md("Shift +xy"),
                array_to_html_text(phys_px_shifted_xy), 
                mo.md("Shift +x"),
                array_to_html_text(phys_px_shifted_x),
            ]),
        ], 
        justify="start", 
        gap=3.0, 
        widths=[0, 0],
    )
    return arrays_updated, phys_arrays_text


@app.cell
def _(mo):
    irradiance_threshold_2 = mo.ui.dropdown(options=["1 or more", "2 or more", "3 or more", "4"], label="Threshold: overlapping physical arrays", value="1 or more")
    return (irradiance_threshold_2,)


@app.cell
def _(mo):
    fill_factor_2D_2 = mo.ui.number(start=0.2, stop=1.0, label="Pixel fill factor", value=0.68)
    return (fill_factor_2D_2,)


@app.cell
def _(create_xpr_grid, mo):
    xpr_grid = mo.ui.anywidget(create_xpr_grid())
    return (xpr_grid,)


@app.cell
def _(array_to_html_text, mo, np, xpr_grid):
    xpr_grid_text = array_to_html_text(np.array(xpr_grid.value.get("grid_values")))
    xpr_grid_text_display = mo.vstack([
        mo.md("XPR pixels"),
        xpr_grid_text,
    ])
    return (xpr_grid_text_display,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## App
    """)
    return


@app.cell
def _(
    fill_factor_2D_2,
    irradiance_threshold_2,
    mo,
    phys_arrays_text,
    plot_fig,
    xpr_grid,
    xpr_grid_text_display,
):
    # Display grid and values
    horizontal_spacer = " "
    vertical_spacer = mo.Html("<pre> </pre>")
    mo.vstack([
        mo.hstack([
            mo.vstack([
                mo.center(mo.md("## XPR DLP Pixels")),
                xpr_grid,
                # vertical_spacer,
                mo.md("---"),
                irradiance_threshold_2,
                fill_factor_2D_2,
                mo.md("---"),
            ]),
            mo.vstack([
                mo.center(mo.md("## Generated Irradiance Pattern")),            
                plot_fig,
            ]),
        ]),
        vertical_spacer,
        mo.hstack(
            [
                horizontal_spacer,
                xpr_grid_text_display,
                horizontal_spacer,
                mo.vstack([
                    mo.md("Physical pixels"),
                    phys_arrays_text,
                ]),
            ],
            justify="start",
            gap=5.0,
            widths=[0,0,0,0]
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Use code from other marimo app
    """)
    return


@app.cell
def _(
    arrays_updated,
    create_grid_pattern,
    extract_np_array,
    fill_factor_2D_2,
    np,
    phys_px_shifted_x,
    phys_px_shifted_xy,
    phys_px_shifted_y,
    phys_px_unshifted,
    render_rectangles_direct,
    shift_rectangles,
    xpr_grid,
):
    # Trigger reactivity by accessing xpr_grid.value
    _ = xpr_grid.value
    _ = arrays_updated

    # Parameters
    grid_size = 5
    square_size = 1.0  # Grid spacing
    # fill_factor_2D = 0.68  # 68% 2D fill factor
    fill_factor_1D = np.sqrt(fill_factor_2D_2.value) # fill_factor_2D.value)  # 1D fill factor
    pixels_per_square = 50  # Number of pixels per grid square

    # Calculate image size based on pixels per square
    xlim = (0, grid_size * square_size + 0.5 * square_size)
    ylim = (0, grid_size * square_size + 0.5 * square_size)
    img_width = int((xlim[1] - xlim[0]) * pixels_per_square)
    img_height = int((ylim[1] - ylim[0]) * pixels_per_square)
    img_size = (img_height, img_width)

    # Create the unshifted grid with fill factor
    rectangles_unshifted = create_grid_pattern(
        grid_size, 
        square_size, 
        fill_factor_1D, 
        extract_np_array(phys_px_unshifted, reverse_order=False))

    # Create shifted grids
    shift_amount = 0.5 * square_size
    rectangles_shifted_x = shift_rectangles(
        create_grid_pattern(
            grid_size, 
            square_size, 
            fill_factor_1D, 
            extract_np_array(phys_px_shifted_x, reverse_order=False)
        ), 
        shift_x=shift_amount, 
        shift_y=0
    )
    rectangles_shifted_y = shift_rectangles(
        create_grid_pattern(
            grid_size, 
            square_size, 
            fill_factor_1D, 
            extract_np_array(phys_px_shifted_y, reverse_order=False)
        ), 
        shift_x=0, 
        shift_y=shift_amount)
    rectangles_shifted_xy = shift_rectangles(
        create_grid_pattern(
            grid_size, 
            square_size, 
            fill_factor_1D, 
            extract_np_array(phys_px_shifted_xy, reverse_order=False)
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
def _(
    irradiance_threshold_2,
    overlap_image,
    plot_irradiance_pattern,
    xlim,
    ylim,
):
    plot_fig, plot_ax = plot_irradiance_pattern(
        overlap_image, xlim, ylim, 
        irradiance_threshold_2.value, 
        title=""
    )
    return (plot_fig,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Code from other marimo app
    """)
    return


@app.cell
def _(np):
    def extract_np_array(rawimage_grid, max_value=1, reverse_order=True):
        if reverse_order:
            return np.array(rawimage_grid[::-1]).astype(float) * max_value
        else:
            return np.array(rawimage_grid).astype(float) * max_value
    return (extract_np_array,)


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
                if pattern[i, j] >= 1:
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
def _(go, np):
    def plot_irradiance_pattern(img_data, xlim, ylim, threshold, title="All Four Patterns Overlapped"):
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
    
        # Create plotly figure
        fig = go.Figure(data=go.Heatmap(
            z=img_data,
            x=np.linspace(xlim[0], xlim[1], img_data.shape[1]),
            y=np.linspace(ylim[0], ylim[1], img_data.shape[0]),
            colorscale='gray',
            zmin=vmin,
            zmax=4,
            showscale=False,  # Remove colorbar
            hovertemplate='x: %{x:.3f}<br>y: %{y:.3f}<br>value: %{z:.2f}<extra></extra>'
        ))
    
        fig.update_layout(
            # title=title,
            # xaxis_title='x',
            # yaxis_title='y',
            width=360,
            height=360,
            showlegend=False,
            xaxis=dict(
                range=[xlim[0], xlim[1]], 
                constrain='domain',
                visible=False  # Hide entire axis
            ),
            yaxis=dict(
                range=[ylim[0], ylim[1]], 
                scaleanchor="x", 
                scaleratio=1, 
                constrain='domain',
                visible=False  # Hide entire axis
            ),        
            # xaxis=dict(range=[xlim[0], xlim[1]], constrain='domain'),
            # yaxis=dict(range=[ylim[0], ylim[1]], scaleanchor="x", scaleratio=1, constrain='domain'),
            plot_bgcolor='white',
            margin=dict(l=50, r=0, t=35, b=115)
        )

        return fig, None
    return (plot_irradiance_pattern,)


@app.cell
def _():
    # def plot_irradiance_pattern(img_data, xlim, ylim, threshold, title="All Four Patterns Overlapped"):
    #     eps = 1e-1
    #     if threshold == "1 or more":
    #         vmin = 0
    #     elif threshold == "2 or more":
    #         vmin = 1 + eps
    #     elif threshold == "3 or more":
    #         vmin = 2 + eps
    #     elif threshold == "4":
    #         vmin = 3 + eps
    #     else:
    #         raise ValueError(f"Incorrect threshold: {threshold}")
    #     fig, ax = plt.subplots() # 2, 3, figsize=(15, 10))
    #     img = ax.imshow(
    #         img_data, 
    #         cmap='gray', 
    #         interpolation='nearest', 
    #         origin='lower', 
    #         extent=[xlim[0], xlim[1], ylim[0], ylim[1]],
    #         vmin=vmin,
    #         vmax=4
    #     )
    #     ax.set_title(title)
    #     ax.set_xlabel('x')
    #     ax.set_ylabel('y')
    #     ax.grid(True, alpha=0.3)
    #     ax.set_aspect('equal')

    # # Add interactive hover using mplcursors
    #     cursor = mplcursors.cursor(img, hover=True)

    #     @cursor.connect("add")
    #     def on_add(sel):
    #         x, y = sel.target
    #         # Convert data coordinates to image pixel coordinates
    #         x_pixel = int((x - xlim[0]) / (xlim[1] - xlim[0]) * img_data.shape[1])
    #         y_pixel = int((y - ylim[0]) / (ylim[1] - ylim[0]) * img_data.shape[0])

    #         if 0 <= x_pixel < img_data.shape[1] and 0 <= y_pixel < img_data.shape[0]:
    #             pixel_value = img_data[y_pixel, x_pixel]
    #             sel.annotation.set_text(f'Value: {pixel_value:.2f}\nx={x:.3f}, y={y:.3f}')

    #     return fig, ax
    return


if __name__ == "__main__":
    app.run()
