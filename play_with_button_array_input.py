import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    # Create a state object that will store the index of the
    # clicked button
    get_state, set_state = mo.state(None)

    def flip_button_state(button):
        if button.value == False:
            return True
        else:
            return False

    buttons_raw = [
        mo.ui.button(
            label="button " + str(i), 
            value=False,
            on_change=flip_button_state,
        )
        for i in range(4)
    ]
    # Create an mo.ui.array of buttons - a regular Python list won't work.
    buttons = mo.ui.array(buttons_raw)

    # Put the buttons array into the table
    table = mo.ui.table(
        {
            "Action": ["Action Name"] * len(buttons),
            "Trigger": list(buttons),
        }
    )
    table
    return buttons, buttons_raw, get_state


@app.cell
def _(get_state):
    get_state()
    return


@app.cell
def _(get_state, mo):
    mo.output.append(get_state())
    return


@app.cell
def _(buttons):
    buttons
    return


@app.cell
def _(buttons_raw):
    buttons_raw[1].text
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
