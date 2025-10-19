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

    # Next steps
    - make grid size a variable, n_size, and pass it into `ToggleGrid.__init__()`?
    - Convert `widget.grid` into a numpy boolean array, then into a numpy float array in range [0,1] and multiply by 0.25
    - Plot data from 4 grids in matplotlib map of irradiance and show underneath 2x2 toggle grids array
    """
    )
    return


@app.cell
def _():
    import marimo as mo
    import anywidget
    import traitlets
    return anywidget, mo, traitlets


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
    return (ToggleGrid,)


@app.cell
def _(ToggleGrid, mo):
    # Create widgets
    rawimage0 = ToggleGrid()
    rawimage1 = ToggleGrid()
    rawimage2 = ToggleGrid()
    rawimage3 = ToggleGrid()

    # Display it
    mo.vstack([
        mo.hstack([rawimage1, rawimage2], justify="start"),
        mo.hstack([rawimage0, rawimage3], justify="start"),
    ])

    return rawimage0, rawimage3


@app.cell
def _(rawimage0):
    rawimage0.get_grid_state()
    return


@app.cell
def _(rawimage3):
    rawimage3.get_grid_state()
    return


@app.cell
def _(rawimage0):
    rawimage0.grid
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
