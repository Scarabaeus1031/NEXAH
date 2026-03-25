import pandapower as pp
import copy
import numpy as np


def run_2d_stability_scan(
    net,
    bus_a,
    bus_b,
    base_load=3.8,     # 🔥 global stress (nahe collapse ~4.16)
    variation=0.3,     # 🔥 lokale Variation ±30%
    steps=40
):
    factors = np.linspace(1 - variation, 1 + variation, steps)
    landscape = np.zeros((steps, steps))

    for i, fa in enumerate(factors):
        for j, fb in enumerate(factors):

            net_copy = copy.deepcopy(net)

            # ===== GLOBAL LOAD =====
            net_copy.load["p_mw"] *= base_load

            # ===== LOCAL VARIATION =====
            mask_a = net_copy.load["bus"] == bus_a
            mask_b = net_copy.load["bus"] == bus_b

            net_copy.load.loc[mask_a, "p_mw"] *= fa
            net_copy.load.loc[mask_b, "p_mw"] *= fb

            try:
                pp.runpp(net_copy)
                landscape[i, j] = 1
            except Exception:
                landscape[i, j] = 0

    return factors, landscape
