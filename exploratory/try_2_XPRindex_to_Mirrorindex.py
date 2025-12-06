import marimo

__generated_with = "0.18.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import pytest
    return (mo,)


@app.cell
def _():
    ii = [0, 1, 2, 3, 4]
    jj = [0, 1, 2, 3, 4]
    i = ii[1]
    j = jj[1]

    def mi(i):
        """
        Given 1D XPR pixel index i, return 1D physical mirror index, i'.
        See handwritten notes.
        """
        return (i + i%2) // 2

    def quadrant(i,j):
        """
        Return which quadrant of a physical mirror the XPR i,j pixel lands on.
        """
        return (0 if j%2 == 1 else 1) if i%2 == 1 else (2 if j%2 == 1 else 3)

    def convert_to_phys_mirror(i,j):
        """
        Given XPR pixel index i,j, return physical mirror index i',j' and
        mirror quadrant as one of [0,1,2,3] (lower left, lower right, 
        upper left, upper right).
        """
        return mi(i), mi(j), quadrant(i,j)

    for i in ii:
        for j in jj:
            print(i, j, "  ", mi(i), mi(j), quadrant(i,j))
    return convert_to_phys_mirror, ii, jj, mi, quadrant


@app.cell
def _(convert_to_phys_mirror, ii, jj):
    for i1 in ii:
        for j1 in jj:
            print(i1, j1, "  ", convert_to_phys_mirror(i1,j1))
    return


@app.cell
def _():
    return


@app.cell
def _(convert_to_phys_mirror, ii, jj):
    def xpr_to_phys_mirrors(i, j):
        """
        Determine indices of which 4 physical mirrors must be turned on
        to turn on XPR pixel i,j.
    
        Parameters
        ----------
        i : int
            Row index of the XPR pixel
        j : int
            Column index of the XPR pixel
    
        Returns
        -------
        list of tuple
            List of 4 tuples (ip, jp) representing the physical mirror indices
            that need to be turned on. The mapping depends on which quadrant
            of the physical mirror the XPR pixel maps to:
            - Quadrant 0: Mirror ip,jp unshifted and 3 shifted mirrors in negative x, y, and xy directions
            - Quadrant 1: Mirror ip,jp unshifted and x-shifted, and mirror in -y direction shifted in y and xy
            - Quadrant 2: Mirror ip,jp unshifted and y-shifted, and mirror in -x direction shifted in x and xy
            - Quadrant 3: Mirror ip,jp unshifted and x-, y-, and xy-shifted
    
        Notes
        -----
        Each XPR pixel maps to a location within an unshifted physical mirror, divided
        into 4 quadrants. Depending on the quadrant, different combinations
        of the shifted physical mirrors must be activated to illuminate
        the XPR pixel position.
        """
        ip, jp, quadrant = convert_to_phys_mirror(i,j)
        if quadrant == 0:
            return [(ip, jp), (ip, jp-1), (ip-1, jp), (ip-1, jp-1)]
        elif quadrant == 1:
            return [(ip, jp), (ip, jp), (ip-1, jp), (ip-1, jp)]
        elif quadrant == 2:
            return [(ip, jp), (ip, jp-1), (ip, jp), (ip, jp-1)]
        elif quadrant == 3:
            return [(ip, jp), (ip, jp), (ip, jp), (ip, jp)]

    for i2 in ii:
        for j2 in jj:
            print(xpr_to_phys_mirrors(i2,j2))
    return (xpr_to_phys_mirrors,)


@app.cell
def _(xpr_to_phys_mirrors):
    print(xpr_to_phys_mirrors(2, 1))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Tests
    """)
    return


@app.cell
def _(convert_to_phys_mirror, mi, quadrant, xpr_to_phys_mirrors):
    def test_mi():
        assert mi(0) == 0
        assert mi(1) == 1
        assert mi(2) == 1
        assert mi(3) == 2
        assert mi(4) == 2

    def test_quadrant():
        assert quadrant(1,1) == 0
        assert quadrant(1,2) == 1
        assert quadrant(2,1) == 2
        assert quadrant(2,2) == 3

    def test_convert_to_phys_mirror():
        assert convert_to_phys_mirror(0,0) == (0, 0, 3)
        assert convert_to_phys_mirror(1,0) == (1, 0, 1)
        assert convert_to_phys_mirror(1,1) == (1, 1, 0)
        assert convert_to_phys_mirror(1,2) == (1, 1, 1)
        assert convert_to_phys_mirror(1,3) == (1, 2, 0)
        assert convert_to_phys_mirror(1,4) == (1, 2, 1)
        assert convert_to_phys_mirror(2,0) == (1, 0, 3)
        assert convert_to_phys_mirror(2,1) == (1, 1, 2)
        assert convert_to_phys_mirror(2,2) == (1, 1, 3)
        assert convert_to_phys_mirror(2,3) == (1, 2, 2)
        assert convert_to_phys_mirror(2,4) == (1, 2, 3)

    def test_xpr_to_phys_mirrors():
        assert xpr_to_phys_mirrors(0, 0) == [(0, 0), (0, 0), (0, 0), (0, 0)]
        assert xpr_to_phys_mirrors(0, 1) == [(0, 1), (0, 0), (0, 1), (0, 0)]
        assert xpr_to_phys_mirrors(0, 2) == [(0, 1), (0, 1), (0, 1), (0, 1)]
        assert xpr_to_phys_mirrors(1, 0) == [(1, 0), (1, 0), (0, 0), (0, 0)]
        assert xpr_to_phys_mirrors(1, 1) == [(1, 1), (1, 0), (0, 1), (0, 0)]
        assert xpr_to_phys_mirrors(1, 2) == [(1, 1), (1, 1), (0, 1), (0, 1)]
        assert xpr_to_phys_mirrors(2, 0) == [(1, 0), (1, 0), (1, 0), (1, 0)]
        assert xpr_to_phys_mirrors(2, 1) == [(1, 1), (1, 0), (1, 1), (1, 0)]
        assert xpr_to_phys_mirrors(2, 2) == [(1, 1), (1, 1), (1, 1), (1, 1)]
        assert not (xpr_to_phys_mirrors(2, 3) == [(1, 1), (1, 1), (1, 1), (1, 1)])

    test_mi()
    test_quadrant()
    test_convert_to_phys_mirror()
    test_xpr_to_phys_mirrors()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
