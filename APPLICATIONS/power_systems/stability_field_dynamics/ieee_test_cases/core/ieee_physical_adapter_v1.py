# ieee_physical_adapter_v2.py

import numpy as np

try:
    import pandapower as pp
    import pandapower.networks as pn
except ImportError:
    raise ImportError(
        "pandapower is required. Install via: pip install pandapower"
    )


# ------------------------------------------------------------
# CORE ADAPTER
# ------------------------------------------------------------

def ieee_to_nexah(case: str = "ieee14", load_scale: float = 1.0):
    """
    Convert IEEE power system state → NEXAH variables

    Returns:
        theta (np.ndarray): phase angles (rad, centered)
        C (np.ndarray): field intensity (voltage deviation)
        loops (np.ndarray): proxy for structural dynamics
        converged (bool): whether power flow converged
    """

    net = _load_case(case)

    # --------------------------------------------------------
    # APPLY LOAD SCALING
    # --------------------------------------------------------
    net.load["p_mw"] *= load_scale
    net.load["q_mvar"] *= load_scale

    # --------------------------------------------------------
    # RUN POWER FLOW (robust)
    # --------------------------------------------------------
    try:
        pp.runpp(
            net,
            algorithm="nr",
            max_iteration=30,
            tolerance_mva=1e-6,
            init="auto"
        )
        converged = True

    except Exception:
        converged = False

    # --------------------------------------------------------
    # FALLBACK (COLLAPSE REGIME)
    # --------------------------------------------------------
    if not converged:
        n = len(net.bus)

        theta = np.zeros(n)
        C = np.ones(n) * 1.0   # strong deviation = collapse signature
        loops = np.zeros(n)

        return theta, C, loops, False

    # --------------------------------------------------------
    # EXTRACT PHYSICAL VARIABLES
    # --------------------------------------------------------
    V = net.res_bus["vm_pu"].values
    theta = net.res_bus["va_degree"].values

    # convert to radians
    theta = np.deg2rad(theta)

    # --------------------------------------------------------
    # NORMALIZE PHASE (important for geometry)
    # --------------------------------------------------------
    theta = theta - np.mean(theta)

    # --------------------------------------------------------
    # NEXAH MAPPING
    # --------------------------------------------------------

    # voltage deviation
    C = 1.0 - V

    # clip for stability
    C = np.clip(C, -1.0, 1.0)

    loops = _compute_loops(theta, net)

    return theta, C, loops, True


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def _load_case(case: str):
    if case == "ieee9":
        return pn.case9()
    elif case == "ieee14":
        return pn.case14()
    elif case == "ieee30":
        return pn.case30()
    elif case == "ieee57":
        return pn.case57()   # 🔥 NEW
    else:
        raise ValueError(f"Unknown case: {case}")

def _compute_loops(theta, net):
    """
    Approximate loop dynamics from branch flows and phase differences
    """

    if len(net.res_line) == 0:
        return np.zeros_like(theta)

    from_bus = net.line["from_bus"].values
    to_bus = net.line["to_bus"].values

    theta_diff = theta[from_bus] - theta[to_bus]
    p_flow = net.res_line["p_from_mw"].values

    loop_signal = np.zeros_like(theta)

    for i in range(len(from_bus)):
        f = from_bus[i]
        t = to_bus[i]

        # slightly stabilized signal
        val = np.sqrt(abs(theta_diff[i])) * abs(p_flow[i])

        loop_signal[f] += val
        loop_signal[t] += val

    max_val = np.max(loop_signal)
    if max_val > 0:
        loop_signal = loop_signal / max_val

    return loop_signal


# ------------------------------------------------------------
# QUICK TEST
# ------------------------------------------------------------

if __name__ == "__main__":
    theta, C, loops, converged = ieee_to_nexah("ieee30", load_scale=1.5)

    print("\n--- IEEE → NEXAH ---")
    print("converged:", converged)
    print("theta:", theta[:5])
    print("C:", C[:5])
    print("loops:", loops[:5])
