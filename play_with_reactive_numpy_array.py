import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    return mo, np


@app.cell
def _(np):
    # Cell 1: Initialize the state as a NumPy array (defined only once)
    state = np.zeros((3, 3), dtype=float)

    # Cell 2: Function to update the state programmatically
    def update_matrix(i, j, value):
        global state
        state = state.copy()  # Create a copy to trigger reactivity
        state[i, j] = value
        return state
    return state, update_matrix


@app.cell
def _(state):
    state
    return


@app.cell
def _(update_matrix):
    # Cell 3: First programmatic update
    update_matrix(0, 0, 1)  # Set matrix[0, 0] to 1
    return


@app.cell
def _(mo, np, state):
    # Cell 4: Display the current state and a reactive variable
    non_zero_count = np.count_nonzero(state)
    mo.md(f"Matrix:\n{state}\n\nNumber of non-zero elements: {non_zero_count}")
    return


@app.cell
def _(mo, np, state):
    # Cell 5: Another reactive variable based on non-zero elements
    if np.any(state != 0):
        other_var = np.sum(state)
    else:
        other_var = "No non-zero elements yet"
    mo.md(f"Other variable: {other_var}")
    return


@app.cell
def _(update_matrix):
    # Cell 6: Additional programmatic update
    update_matrix(1, 2, 3.5)  # Set matrix[1, 2] to 3.5
    return


@app.cell
def _(update_matrix):
    update_matrix(0, 0, 0)
    return


@app.cell
def _(update_matrix):
    update_matrix(0, 1, 2)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
