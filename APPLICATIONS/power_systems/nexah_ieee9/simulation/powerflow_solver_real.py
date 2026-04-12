# =========================================
# REAL POWERFLOW SOLVER (IEEE9 via pandapower)
# =========================================

import numpy as np
import pandapower as pp
import pandapower.networks as pn


# =========================================
# INIT NETWORK
# =========================================

def create_base_network():
    """
    Load IEEE 9-bus test system
    """
    net = pn.case9()
    return net


# =========================================
# APPLY LOAD SCALING
# =========================================

def apply_load_scaling(net, lam):
    """
    Scale all loads by lambda
    """
    net.load["p_mw"] *= lam
    net.load["q_mvar"] *= lam


# =========================================
# APPLY CONTROL ACTION
# =========================================

def apply_action(net, action):
    """
    Map intervention actions to physical modifications
    """

    if action is None or action == "INIT":
        return

    if action == "STABILIZE":
        # small voltage support
        net.gen["vm_pu"] *= 1.01

    elif action == "PREEMPTIVE_STABILIZE":
        net.gen["vm_pu"] *= 1.02

    elif action == "REDUCE_LOAD":
        net.load["p_mw"] *= 0.95
        net.load["q_mvar"] *= 0.95

    elif action == "EMERGENCY_SHED":
        net.load["p_mw"] *= 0.85
        net.load["q_mvar"] *= 0.85

    elif action == "NONE":
        pass


# =========================================
# MAIN SOLVER
# =========================================

def powerflow_solver_real(lam, action=None):
    """
    Real AC power flow using pandapower
    """

    try:
        # fresh network each step
        net = create_base_network()

        # apply load increase
        apply_load_scaling(net, lam)

        # apply control action
        apply_action(net, action)

        # run AC power flow
        pp.runpp(net, init="flat", tolerance_mva=1e-6)

        # extract results
        V = net.res_bus.vm_pu.values
        theta = net.res_bus.va_degree.values

        converged = True

    except Exception as e:
        # solver failed → collapse
        n = 9
        V = np.full(n, np.nan)
        theta = np.full(n, np.nan)
        converged = False

    return {
        "V": V,
        "theta": theta,
        "converged": converged
    }
