import marimo

__generated_with = "0.18.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import anywidget
    import traitlets
    return anywidget, mo, np, traitlets


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
          allOnButton.style.backgroundColor = '#4CAF50';
          allOnButton.style.color = 'white';
          allOnButton.style.border = '1px solid #45a049';
          allOnButton.style.borderRadius = '4px';
      
          const allOffButton = document.createElement('button');
          allOffButton.textContent = 'All Off';
          allOffButton.style.padding = '8px 16px';
          allOffButton.style.cursor = 'pointer';
          allOffButton.style.fontSize = '12px';
          allOffButton.style.backgroundColor = '#f44336';
          allOffButton.style.color = 'white';
          allOffButton.style.border = '1px solid #da190b';
          allOffButton.style.borderRadius = '4px';
      
          // Add hover effects
          allOnButton.addEventListener('mouseenter', () => {
            allOnButton.style.backgroundColor = '#45a049';
          });
          allOnButton.addEventListener('mouseleave', () => {
            allOnButton.style.backgroundColor = '#4CAF50';
          });
      
          allOffButton.addEventListener('mouseenter', () => {
            allOffButton.style.backgroundColor = '#da190b';
          });
          allOffButton.addEventListener('mouseleave', () => {
            allOffButton.style.backgroundColor = '#f44336';
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
    return (phys_arrays_text,)


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
def _(mo, phys_arrays_text, xpr_grid, xpr_grid_text_display):
    # Display grid values with spaces between numbers
    # rows_text = format_array_for_text_display(
    #     np.array(xpr_grid.value.get("grid_values"))
    # )

    # Display grid and values
    mo.vstack([
        xpr_grid, 
        mo.hstack(
            [
                xpr_grid_text_display,
                mo.vstack([
                    mo.md("Physical pixels"),
                        phys_arrays_text,
                ]),
            ],
            justify="start",
            gap=2.0,
            widths=[0,0]
        )
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
