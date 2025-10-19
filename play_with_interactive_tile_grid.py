import marimo

__generated_with = "0.9.14"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __(mo):
    # Initialize grid state - True = black, False = white
    get_grid, set_grid = mo.state([[True] * 5 for _ in range(5)])
    return get_grid, set_grid


@app.cell
def __(get_grid, mo, set_grid):
    def create_tile(row, col, is_black):
        """Create a single tile button"""
        bg_color = "black" if is_black else "white"
        border_color = "#666"
        
        return mo.ui.button(
            label="",
            on_click=lambda _: toggle_tile(row, col),
            style={
                "width": "60px",
                "height": "60px",
                "background-color": bg_color,
                "border": f"2px solid {border_color}",
                "cursor": "pointer",
                "margin": "2px"
            }
        )
    
    def toggle_tile(row, col):
        """Toggle the state of a specific tile"""
        current_grid = get_grid()
        current_grid[row][col] = not current_grid[row][col]
        set_grid(current_grid)
    
    return create_tile, toggle_tile


@app.cell
def __(create_tile, get_grid, mo):
    # Create the grid of tiles
    grid = mo.vstack([
        mo.hstack([
            create_tile(row, col, get_grid()[row][col])
            for col in range(5)
        ])
        for row in range(5)
    ])
    
    grid
    return grid,


@app.cell
def __(get_grid, mo):
    # Display the current state of the grid
    state_display = mo.md(f"""
    ## Grid State
    
    Current grid configuration (True = Black, False = White):
    
    ```python
    {get_grid()}
    ```
    """)
    
    state_display
    return state_display,


@app.cell
def __(get_grid):
    # Access the grid state programmatically
    current_state = get_grid()
    
    # Example: Count black and white tiles
    black_count = sum(row.count(True) for row in current_state)
    white_count = sum(row.count(False) for row in current_state)
    
    print(f"Black tiles: {black_count}")
    print(f"White tiles: {white_count}")
    return black_count, current_state, white_count


if __name__ == "__main__":
    app.run()