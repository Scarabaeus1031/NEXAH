from .ieee_loader import load_ieee14
from .stability_scan import run_stability_scan
from .run_2d_stability_scan_v2 import run_2d_stability_scan_v2

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

    # Collapse detection
    collapse = next((f for f, s in results if not s), None)
    if collapse:
        plt.axvline(x=collapse, linestyle="--", label=f"Collapse ~ {collapse:.2f}")
        plt.legend()

    plt.show()


# =========================
# 2D LANDSCAPE PLOT
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

    # Boundary nur wenn sinnvoll
    if np.unique(landscape).size > 1:
        plt.contour(
            load_factors,
            gen_factors,
            landscape,
            levels=[0.5],
            colors="red",
            linewidths=1
        )
        plt.colorbar(label="Stability (1=stable, 0=unstable)")

    plt.xlabel("Load Scaling")
    plt.ylabel("Generation Scaling")
    plt.title("IEEE 14-bus Stability Landscape (Load vs Generation)")

    plt.show()


# =========================
# MAIN
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

            # 🔥 Load hoch
            net_copy.load["p_mw"] *= lf

            # 🔥 Generation runter (IMBALANCE!)
            net_copy.gen["p_mw"] *= gf

            try:
                pp.runpp(net_copy)
                landscape[i, j] = 1
            except:
                landscape[i, j] = 0

    return load_factors, gen_factors, landscape

    # ===== 2D LANDSCAPE (NEW) =====
    print("\n--- 2D Stability Landscape (Load vs Generation) ---")

    load_factors, gen_factors, landscape = run_2d_stability_scan_v2(
        net,
        min_load=3.5,
        max_load=4.5,
        min_gen=0.8,
        max_gen=1.2,
        steps=50
    )

    plot_landscape(load_factors, gen_factors, landscape)


if __name__ == "__main__":
    main()
