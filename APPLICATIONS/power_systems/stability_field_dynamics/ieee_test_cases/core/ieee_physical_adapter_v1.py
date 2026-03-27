# ieee_physical_adapter.py

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
        theta (np.ndarray): phase angles
        C (np.ndarray): field intensity (voltage deviation)
        loops (np.ndarray): proxy for structural dynamics
    """

    net = _load_case(case)

    # --------------------------------------------------------
    # APPLY LOAD SCALING (REAL PHYSICAL INPUT)
    # --------------------------------------------------------
    net.load["p_mw"] *= load_scale
    net.load["q_mvar"] *= load_scale

    # --------------------------------------------------------
    # RUN POWER FLOW
    # --------------------------------------------------------
    pp.runpp(net)

    # --------------------------------------------------------
    # EXTRACT PHYSICAL VARIABLES
    # --------------------------------------------------------
    V = net.res_bus["vm_pu"].values          # voltage magnitude
    theta = net.res_bus["va_degree"].values  # phase angle (degrees)

    # convert to radians
    theta = np.deg2rad(theta)

    # --------------------------------------------------------
    # NEXAH MAPPING
    # --------------------------------------------------------

    # C = deviation from nominal voltage
    C = 1.0 - V

    # loops proxy (simple but meaningful)
    loops = _compute_loops(theta, net)

    return theta, C, loops


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def _load_case(case: str):
    if case == "ieee14":
        return pn.case14()
    elif case == "ieee9":
        return pn.case9()
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

    # power flow magnitude as weighting
    p_flow = net.res_line["p_from_mw"].values

    # accumulate per node
    loop_signal = np.zeros_like(theta)

    for i in range(len(from_bus)):
        f = from_bus[i]
        t = to_bus[i]

        val = abs(theta_diff[i]) * abs(p_flow[i])

        loop_signal[f] += val
        loop_signal[t] += val

    # normalize
    if np.max(loop_signal) > 0:
        loop_signal = loop_signal / np.max(loop_signal)

    return loop_signal


# ------------------------------------------------------------
# QUICK TEST
# ------------------------------------------------------------

if __name__ == "__main__":
    theta, C, loops = ieee_to_nexah("ieee14", load_scale=1.5)

    print("\n--- IEEE → NEXAH ---")
    print("theta:", theta[:5])
    print("C:", C[:5])
    print("loops:", loops[:5])
