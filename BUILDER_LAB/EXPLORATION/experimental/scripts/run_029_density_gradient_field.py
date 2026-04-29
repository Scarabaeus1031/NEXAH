# ============================================================
# RUN 029 — DENSITY GRADIENT FIELD
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.ndimage import gaussian_filter1d

# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------
OUT_DIR = Path(__file__).resolve().parent.parent / "outputs/run_029_density_gradient"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# SCENARIO
# ------------------------------------------------------------
def make_scenario(n=500):
    t = np.linspace(0, 100, n)
    V = 1.0 - 0.002 * t - 0.0005 * t**2

    V += 0.015 * np.exp((t - 16) / 4.0) * (t < 25)
    V += 0.01 * np.sin(0.8 * t) * (t < 25)

    return t, V

# ------------------------------------------------------------
# EMBEDDING
# ------------------------------------------------------------
def embedding(t, V):
    V_s = gaussian_filter1d(V, sigma=2)
    dV = gaussian_filter1d(np.gradient(V_s, t), sigma=2)
    return V_s, dV

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == "__main__":

    print("\n=== RUN 029 — DENSITY GRADIENT FIELD ===\n")

    t, V = make_scenario()
    V_s, dV = embedding(t, V)

    bins = 80

    H, xedges, yedges = np.histogram2d(V_s, dV, bins=bins)
    H = H / np.max(H)

    # grid centers
    X = (xedges[:-1] + xedges[1:]) / 2
    Y = (yedges[:-1] + yedges[1:]) / 2
    X, Y = np.meshgrid(X, Y)

    # gradient
    dHy, dHx = np.gradient(H.T)

    # --------------------------------------------------------
    # PLOT
    # --------------------------------------------------------
    plt.figure(figsize=(8,6))

    plt.imshow(
        H.T,
        origin='lower',
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        alpha=0.6
    )

    plt.quiver(
        X, Y,
        dHx, dHy,
        color='black',
        scale=20
    )

    plt.title("Density Gradient Field")
    plt.xlabel("V")
    plt.ylabel("dV")

    plt.savefig(OUT_DIR / "figure_01_density_gradient_field.png", dpi=150)
    plt.close()

    print(f"Saved to: {OUT_DIR}")
