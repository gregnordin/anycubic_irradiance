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
    get_m0_state, set_m0_state = mo.state(np.zeros((3,3)))
    get_m0_state, set_m0_state = mo.state([[0]*3, [0]*3, [0]*3])
    return (get_m0_state,)


@app.cell
def _(get_m0_state):
    get_m0_state()
    return


@app.cell
def _(get_m0_state):
    temp_m0 = get_m0_state().copy()
    temp_m0[0][0] = 1
    temp_m0[1][1] = 2
    temp_m0
    return


@app.cell
def _(get_m0_state):
    get_m0_state()
    return


@app.cell
def _():
    # set_m0_state(temp_m0)
    # get_m0_state()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
