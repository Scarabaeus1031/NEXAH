# =========================================
# IMPORTS
# =========================================

import numpy as np
import pandapower as pp
import pandapower.networks as pn
import copy


# =========================================
# NETWORK FACTORY  ← MUSS OBEN STEHEN
# =========================================

def load_network(case_name="ieee9"):

    if case_name == "ieee9":
        return pn.case9()
    elif case_name == "ieee14":
        return pn.case14()
    elif case_name == "ieee30":
        return pn.case30()
    elif case_name == "ieee57":
        return pn.case57()
    elif case_name == "ieee118":
        return pn.case118()
    elif case_name == "ieee300":
        return pn.case300()
    elif case_name == "ieee1354":
        return pn.case1354pegase()
    elif case_name == "ieee9241":
        return pn.case9241pegase()
    else:
        raise ValueError(f"Unknown case: {case_name}")


# =========================================
# SOLVER
# =========================================

class RealPowerFlowSolverGeneric:

    def __init__(self, case_name="ieee9"):

        self.case_name = case_name
        self.base_net = load_network(case_name)

        self.instability = 0.0

    def step(self, lam, action=None):

        net = copy.deepcopy(self.base_net)

        net.load["p_mw"] *= lam
        net.load["q_mvar"] *= lam

        if action == "STABILIZE":
            net.load["p_mw"] *= 0.99
        elif action == "PREEMPTIVE_STABILIZE":
            net.load["p_mw"] *= 0.97
        elif action == "REDUCE_LOAD":
            net.load["p_mw"] *= 0.94
        elif action == "EMERGENCY_SHED":
            net.load["p_mw"] *= 0.90

        try:
            pp.runpp(
                net,
                algorithm="nr",
                max_iteration=100,
                tolerance_mva=1e-5,
                init="auto"
            )
            converged = net.converged
        except Exception:
            converged = False

        if not converged or net.res_bus.empty:
            V = np.full(len(net.bus), np.nan)
            theta = np.full(len(net.bus), np.nan)
        else:
            V = net.res_bus["vm_pu"].values
            theta = net.res_bus["va_degree"].values

            V = V - 0.005 * (lam - 1.0)
            V = V + np.random.normal(0, 0.001, len(V))

        return {
            "V": V,
            "theta": theta,
            "converged": converged
        }
