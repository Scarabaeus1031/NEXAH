from .ieee_loader import load_ieee14
from .stability_scan import run_stability_scan
from .stability_landscape import run_2d_stability_scan
from .sensitivity_analysis import run_sensitivity_analysis

import matplotlib.pyplot as plt
import numpy as np


# =========================
# 1D PLOT
# =========================
def plot_results(results):
    factors = [f for f, s in results]
    stability = [1 if s else 0 for f, s in results]

    plt.figure()
    plt.plot(factors, stability, marker="o")
    plt.xlabel("Load Factor")
    plt.ylabel("Stability (1=stable, 0=unstable)")
    plt.title("IEEE 14-bus Stability Scan")
    plt.grid()

    collapse = next((f for f, s in results if not s), None)
    if collapse:
        plt.axvline(x=collapse, linestyle="--", label=f"Collapse ~ {collapse:.2f}")
        plt.legend()

    plt.show()


# =========================
# 2D LANDSCAPE PLOT
# =========================
def plot_landscape(factors, landscape):
    plt.figure()

    plt.imshow(
        landscape,
        origin="lower",
        extent=[factors[0], factors[-1], factors[0], factors[-1]],
        aspect="auto",
        cmap="viridis"
    )

    if np.unique(landscape).size > 1:
        plt.contour(
            landscape,
            levels=[0.5],
            colors="red",
            linewidths=1,
            extent=[factors[0], factors[-1], factors[0], factors[-1]]
        )
        plt.colorbar(label="Stability (1=stable, 0=unstable)")

    plt.xlabel("Load factor (Load Bus)")
    plt.ylabel("Generation factor")
    plt.title("IEEE 14-bus Stability Landscape")
    plt.show()


# =========================
# MAIN
# =========================
def main():
    net = load_ieee14()

    # ===== 1D SCAN =====
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

    # ===== 2D LANDSCAPE =====
    print("\n--- 2D Stability Landscape ---")

    load_buses = net.load["bus"].values

    # 🔥 DEFINIERT (das hat dir gefehlt)
    load_bus = int(load_buses[2])
    gen_idx = 0

    factors, landscape = run_2d_stability_scan(
        net,
        load_bus=load_bus,
        gen_idx=gen_idx,
        base_load=3.8,
        steps=50
    )

    plot_landscape(factors, landscape)

    # ===== SENSITIVITY =====
    print("\n--- Sensitivity Analysis ---")

    sensitivity = run_sensitivity_analysis(net)

    for bus, collapse in sensitivity.items():
        print(f"Bus {bus} → collapse at {collapse:.2f}")


if __name__ == "__main__":
    main()
