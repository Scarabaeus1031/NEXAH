import pandapower as pp
import copy
import numpy as np


def run_2d_stability_scan_v2(
    net,
    min_load=3.5,
    max_load=4.5,
    min_gen=0.8,
    max_gen=1.2,
    steps=40
):
    """
    2D Stability Landscape:
    Load scaling vs Generation scaling

    Returns:
        load_factors (x-axis)
        gen_factors (y-axis)
        landscape (2D array: 1=stable, 0=unstable)
    """

    load_factors = np.linspace(min_load, max_load, steps)
    gen_factors = np.linspace(min_gen, max_gen, steps)

    landscape = np.zeros((steps, steps))

    for i, lf in enumerate(load_factors):
        for j, gf in enumerate(gen_factors):

            net_copy = copy.deepcopy(net)

            # 🔥 Load scaling (destabilizing force)
            net_copy.load["p_mw"] *= lf

            # 🔥 Generation scaling (stabilizing force)
            net_copy.gen["p_mw"] *= gf

            try:
                pp.runpp(net_copy, init="results")
                landscape[i, j] = 1  # stable
            except Exception:
                landscape[i, j] = 0  # unstable

    return load_factors, gen_factors, landscape
