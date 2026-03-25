import pandapower as pp
import copy
import numpy as np


def run_2d_stability_scan(
    net,
    bus_a,
    bus_b,
    min_factor=3.9,
    max_factor=4.3,
    steps=50
):
    factors = np.linspace(min_factor, max_factor, steps)
    landscape = np.zeros((steps, steps))

    for i, fa in enumerate(factors):
        for j, fb in enumerate(factors):

            net_copy = copy.deepcopy(net)

            # global stress
            net_copy.load["p_mw"] *= 4.0

            # local variation
            mask_a = net_copy.load["bus"] == bus_a
            mask_b = net_copy.load["bus"] == bus_b

            net_copy.load.loc[mask_a, "p_mw"] *= fa / 4.0
            net_copy.load.loc[mask_b, "p_mw"] *= fb / 4.0

            try:
                pp.runpp(net_copy)
                landscape[i, j] = 1
            except Exception:
                landscape[i, j] = 0

    return factors, landscape
