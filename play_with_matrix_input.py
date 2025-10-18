import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    return mo, np


@app.cell
def _(mo, np):
    grid, set_grid = mo.state(np.zeros((4, 4), dtype=int))
    return grid, set_grid


@app.cell
def _(grid, mo, set_grid):
    def make_toggle(i, j):
        def toggle(_):
            new_grid = grid().copy()
            new_grid[i, j] = 1 - new_grid[i, j]
            set_grid(new_grid)
        return toggle

    # buttons = [mo.ui.button(label="a") for j in range(4)]

    buttons = [
        [
            mo.ui.button(
                label="a",
                on_click=make_toggle(i, j)
            ).style({
                    "width": "30px",
                    "height": "30px",
                    "background-color": "white" if grid()[i, j] == 0 else "black",
                    # "border": "1px solid black",
                    }
            ) for j in range(4)
        ]
        for i in range(4)
    ]
    # buttons
    return (buttons,)


@app.cell
def _(buttons, mo):
    grid_ui = mo.vstack(
        [mo.hstack(row, justify="start", gap=0) for row in buttons],
        align="start",
        gap=0
    )
    return (grid_ui,)


@app.cell
def _(grid, grid_ui, mo):
    mo.vstack([
        mo.md("**4x4 Grid of Squares (White: 0, Black: 1)**"),
        grid_ui,
        mo.md("**Current Array of Numbers:**"),
        mo.md(f"```\n{grid()}\n```")
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
