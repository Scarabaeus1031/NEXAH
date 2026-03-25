import pandapower as pp
import copy
import numpy as np

def run_2d_stability_scan(
    net,
    bus_a,
    bus_b,
    min_factor=3.8,
    max_factor=4.3,
    steps=40
):
    factors = np.linspace(min_factor, max_factor, steps)
    landscape = np.zeros((steps, steps))

    for i, fa in enumerate(factors):
        for j, fb in enumerate(factors):

            net_copy = copy.deepcopy(net)

            # 🔥 WICHTIG: globales Stress-Level
            net_copy.load["p_mw"] *= 3.5

            # 🔥 lokale Variation
            mask_a = net_copy.load["bus"] == bus_a
            mask_b = net_copy.load["bus"] == bus_b

            net_copy.load.loc[mask_a, "p_mw"] *= fa / 3.5
            net_copy.load.loc[mask_b, "p_mw"] *= fb / 3.5

            try:
                pp.runpp(net_copy)
                landscape[i, j] = 1
            except Exception:
                landscape[i, j] = 0

    return factors, landscape
