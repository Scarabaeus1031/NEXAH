import numpy as np
import pandapower as pp
import pandapower.networks as pn
import copy


class RealPowerFlowSolverV3:
    def __init__(self):
        """
        Real AC power flow solver using pandapower IEEE9 network.
        Improved version with:
        - clean lambda scaling
        - line loading extraction
        - robust outputs for controller
        """

        # base network
        self.base_net = pn.case9()

        # store base loads (IMPORTANT)
        self.base_p = self.base_net.load["p_mw"].values.copy()
        self.base_q = self.base_net.load["q_mvar"].values.copy()

    def _apply_lambda(self, net, lam):
        """
        Scale loads relative to BASE case (not cumulative).
        """
        net.load["p_mw"] = self.base_p * lam
        net.load["q_mvar"] = self.base_q * lam

    def _apply_action(self, net, action):
        """
        Map NEXAH actions → physical interventions.
        """

        if action == "STABILIZE":
            if hasattr(net, "gen") and len(net.gen) > 0:
                net.gen["vm_pu"] = net.gen["vm_pu"] + 0.01

        elif action == "PREEMPTIVE_STABILIZE":
            if hasattr(net, "gen") and len(net.gen) > 0:
                net.gen["vm_pu"] = net.gen["vm_pu"] + 0.02

        elif action == "REDUCE_LOAD":
            net.load["p_mw"] *= 0.95
            net.load["q_mvar"] *= 0.95

        elif action == "EMERGENCY_SHED":
            net.load["p_mw"] *= 0.85
            net.load["q_mvar"] *= 0.85

    def step(self, lam, action=None):
        """
        One simulation step:
        λ → load scaling → action → AC power flow
        Returns physically meaningful signals.
        """

        # ----------------------------------------
        # 1. fresh copy
        # ----------------------------------------
        net = copy.deepcopy(self.base_net)

        # ----------------------------------------
        # 2. lambda scaling
        # ----------------------------------------
        self._apply_lambda(net, lam)

        # ----------------------------------------
        # 3. control action
        # ----------------------------------------
        if action is not None:
            self._apply_action(net, action)

        # ----------------------------------------
        # 4. AC power flow
        # ----------------------------------------
        try:
            pp.runpp(net, init="auto", max_iteration=20)

            V = net.res_bus.vm_pu.values
            theta = net.res_bus.va_degree.values

            # --- NEW: physical observables ---
            vmin = float(np.min(V))

            if hasattr(net, "res_line") and len(net.res_line) > 0:
                line_loading = float(np.max(net.res_line.loading_percent))
            else:
                line_loading = 0.0

            converged = True

        except Exception:
            # collapse
            n = len(net.bus)

            V = np.full(n, np.nan)
            theta = np.full(n, np.nan)

            vmin = np.nan
            line_loading = np.nan

            converged = False

        return {
            "V": V,
            "theta": theta,
            "vmin": vmin,
            "line_loading": line_loading,
            "converged": converged
        }
