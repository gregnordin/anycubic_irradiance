import marimo

app = marimo.App(width="medium")

@app.cell
def __():
    import marimo as mo
    import numpy as np
    return mo, np

@app.cell
def __(mo, np):
    grid, set_grid = mo.state(np.zeros((4, 4), dtype=int))
    debug, set_debug = mo.state("")
    return grid, set_grid, debug, set_debug

@app.cell
def __(grid, set_grid, debug, set_debug, mo):
    def toggle(_):
        new_grid = grid().copy()
        new_grid[0, 0] = 1 - new_grid[0, 0]
        print(f"Toggled (0,0) to {new_grid[0, 0]}")  # Terminal output
        set_debug(f"Clicked (0,0), new value: {new_grid[0, 0]}")  # In-notebook output
        set_grid(new_grid)

    button = mo.ui.button(
        label=f"{grid()[0,0]}",
        on_click=toggle
    ).style({
        "width": "30px",
        "height": "30px",
        "background-color": "white" if grid()[0, 0] == 0 else "black",
        "color": "black" if grid()[0, 0] == 0 else "white"
    })
    return button,

@app.cell
def __(button, grid, debug, mo):
    mo.vstack([
        mo.md("**Single Button Test (White: 0, Black: 1)**"),
        button,
        mo.md(f"**Debug Output:** {debug()}"),
        mo.md("**Current Array:**"),
        mo.md(f"```\n{grid()}\n```")
    ])
    return

if __name__ == "__main__":
    app.run()