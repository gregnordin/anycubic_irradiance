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
