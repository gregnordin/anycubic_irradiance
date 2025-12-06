import marimo

__generated_with = "0.18.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    return mo, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ChatGPT version
    """)
    return


@app.cell
def _():
    import anywidget
    import traitlets

    class GridWidget(anywidget.AnyWidget):
        _esm = """
        function render({ model, el }) {
          const size = model.get("size") || 9;
          el.innerHTML = "";

          const container = document.createElement("div");
          container.style.display = "inline-grid";
          container.style.gridTemplateColumns = "repeat(" + size + ", 24px)";
          container.style.gridTemplateRows = "repeat(" + size + ", 24px)";
          container.style.gap = "1px";               // smaller visual separation
          container.style.backgroundColor = "#444";  // grid line color

          const status = document.createElement("div");
          status.style.marginTop = "8px";
          status.style.fontFamily = "monospace";

          el.appendChild(container);
          el.appendChild(status);

          const cells = Array.from({ length: size }, () => Array(size));
          const getGrid = () => model.get("value") || Array.from({ length: size }, () => Array(size).fill(0));

          function colorFor(v) { return v ? "white" : "black"; }

          function updateStatus() {
            const r = model.get("last_row");
            const c = model.get("last_col");
            if (r === null || c === null) status.textContent = "Last clicked: (none)";
            else status.textContent = "Last clicked: (" + r + ", " + c + ")";
          }

          function refreshFromModel() {
            const grid = getGrid();
            for (let r = 0; r < size; r++) {
              for (let c = 0; c < size; c++) {
                const cell = cells[r][c];
                if (!cell) continue;
                cell.style.backgroundColor = colorFor(grid[r][c]);
              }
            }
          }

          const grid = getGrid();
          for (let pyRow = size - 1; pyRow >= 0; pyRow--) {
            for (let col = 0; col < size; col++) {
              const cell = document.createElement("div");
              cell.style.width = "24px";
              cell.style.height = "24px";
              cell.style.cursor = "pointer";
              cell.style.boxSizing = "border-box";
              cell.style.border = "none";             // no per-cell border
              cell.dataset.row = String(pyRow);
              cell.dataset.col = String(col);
              cell.style.backgroundColor = colorFor(grid[pyRow][col]);

              cell.addEventListener("click", () => {
                const r = parseInt(cell.dataset.row);
                const c = parseInt(cell.dataset.col);
                const g = getGrid();
                g[r][c] = g[r][c] ? 0 : 1;
                model.set("value", g);
                model.set("last_row", r);
                model.set("last_col", c);
                model.save_changes();
                cell.style.backgroundColor = colorFor(g[r][c]);
                updateStatus();
              });

              cells[pyRow][col] = cell;
              container.appendChild(cell);
            }
          }

          model.on("change:value", refreshFromModel);
          model.on("change:last_row", updateStatus);
          model.on("change:last_col", updateStatus);

          updateStatus();
        }
        export default { render };
        """

        size = traitlets.Int(9).tag(sync=True)
        value = traitlets.List(
            traitlets.List(traitlets.Int())
        ).tag(sync=True)
        last_row = traitlets.Int(allow_none=True, default_value=None).tag(sync=True)
        last_col = traitlets.Int(allow_none=True, default_value=None).tag(sync=True)

        def __init__(self, **kwargs):
            if "value" not in kwargs:
                kwargs["value"] = [[0 for _ in range(9)] for _ in range(9)]
            super().__init__(**kwargs)

    return GridWidget, anywidget, traitlets


@app.cell
def _(GridWidget, mo):
    xpr_pixel_array_ideal_widget = mo.ui.anywidget(GridWidget())
    xpr_pixel_array_ideal_widget
    return (xpr_pixel_array_ideal_widget,)


@app.cell
def _(xpr_pixel_array_ideal_widget):
    print(
        xpr_pixel_array_ideal_widget.value,          # 9x9 array of 0/1
        xpr_pixel_array_ideal_widget.last_row,
        xpr_pixel_array_ideal_widget.last_col,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Claude version
    """)
    return


@app.cell
def _(anywidget, traitlets):
    class GridWidget2(anywidget.AnyWidget):
        _esm = """
        function render({ model, el }) {
          const container = document.createElement('div');
          container.style.display = 'flex';
          container.style.flexDirection = 'column';
          container.style.alignItems = 'center';
          container.style.fontFamily = 'Arial, sans-serif';
      
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
          
              cell.addEventListener('click', () => {
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
              });
          
              cells[displayRow][col] = cell;
              gridContainer.appendChild(cell);
            }
          }
      
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
    def create_grid():
        """Create and return a new GridWidget instance."""
        return GridWidget2()
    return (create_grid,)


@app.cell
def _(create_grid, mo):
    # Create the widget
    grid = mo.ui.anywidget(create_grid())
    return (grid,)


@app.cell
def _(grid, mo, np):
    # Display grid values with spaces between numbers
    arr = np.array(grid.value.get("grid_values"))
    rows_text = "\n".join([" ".join(map(str, row)) for row in arr[::-1]])

    # Display grid and values
    mo.vstack([grid, mo.md(f"```\n{rows_text}\n```")])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
