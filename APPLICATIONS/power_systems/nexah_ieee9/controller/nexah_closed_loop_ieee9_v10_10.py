import numpy as np
import pandas as pd
from nexah_ieee9.simulation.powerflow_solver_real_v3 import RealPowerFlowSolverV3


def run_scan():
    solver = RealPowerFlowSolverV3()

    # λ range (fein genug!)
    lambdas = np.linspace(0.5, 1.5, 100)

    results = []

    print("\n--- NEXAH SCAN MODE ---\n")

    for lam in lambdas:
        res = solver.step(lam)

        vmin = res["vmin"]
        loading = res["line_loading"]
        converged = res["converged"]

        # simple risk proxy
        if np.isnan(vmin):
            risk = 1.0
        else:
            risk = max(0.0, 1.0 - vmin)

        print(
            f"λ={lam:.3f} | vmin={vmin:.4f} | "
            f"loading={loading:.2f} | risk={risk:.4f} | conv={converged}"
        )

        results.append({
            "lambda": lam,
            "vmin": vmin,
            "loading": loading,
            "risk": risk,
            "converged": converged
        })

        # optional: stop at collapse
        if not converged:
            print("\n⚠️ COLLAPSE DETECTED — stopping scan\n")
            break

    # save results
    df = pd.DataFrame(results)
    df.to_csv("nexah_ieee9_scan.csv", index=False)

    print("\n✅ Scan complete → saved to nexah_ieee9_scan.csv\n")


if __name__ == "__main__":
    run_scan()
