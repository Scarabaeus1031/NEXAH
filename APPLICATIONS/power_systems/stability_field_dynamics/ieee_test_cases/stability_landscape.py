import pandapower as pp
import copy
import numpy as np


def run_2d_stability_scan(
    net,
    load_bus,
    gen_idx,
    base_load=3.8,
    steps=40,
    outage_line=0
):
    # 🔥 KRITISCHER BEREICH
    factors = np.linspace(3.5, 4.5, steps)
    landscape = np.zeros((steps, steps))

    for i, lf in enumerate(factors):
        for j, gf in enumerate(factors):

            net_copy = copy.deepcopy(net)

            # ===== LINE OUTAGE =====
            net_copy.line.drop(outage_line, inplace=True)

            # ===== GLOBAL LOAD =====
            net_copy.load["p_mw"] *= base_load

            # ===== LOCAL LOAD =====
            mask = net_copy.load["bus"] == load_bus
            net_copy.load.loc[mask, "p_mw"] *= lf / base_load

            # ❌ Generator scaling raus (wichtig)
            # net_copy.gen.loc[gen_idx, "p_mw"] *= gf

            try:
                pp.runpp(net_copy)
                landscape[i, j] = 1
            except:
                landscape[i, j] = 0

    return factors, landscape
