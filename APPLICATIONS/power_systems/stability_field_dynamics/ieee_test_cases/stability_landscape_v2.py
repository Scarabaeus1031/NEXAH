import pandapower as pp
import copy
import numpy as np


def run_2d_stability_scan_v2(
    net,
    load_bus,
    base_load=3.8,
    min_factor=3.5,
    max_factor=4.5,
    steps=50,
    outage_line=None
):
    """
    2D Stability Scan (Load vs Load)
    → bewusst ohne Generator Scaling (wichtig!)
    """

    factors = np.linspace(min_factor, max_factor, steps)
    landscape = np.zeros((steps, steps))

    for i, fa in enumerate(factors):
        for j, fb in enumerate(factors):

            net_copy = copy.deepcopy(net)

            # ===== OPTIONAL: LINE OUTAGE =====
            if outage_line is not None:
                if outage_line in net_copy.line.index:
                    net_copy.line.drop(outage_line, inplace=True)

            # ===== GLOBAL LOAD LEVEL =====
            net_copy.load["p_mw"] *= base_load

            # ===== LOCAL LOAD VARIATION =====
            mask = net_copy.load["bus"] == load_bus

            # 👉 zwei Richtungen = dein "90° Kreuz"
            net_copy.load.loc[mask, "p_mw"] *= fa / base_load
            net_copy.load.loc[~mask, "p_mw"] *= fb / base_load

            try:
                pp.runpp(net_copy)

                # 🔥 wichtig: CONTINUOUS VALUE statt 0/1
                v_min = net_copy.res_bus["vm_pu"].min()
                landscape[i, j] = v_min

            except:
                landscape[i, j] = 0.0

    return factors, factors, landscape
