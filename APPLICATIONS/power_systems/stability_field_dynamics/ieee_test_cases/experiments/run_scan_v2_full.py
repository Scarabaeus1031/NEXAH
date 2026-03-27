from .ieee_loader import load_ieee14
from .stability_scan import run_stability_scan
from .run_2d_stability_scan_continuous import run_2d_stability_scan_continuous

import matplotlib.pyplot as plt
import numpy as np


# =========================
# 1D STABILITY PLOT
# =========================
def plot_results(results):
    factors = [f for f, s in results]
    stability = [1 if s else 0 for f, s in results]

    plt.figure()
    plt.plot(factors, stability, marker="o")

    plt.xlabel("Load Factor")
    plt.ylabel("Stability (1=stable, 0=unstable)")
    plt.title("IEEE 14-bus Stability Scan (1D)")
    plt.grid()

    collapse = next((f for f, s in results if not s), None)
    if collapse:
        plt.axvline(x=collapse, linestyle="--", label=f"Collapse ~ {collapse:.2f}")
        plt.legend()

    plt.show()


# =========================
# 2D CONTINUOUS LANDSCAPE PLOT
# =========================
def plot_landscape(load_factors, q_factors, landscape):
    plt.figure()

    im = plt.imshow(
        landscape,
        origin="lower",
        extent=[load_factors[0], load_factors[-1],
                q_factors[0], q_factors[-1]],
        aspect="auto",
        cmap="viridis"
    )

    # 🔥 Jetzt immer Colorbar, weil continuous
    plt.colorbar(im, label="Min Voltage (pu)")

    # 🔥 Critical contour (Voltage collapse region)
    plt.contour(
        load_factors,
        q_factors,
        landscape,
        levels=[0.7],  # typische collapse zone
        colors="red",
        linewidths=1
    )

    plt.xlabel("Load Scaling (P)")
    plt.ylabel("Reactive Scaling (Q)")
    plt.title("IEEE 14-bus Stability Landscape (Continuous Voltage Field)")

    plt.show()


# =========================
# MAIN
# =========================
def main():
    net = load_ieee14()

    # ===== 1D =====
    print("\n--- 1D Stability Scan ---")

    results = run_stability_scan(
        net,
        min_factor=3.8,
        max_factor=4.4,
        steps=40
    )

    for factor, stable in results:
        status = "Stable" if stable else "Unstable"
        print(f"Load factor: {factor:.2f} → {status}")

    plot_results(results)

    # ===== 2D CONTINUOUS =====
    print("\n--- 2D Stability Landscape (Continuous) ---")

    load_factors, q_factors, landscape = run_2d_stability_scan_continuous(
        net,
        min_load=3.5,
        max_load=4.5,
        min_q=0.5,
        max_q=1.5,
        steps=50
    )

    plot_landscape(load_factors, q_factors, landscape)


if __name__ == "__main__":
    main()
