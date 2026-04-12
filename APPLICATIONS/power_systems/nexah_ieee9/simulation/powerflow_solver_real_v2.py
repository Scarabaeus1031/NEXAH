import numpy as np
import pandapower as pp
import pandapower.networks as pn


class RealPowerFlowSolverV2:
    def __init__(self):
        """
        Real AC power flow solver using pandapower IEEE9 network.
        """

        # base network
        self.base_net = pn.case9()

    def _apply_lambda(self, net, lam):
        """
        Scale loads by lambda.
        """
        net.load["p_mw"] = net.load["p_mw"] * lam
        net.load["q_mvar"] = net.load["q_mvar"] * lam

    def _apply_action(self, net, action):
        """
        Map NEXAH actions → physical interventions.
        """

        if action == "STABILIZE":
            # small voltage support via generators
            if "gen" in net:
                net.gen["vm_pu"] += 0.01

        elif action == "PREEMPTIVE_STABILIZE":
            if "gen" in net:
                net.gen["vm_pu"] += 0.02

        elif action == "REDUCE_LOAD":
            net.load["p_mw"] *= 0.95
            net.load["q_mvar"] *= 0.95

        elif action == "EMERGENCY_SHED":
            net.load["p_mw"] *= 0.85
            net.load["q_mvar"] *= 0.85

        # NONE → no change

    def step(self, lam, action=None):
        """
        One simulation step:
        λ → modify loads → apply action → run AC power flow
        """

        # ----------------------------------------
        # 1. fresh copy of network (IMPORTANT)
        # ----------------------------------------
        net = self.base_net.deepcopy()

        # ----------------------------------------
        # 2. apply load scaling
        # ----------------------------------------
        self._apply_lambda(net, lam)

        # ----------------------------------------
        # 3. apply control action
        # ----------------------------------------
        if action is not None:
            self._apply_action(net, action)

        # ----------------------------------------
        # 4. run AC power flow
        # ----------------------------------------
        try:
            pp.runpp(net, init="auto", max_iteration=20)

            V = net.res_bus.vm_pu.values
            theta = net.res_bus.va_degree.values

            converged = True

        except Exception:
            # power flow failed → collapse
            n = len(net.bus)
            V = np.full(n, np.nan)
            theta = np.full(n, np.nan)
            converged = False

        return {
            "V": V,
            "theta": theta,
            "converged": converged
        }
