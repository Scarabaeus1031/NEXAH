import pandapower as pp
import copy
import numpy as np


def run_2d_stability_scan(
    net,
    load_bus,
    gen_idx,
    base_load=3.8,
    steps=40
):
    factors = np.linspace(0.8, 1.3, steps)
    landscape = np.zeros((steps, steps))

    for i, lf in enumerate(factors):
        for j, gf in enumerate(factors):

            net_copy = copy.deepcopy(net)

            # ===== GLOBAL LOAD =====
            net_copy.load["p_mw"] *= base_load

            # ===== LOCAL LOAD VARIATION =====
            mask = net_copy.load["bus"] == load_bus
            net_copy.load.loc[mask, "p_mw"] *= lf

            # ===== GENERATOR VARIATION =====
            net_copy.gen.loc[gen_idx, "p_mw"] *= gf

            try:
                pp.runpp(net_copy)
                landscape[i, j] = 1
            except Exception:
                landscape[i, j] = 0

    return factors, landscape
