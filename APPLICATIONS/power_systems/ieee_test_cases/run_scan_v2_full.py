from .ieee_loader import load_ieee14
from .stability_scan import run_stability_scan

import pandapower as pp
import copy
import numpy as np
import matplotlib.pyplot as plt


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
# 2D LANDSCAPE (FIXED)
# =========================
def run_2d_stability_scan_v2(
    net,
    min_load=3.5,
    max_load=4.5,
    min_gen=0.5,
    max_gen=1.0,
    steps=40
):
    load_factors = np.linspace(min_load, max_load, steps)
    gen_factors = np.linspace(min_gen, max_gen, steps)

    landscape = np.zeros((steps, steps))

    for i, lf in enumerate(load_factors):
        for j, gf in enumerate(gen_factors):

            net_copy = copy.deepcopy(net)

            # 🔥 DESTABILISIERUNG
            net_copy.load["p_mw"] *= lf

            # 🔥 IMBALANCE (wichtiger Fix!)
            net_copy.gen["p_mw"] *= gf

            try:
                pp.runpp(net_copy)
                landscape[i, j] = 1
            except Exception:
                landscape[i, j] = 0

    return load_factors, gen_factors, landscape


# =========================
# 2D PLOT (ROBUST)
# =========================
def plot_landscape(load_factors, gen_factors, landscape):
    plt.figure()

    plt.imshow(
        landscape,
        origin="lower",
        extent=[load_factors[0], load_factors[-1],
                gen_factors[0], gen_factors[-1]],
        aspect="auto",
        cmap="viridis"
    )

    unique_vals = np.unique(landscape)

    if unique_vals.size > 1:
        plt.contour(
            load_factors,
            gen_factors,
            landscape,
            levels=[0.5],
            colors="red",
            linewidths=1
        )
        plt.colorbar(label="Stability (1=stable, 0=unstable)")
    else:
        print("⚠️ Landscape has no variation (all stable or all unstable)")

    plt.xlabel("Load Scaling (destabilizing)")
    plt.ylabel("Generation Scaling (stabilizing ↓)")
    plt.title("IEEE 14-bus Stability Landscape (Load vs Generation Imbalance)")

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

    # ===== 2D =====
    print("\n--- 2D Stability Landscape (IMBALANCE) ---")

    load_factors, gen_factors, landscape = run_2d_stability_scan_v2(
        net,
        min_load=3.5,
        max_load=4.5,
        min_gen=0.5,   # 🔥 wichtig
        max_gen=1.0,
        steps=50
    )

    plot_landscape(load_factors, gen_factors, landscape)


if __name__ == "__main__":
    main()
