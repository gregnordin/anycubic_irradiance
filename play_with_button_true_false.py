import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    return mo, np


@app.cell
def _(mo):
    # Use a number input to track the count (hidden)
    counter = mo.ui.number(start=0, value=0)
    return (counter,)


@app.cell
def _(counter, mo):
    # Create button that references the counter
    button = mo.ui.button(
        label=f"Count: {counter.value}",
        on_click=lambda _: counter._update(counter.value + 1)
    )

    mo.hstack([button, counter])  # Show counter to make it reactive
    return


@app.cell
def _(mo):
    # Create the toggle button, starting with False; flip on each click
    toggle_button = mo.ui.button(
        value=0,
        on_click=lambda current_value: 1 - current_value,
        label="Toggle Me"
    # ).style({
    #         "background-color": "black" if button_matrix_state[0,0] == 0 else "white",
    #         "width": "95px",  # Optional: Set size for visibility
    #         "height": "40px",
    #         "border": "1px solid gray"  # Optional: Border for visibility
    #     }
    )
    toggle_button
    return (toggle_button,)


@app.cell
def _(toggle_button):
    toggle_button.value
    return


@app.cell
def _(mo, toggle_button):
    # This cell reactively shows the button's value
    mo.md(f"**Toggle State**: {toggle_button.value}")
    return


@app.cell
def _(np):
    button_matrix_state = np.zeros((2,2))
    button_matrix_state
    return (button_matrix_state,)


@app.cell
def _(button_matrix_state, mo):
    # Create a toggle button with no label and dynamic background color
    toggle_button2 = mo.ui.button(
        value=button_matrix_state[0,0],
        on_click=lambda v: 1 - button_matrix_state[0,0],
        # label="a",  # No label
    ).style({
            "background-color": "black" if button_matrix_state[0,0] == 0 else "white",
            "width": "50px",  # Optional: Set size for visibility
            "height": "50px",
            "border": "1px solid gray"  # Optional: Border for visibility
        }
    )
    toggle_button2
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
