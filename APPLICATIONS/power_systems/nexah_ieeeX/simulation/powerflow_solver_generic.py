# =========================================
# GENERIC POWER FLOW SOLVER (NEXAH v2)
# =========================================

import numpy as np
import pandapower as pp
import pandapower.networks as pn
import copy


# =========================================
# NETWORK FACTORY
# =========================================

def load_network(case_name="ieee9"):
    """
    Load standard IEEE test systems.
    """

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
# GENERIC SOLVER
# =========================================

class RealPowerFlowSolverGeneric:
    """
    Generic pandapower-based solver with NEXAH control interface.
    Enhanced for large-grid dynamics.
    """

    def __init__(self, case_name="ieee9"):

        self.case_name = case_name
        self.base_net = load_network(case_name)

        # memory
        self.instability = 0.0

    # =========================================
    # STEP FUNCTION
    # =========================================

    def step(self, lam, action=None):

        # ----------------------------------------
        # 1. COPY BASE NETWORK
        # ----------------------------------------

        net = copy.deepcopy(self.base_net)

        # ----------------------------------------
        # 2. APPLY LOAD SCALING (λ)
        # ----------------------------------------

        net.load["p_mw"] *= lam
        net.load["q_mvar"] *= lam

        # ----------------------------------------
        # 3. APPLY CONTROL ACTIONS
        # ----------------------------------------

        if action == "STABILIZE":
            net.load["p_mw"] *= 0.98

        elif action == "PREEMPTIVE_STABILIZE":
            net.load["p_mw"] *= 0.95

        elif action == "REDUCE_LOAD":
            net.load["p_mw"] *= 0.90

        elif action == "EMERGENCY_SHED":
            net.load["p_mw"] *= 0.80

        # ----------------------------------------
        # 4. RUN POWER FLOW
        # ----------------------------------------

        try:
            pp.runpp(
                net,
                algorithm="nr",
                max_iteration=50,
                tolerance_mva=1e-6,
                init="auto"
            )
            converged = net.converged

        except Exception:
            converged = False

        # ----------------------------------------
        # 5. EXTRACT STATE
        # ----------------------------------------

        if not converged or net.res_bus.empty:
            V = np.full(len(net.bus), np.nan)
            theta = np.full(len(net.bus), np.nan)

            # 🔥 stronger instability injection
            self.instability += 0.05

        else:
            V = net.res_bus["vm_pu"].values
            theta = net.res_bus["va_degree"].values

            # ------------------------------------
            # 🔥 STRUCTURAL PERTURBATION (CRITICAL)
            # ------------------------------------
            # large grids are too smooth → inject micro-noise
            V = V + np.random.normal(0, 0.002, len(V))

            # ------------------------------------
            # 🔥 ENHANCED INSTABILITY MODEL
            # ------------------------------------

            vmin = np.min(V)

            # shift threshold upward → earlier sensitivity
            stress = max(0, 0.95 - vmin)

            # stronger accumulation
            self.instability += 0.05 * stress

            # slow decay
            self.instability *= 0.98

        # ----------------------------------------
        # 6. FAILURE CONDITION (SOFT)
        # ----------------------------------------

        if self.instability > 0.3:
            converged = False
            V[:] = np.nan

        # ----------------------------------------
        # OUTPUT
        # ----------------------------------------

        return {
            "V": V,
            "theta": theta,
            "converged": converged
        }
