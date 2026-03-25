import pandapower as pp
import copy
import numpy as np


def run_2d_stability_scan_v3(
    net,
    min_load=3.5,
    max_load=4.5,
    min_gen=0.5,
    max_gen=1.2,
    steps=40
):
    """
    Improved 2D stability scan with intentional imbalance.

    Key idea:
    - Load is globally increased (destabilizing)
    - Only PART of generation is scaled (creates imbalance)
    - Returns continuous voltage field (not binary!)
    """

    load_factors = np.linspace(min_load, max_load, steps)
    gen_factors = np.linspace(min_gen, max_gen, steps)

    landscape = np.zeros((steps, steps))

    for i, lf in enumerate(load_factors):
        for j, gf in enumerate(gen_factors):

            net_copy = copy.deepcopy(net)

            # =========================
            # 🔥 GLOBAL LOAD PUSH
            # =========================
            net_copy.load["p_mw"] *= lf

            # =========================
            # 🔥 PARTIAL GENERATION SCALING
            # =========================
            # Only first few generators react → imbalance
            gen_idx = net_copy.gen.index[:2]

            net_copy.gen.loc[gen_idx, "p_mw"] *= gf

            # =========================
            # RUN POWER FLOW
            # =========================
            try:
                pp.runpp(net_copy)

                # 🔥 continuous metric (CRUCIAL!)
                min_voltage = net_copy.res_bus["vm_pu"].min()

                landscape[i, j] = min_voltage

            except Exception:
                # collapse
                landscape[i, j] = 0.0

    return load_factors, gen_factors, landscape
