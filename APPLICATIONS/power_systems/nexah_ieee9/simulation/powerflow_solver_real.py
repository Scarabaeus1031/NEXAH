import numpy as np

class RealPowerFlowSolver:
    def __init__(self, n=9):
        self.n = n

        # memory state (VERY IMPORTANT)
        self.prev_V = np.ones(n)
        self.instability = 0.0

    def step(self, lam, action=None):
        """
        Improved physical-like solver:
        - nonlinear voltage collapse (nose curve)
        - dynamic instability
        - action feedback
        """

        # ----------------------------------------
        # 1. BASE NONLINEAR LOAD MODEL
        # ----------------------------------------

        # classic "nose curve" approximation
        base = 1.0 - 0.12 * (lam - 1.0)**2

        # ----------------------------------------
        # 2. CONTROL EFFECT (from action)
        # ----------------------------------------

        control = 0.0
        if action == "STABILIZE":
            control = 0.01
        elif action == "PREEMPTIVE_STABILIZE":
            control = 0.02
        elif action == "REDUCE_LOAD":
            control = 0.04
        elif action == "EMERGENCY_SHED":
            control = 0.07

        # ----------------------------------------
        # 3. INSTABILITY BUILD-UP
        # ----------------------------------------

        # instability increases near collapse
        stress = max(0, lam - 1.5)
        self.instability += 0.02 * stress

        # decay if stabilized
        self.instability *= 0.98

        # ----------------------------------------
        # 4. VOLTAGE UPDATE (WITH MEMORY)
        # ----------------------------------------

        noise = np.random.normal(0, 0.01 + self.instability, self.n)

        V = (
            0.7 * self.prev_V +                      # inertia
            0.3 * (base + control) +                # target
            noise                                  # instability noise
        )

        # ----------------------------------------
        # 5. ANGLES
        # ----------------------------------------

        theta = np.random.uniform(-0.2, 0.2, self.n)

        # ----------------------------------------
        # 6. FAILURE CONDITION (SOFT COLLAPSE)
        # ----------------------------------------

        if np.mean(V) < 0.75 or self.instability > 0.25:
            converged = False
            V[:] = np.nan
        else:
            converged = True

        # update memory
        self.prev_V = V.copy()

        return {
            "V": V,
            "theta": theta,
            "converged": converged
        }
