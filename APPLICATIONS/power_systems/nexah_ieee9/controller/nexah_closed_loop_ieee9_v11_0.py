import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.nexah_ieee9.simulation.powerflow_solver_real_v3 import RealPowerFlowSolverV3


def compute_risk(vmin, loading):
    return max(0, 0.97 - vmin) + max(0, (loading - 80) / 100)


def run_scan():
    solver = RealPowerFlowSolverV3()

    lambdas = np.linspace(0.5, 1.5, 100)

    data = []

    print("\n--- NEXAH STABILITY SURFACE SCAN (v11_0) ---\n")

    for lam in lambdas:
        result = solver.step(lam)

        vmin = result["vmin"]
        loading = result["line_loading"]
        converged = result["converged"]

        risk = compute_risk(vmin, loading) if converged else np.nan

        print(f"λ={lam:.3f} | vmin={vmin:.4f} | loading={loading:.2f} | risk={risk:.4f} | conv={converged}")

        data.append({
            "lambda": lam,
            "vmin": vmin,
            "loading": loading,
            "risk": risk,
            "converged": converged
        })

    df = pd.DataFrame(data)

    # -----------------------------------
    # SAVE CSV
    # -----------------------------------
    df.to_csv("nexah_stability_surface.csv", index=False)
    print("\n✅ CSV saved: nexah_stability_surface.csv")

    # -----------------------------------
    # PLOT
    # -----------------------------------
    plt.figure()

    plt.plot(df["lambda"], df["vmin"], label="vmin")
    plt.plot(df["lambda"], df["loading"] / 100.0, label="loading (scaled)")
    plt.plot(df["lambda"], df["risk"], label="risk")

    plt.axhline(0.95, linestyle="--")  # voltage stability line

    plt.xlabel("Lambda (Load Scaling)")
    plt.ylabel("Values")
    plt.title("NEXAH Stability Surface (IEEE9)")
    plt.legend()

    plt.savefig("nexah_stability_surface.png")
    print("🖼️ Plot saved: nexah_stability_surface.png")

    plt.show()


if __name__ == "__main__":
    run_scan()
