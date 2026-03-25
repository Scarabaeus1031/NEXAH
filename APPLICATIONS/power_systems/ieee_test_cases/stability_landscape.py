import pandapower as pp
import copy
import numpy as np


def run_2d_stability_scan(
    net,
    bus_a,
    bus_b,
    min_factor=1.0,
    max_factor=4.5,
    steps=30
):
    factors = np.linspace(min_factor, max_factor, steps)
    landscape = np.zeros((steps, steps))

    for i, fa in enumerate(factors):
        for j, fb in enumerate(factors):

            net_copy = copy.deepcopy(net)

            # Masken für Load-Busse
            mask_a = net_copy.load["bus"] == bus_a
            mask_b = net_copy.load["bus"] == bus_b

            # Load skalieren
            net_copy.load.loc[mask_a, "p_mw"] *= fa
            net_copy.load.loc[mask_b, "p_mw"] *= fb

            try:
                pp.runpp(net_copy)
                landscape[i, j] = 1  # stable
            except Exception:
                landscape[i, j] = 0  # unstable

    return factors, landscape
