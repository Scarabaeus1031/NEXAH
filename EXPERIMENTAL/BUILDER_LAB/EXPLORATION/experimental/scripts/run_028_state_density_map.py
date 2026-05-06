# ============================================================
# RUN 028 — STATE SPACE DENSITY / OCCUPATION FIELD
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.ndimage import gaussian_filter1d

# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------
OUT_DIR = Path(__file__).resolve().parent.parent / "outputs/run_028_density_map"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# SCENARIO (same as before)
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

    print("\n=== RUN 028 — STATE DENSITY MAP ===\n")

    t, V = make_scenario()
    V_s, dV = embedding(t, V)

    # --------------------------------------------------------
    # 2D HISTOGRAM (density field)
    # --------------------------------------------------------
    bins = 80

    H, xedges, yedges = np.histogram2d(
        V_s, dV,
        bins=bins
    )

    # normalize (optional)
    H = H / np.max(H)

    # --------------------------------------------------------
    # PLOT 1 — Density map
    # --------------------------------------------------------
    plt.figure(figsize=(8,6))

    plt.imshow(
        H.T,
        origin='lower',
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect='auto'
    )

    plt.colorbar(label="occupancy density")

    plt.xlabel("V")
    plt.ylabel("dV")
    plt.title("State Space Density (Occupation Field)")

    plt.savefig(OUT_DIR / "figure_01_density_map.png", dpi=150)
    plt.close()

    # --------------------------------------------------------
    # PLOT 2 — Overlay trajectory
    # --------------------------------------------------------
    plt.figure(figsize=(8,6))

    plt.imshow(
        H.T,
        origin='lower',
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect='auto',
        alpha=0.7
    )

    plt.plot(V_s, dV, color="white", linewidth=1)

    plt.xlabel("V")
    plt.ylabel("dV")
    plt.title("Density + Trajectory")

    plt.savefig(OUT_DIR / "figure_02_density_with_trajectory.png", dpi=150)
    plt.close()

    print(f"Saved to: {OUT_DIR}")
