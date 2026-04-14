import numpy as np
import pandas as pd

from nexah_ieee9.simulation.powerflow_solver_real_v3 import RealPowerFlowSolverV3


def detect_critical_lambda(df):
    lambdas = df["lambda"].values
    risk = df["risk"].values

    drisk = np.gradient(risk, lambdas)
    d2risk = np.gradient(drisk, lambdas)

    for i in range(len(lambdas)):
        if drisk[i] > 0.1 or d2risk[i] > 0.5:
            return lambdas[i]

    return None


def load_scan_data():
    return pd.read_csv("nexah_stability_surface_v11_1.csv")


def run_controller():
    solver = RealPowerFlowSolverV3()

    df = load_scan_data()
    critical_lambda = detect_critical_lambda(df)

    if critical_lambda is None:
        print("❌ No critical zone found → aborting")
        return

    # Sicherheitsabstand
    safety_margin = 0.02
    target_lambda = critical_lambda - safety_margin

    print("\n--- NEXAH NAVIGATION CONTROLLER (v11_2) ---\n")
    print(f"🎯 Target λ ≈ {target_lambda:.3f} (critical at {critical_lambda:.3f})\n")

    lam = 0.6
    max_steps = 100

    for step in range(max_steps):
        res = solver.step(lam)

        vmin = res["vmin"]
        converged = res["converged"]

        if not converged or np.isnan(vmin):
            print(f"[STEP {step}] ❌ COLLAPSE at λ={lam:.4f}")
            break

        error = target_lambda - lam

        # sanfte Navigation (kein Overshoot)
        dlam = np.clip(0.3 * error, -0.05, 0.05)

        lam_next = lam + dlam

        print(
            f"[STEP {step}] λ={lam:.4f} → {lam_next:.4f} | "
            f"target={target_lambda:.4f} | dλ={dlam:.4f}"
        )

        lam = lam_next

        # Stop wenn nah genug
        if abs(error) < 0.002:
            print(f"\n✅ Target reached safely at λ ≈ {lam:.4f}")
            break


if __name__ == "__main__":
    run_controller()
