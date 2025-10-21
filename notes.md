Notebook file: `xpr_irradiance_visualizer.py`

To run as app: `uv run marimo run xpr_irradiance_visualizer.py`  
To run in edit mode: `uv run marimo edit xpr_irradiance_visualizer.py`  
Export as webpage with WASM to run python:  
  `marimo export html-wasm xpr_irradiance_visualizer.py -o output_dir --mode run`

### Current state
- Single grid works with `widget.get_grid_state()` returning the 2D grid array which accurately contains clicked grid tiles
- Position grid inside a marimo container
- Make 4 grids and layout as 2x2 in marimo containers
- Convert `widget.grid` into a numpy boolean array, then into a numpy float array in range [0,1] and multiply by 0.25
- Plot data from 4 grids in matplotlib map of irradiance and show underneath 2x2 toggle grids array
- Convert overlapping rectangular patches into an image and map to grayscale [threshold, 1]
- Input to set threshold value for irradiance map
- Add buttons to turn all pixels on and all pixels off
- Add float input widget to set micromirror array fill factor
- Add labels to 4 input 102 um images to indicate shifts?
- Reduce size of 4 input images
- **Put jpg image into `/public` directory so it is used in the html-wasm export**

### Next steps
- Show 51 um grid lines in final image?
- make grid size a variable, n_size, and pass it into `ToggleGrid.__init__()`?
- Put `mo.ui.anywidget` wrapper in a function to make it easy to create fully reactive `ToggleGrid` widget
- Save state to file?
- Load state from file?
- How make image of UI and irradiance map?

