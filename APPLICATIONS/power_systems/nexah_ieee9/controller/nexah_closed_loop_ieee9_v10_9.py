import numpy as np
from nexah_ieee9.simulation.powerflow_solver_real_v3 import RealPowerFlowSolverV3


class NEXAHControllerV10_9:
    def __init__(self):
        self.solver = RealPowerFlowSolverV3()

        self.lam = 0.60
        self.lam_max = 1.50

        # dynamics
        self.prev_lam = self.lam
        self.stuck_counter = 0

    def compute_risk(self, vmin):
        if np.isnan(vmin):
            return 1.0
        return max(0.0, (1.0 - vmin))

    def step(self, step_id):
        result = self.solver.step(self.lam)

        vmin = result["vmin"]
        risk = self.compute_risk(vmin)

        # -----------------------------
        # Δλ baseline (field movement)
        # -----------------------------
        dlam = 0.04 * (1.0 - risk)

        # -----------------------------
        # EXPLOITATION vs EXPLORATION
        # -----------------------------
        if risk < 0.03:
            # system is safe → push harder
            dlam += 0.02

        elif risk > 0.06:
            # too risky → slow down
            dlam -= 0.03

        # -----------------------------
        # STUCK DETECTION
        # -----------------------------
        if abs(self.lam - self.prev_lam) < 1e-4:
            self.stuck_counter += 1
        else:
            self.stuck_counter = 0

        # -----------------------------
        # ESCAPE MECHANISM 🔥
        # -----------------------------
        if self.stuck_counter > 5:
            print("⚡ ESCAPE MODE ACTIVATED")
            dlam += 0.05
            self.stuck_counter = 0

        # -----------------------------
        # COLLAPSE DETECTION
        # -----------------------------
        if not result["converged"] or np.isnan(vmin):
            print("💥 COLLAPSE DETECTED → emergency reduce")
            dlam = -0.10

        # -----------------------------
        # UPDATE λ
        # -----------------------------
        new_lam = self.lam + dlam
        new_lam = max(0.5, min(self.lam_max, new_lam))

        # -----------------------------
        # LOAD SHEDDING (only if needed)
        # -----------------------------
        shed = 0.0
        if risk > 0.04:
            shed = min(0.05, risk)
            new_lam *= (1 - shed)

        # -----------------------------
        # LOGGING
        # -----------------------------
        print(
            f"[STEP {step_id}] λ={self.lam:.4f} → {new_lam:.4f} | "
            f"risk={risk:.4f} vmin={vmin:.4f} "
            f"dλ={dlam:.4f} shed={shed:.4f}"
        )

        # shift state
        self.prev_lam = self.lam
        self.lam = new_lam


if __name__ == "__main__":
    controller = NEXAHControllerV10_9()

    for i in range(200):
        controller.step(i)
