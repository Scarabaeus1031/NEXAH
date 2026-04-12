class RealPowerFlowSolverGeneric:

    def __init__(self, case_name="ieee9"):

        self.case_name = case_name
        self.base_net = load_network(case_name)

        self.instability = 0.0

    def step(self, lam, action=None):

        net = copy.deepcopy(self.base_net)

        # ----------------------------------------
        # 1. LOAD SCALING (sehr vorsichtig)
        # ----------------------------------------

        net.load["p_mw"] *= lam
        net.load["q_mvar"] *= lam

        # ----------------------------------------
        # 2. CONTROL (sanft)
        # ----------------------------------------

        if action == "STABILIZE":
            net.load["p_mw"] *= 0.99

        elif action == "PREEMPTIVE_STABILIZE":
            net.load["p_mw"] *= 0.97

        elif action == "REDUCE_LOAD":
            net.load["p_mw"] *= 0.94

        elif action == "EMERGENCY_SHED":
            net.load["p_mw"] *= 0.90

        # ----------------------------------------
        # 3. RUN POWER FLOW (robuster)
        # ----------------------------------------

        try:
            pp.runpp(
                net,
                algorithm="nr",
                max_iteration=100,   # 🔥 mehr Iterationen
                tolerance_mva=1e-5,  # 🔥 entspannter
                init="auto"
            )
            converged = net.converged

        except Exception:
            converged = False

        # ----------------------------------------
        # 4. STATE
        # ----------------------------------------

        if not converged or net.res_bus.empty:

            V = np.full(len(net.bus), np.nan)
            theta = np.full(len(net.bus), np.nan)

        else:
            V = net.res_bus["vm_pu"].values
            theta = net.res_bus["va_degree"].values

            # 🔥 NUR MINIMALER DRIFT
            V = V - 0.005 * (lam - 1.0)

            # 🔥 leichte Noise (wichtig)
            V = V + np.random.normal(0, 0.001, len(V))

        return {
            "V": V,
            "theta": theta,
            "converged": converged
        }
