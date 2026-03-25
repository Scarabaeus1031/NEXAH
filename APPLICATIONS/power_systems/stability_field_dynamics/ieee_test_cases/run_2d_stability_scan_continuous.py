import pandapower as pp
import numpy as np
import copy


def run_2d_stability_scan_continuous(
    net,
    min_load=3.5,
    max_load=4.5,
    min_q=0.5,
    max_q=1.5,
    steps=40
):
    """
    Continuous stability landscape using voltage as stability metric.

    Instead of binary stable/unstable:
        returns min voltage per state (continuous field)

    Parameters:
        net        : pandapower network
        min_load   : minimum load scaling (P)
        max_load   : maximum load scaling (P)
        min_q      : minimum reactive scaling (Q)
        max_q      : maximum reactive scaling (Q)
        steps      : grid resolution

    Returns:
        load_factors : array
        q_factors    : array
        landscape    : 2D array (voltage field)
    """

    load_factors = np.linspace(min_load, max_load, steps)
    q_factors = np.linspace(min_q, max_q, steps)

    landscape = np.zeros((steps, steps))

    for i, lf in enumerate(load_factors):
        for j, qf in enumerate(q_factors):

            net_copy = copy.deepcopy(net)

            # 🔥 ACTIVE POWER scaling (P)
            net_copy.load["p_mw"] *= lf

            # 🔥 REACTIVE POWER scaling (Q)
            if "q_mvar" in net_copy.load.columns:
                net_copy.load["q_mvar"] *= qf

            try:
                pp.runpp(net_copy, max_iteration=20)

                # ✅ CONTINUOUS METRIC
                min_vm = net_copy.res_bus["vm_pu"].min()

                # clamp for visualization stability
                if np.isnan(min_vm):
                    landscape[i, j] = 0
                else:
                    landscape[i, j] = min_vm

            except Exception:
                # solver fail = collapse
                landscape[i, j] = 0

    return load_factors, q_factors, landscape
