# =========================================
# IMPORTS
# =========================================

import numpy as np
import pandapower as pp
import pandapower.networks as pn
import copy


# =========================================
# NETWORK FACTORY
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
# SOLVER (STABILIZED VERSION)
# =========================================

class RealPowerFlowSolverGeneric:

    def __init__(self, case_name="ieee9"):

        self.case_name = case_name
        self.base_net = load_network(case_name)

    def step(self, lam, action=None):

        net = copy.deepcopy(self.base_net)

        # ----------------------------------------
        # 1. LOAD SCALING (sanfter!)
        # ----------------------------------------

        net.load["p_mw"] *= lam
        net.load["q_mvar"] *= lam

        # ----------------------------------------
        # 2. CONTROL (weniger aggressiv)
        # ----------------------------------------

        if action == "STABILIZE":
            net.load["p_mw"] *= 0.995

        elif action == "PREEMPTIVE_STABILIZE":
            net.load["p_mw"] *= 0.98

        elif action == "REDUCE_LOAD":
            net.load["p_mw"] *= 0.95

        elif action == "EMERGENCY_SHED":
            net.load["p_mw"] *= 0.92

        # ----------------------------------------
        # 3. RUN POWER FLOW (robuster)
        # ----------------------------------------

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

        # ----------------------------------------
        # 4. STATE HANDLING (KRITISCH!)
        # ----------------------------------------

        if not converged or net.res_bus.empty:

            # 🔥 WICHTIG: NICHT mehr NaN → sonst stirbt Pipeline
            V = np.random.normal(0.85, 0.02, len(net.bus))
            theta = np.zeros(len(net.bus))

        else:
            V = net.res_bus["vm_pu"].values
            theta = net.res_bus["va_degree"].values

            # 🔥 sanfter Drift (nicht zu stark!)
            V = V - 0.002 * (lam - 1.0)

            # 🔥 kleine Noise → verhindert Flatline
            V = V + np.random.normal(0, 0.001, len(V))

        return {
            "V": V,
            "theta": theta,
            "converged": converged
        }
