import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from nexah_ieee9.simulation.powerflow_solver_real_v3 import RealPowerFlowSolverV3


def compute_risk(vmin, loading):
    return max(0, 0.97 - vmin) + max(0, (loading - 80) / 100)


def detect_critical_regions(df):
    lambdas = df["lambda"].values
    risk = df["risk"].values

    # 1st derivative (gradient)
    drisk = np.gradient(risk, lambdas)

    # 2nd derivative (curvature)
    d2risk = np.gradient(drisk, lambdas)

    # thresholds (tunable!)
    grad_threshold = 0.1
    curvature_threshold = 0.5

    critical_points = []

    for i in range(len(lambdas)):
        if drisk[i] > grad_threshold or d2risk[i] > curvature_threshold:
            critical_points.append(i)

    return critical_points, drisk, d2risk


def run_scan():
    solver = RealPowerFlowSolverV3()

    lambdas = np.linspace(0.5, 1.5, 100)

    data = []

    print("\n--- NEXAH STABILITY SURFACE + CRITICAL DETECTION (v11_1) ---\n")

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
    # CRITICAL DETECTION
    # -----------------------------------
    critical_points, drisk, d2risk = detect_critical_regions(df)

    if critical_points:
        first_critical = critical_points[0]
        print(f"\n⚠️ CRITICAL REGION starts at λ ≈ {df['lambda'][first_critical]:.3f}")
    else:
        print("\n✅ No critical region detected")

    # -----------------------------------
    # SAVE CSV
    # -----------------------------------
    df["drisk"] = drisk
    df["d2risk"] = d2risk

    df.to_csv("nexah_stability_surface_v11_1.csv", index=False)
    print("✅ CSV saved: nexah_stability_surface_v11_1.csv")

    # -----------------------------------
    # PLOT
    # -----------------------------------
    plt.figure()

    plt.plot(df["lambda"], df["vmin"], label="vmin")
    plt.plot(df["lambda"], df["loading"] / 100.0, label="loading (scaled)")
    plt.plot(df["lambda"], df["risk"], label="risk")

    # Critical markers
    for idx in critical_points:
        plt.axvline(df["lambda"][idx], linestyle=":", alpha=0.3)

    plt.axhline(0.95, linestyle="--")

    plt.xlabel("Lambda (Load Scaling)")
    plt.ylabel("Values")
    plt.title("NEXAH Stability Surface + Critical Zones")
    plt.legend()

    plt.savefig("nexah_stability_surface_v11_1.png")
    print("🖼️ Plot saved: nexah_stability_surface_v11_1.png")

    plt.show()


if __name__ == "__main__":
    run_scan()
