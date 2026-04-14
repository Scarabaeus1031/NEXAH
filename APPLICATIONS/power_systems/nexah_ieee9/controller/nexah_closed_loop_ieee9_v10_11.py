import numpy as np
from nexah_ieee9.simulation.powerflow_solver_real_v3 import RealPowerFlowSolverV3


def run_controller():
    solver = RealPowerFlowSolverV3()

    lam = 0.6

    # Zielbereich (wichtig!)
    vmin_target = 0.955
    tolerance = 0.002

    max_steps = 150

    print("\n--- NEXAH SMART CONTROLLER (v10_11) ---\n")

    for step in range(max_steps):

        res = solver.step(lam)

        vmin = res["vmin"]
        converged = res["converged"]

        if not converged or np.isnan(vmin):
            print(f"[STEP {step}] ❌ COLLAPSE at λ={lam:.4f}")
            break

        # --- SMART CONTROL LOGIC ---

        error = vmin - vmin_target

        # proportional step size
        dlam = 0.0

        if abs(error) < tolerance:
            # stay stable
            dlam = 0.0

        elif error > 0:
            # system stable → increase load
            dlam = min(0.05, 0.5 * error)

        else:
            # system too stressed → reduce load
            dlam = max(-0.05, 0.5 * error)

        lam_next = lam + dlam

        print(
            f"[STEP {step}] λ={lam:.4f} → {lam_next:.4f} | "
            f"vmin={vmin:.4f} | error={error:.4f} | dλ={dlam:.4f}"
        )

        lam = lam_next


if __name__ == "__main__":
    run_controller()
