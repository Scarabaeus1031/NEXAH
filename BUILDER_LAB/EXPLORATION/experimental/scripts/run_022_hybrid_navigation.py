# ============================================================
# RUN 022 — HYBRID NAVIGATION (COUPLING + NAVIGATOR)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# import your modules
from spiral_coupling.spiral_coupling_kernel import SpiralCouplingKernel
from nexah_navigation_kernel_v1 import nexah_kernel_step


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
OUT_DIR = Path("outputs/run_022_hybrid_navigation")
OUT_DIR.mkdir(parents=True, exist_ok=True)

steps = 600


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == "__main__":
    print("\n=== RUN 022 — HYBRID NAVIGATION ===\n")

    # init systems
    coupling = SpiralCouplingKernel(coupling_strength=0.85)

    x, y = -6.0, -5.0
    prev_x, prev_y = x, y

    traj = []
    coherence_list = []
    drift_list = []
    collapse_list = []

    for t in range(steps):

        # ----------------------------------------------------
        # 1. get direction from coupling
        # ----------------------------------------------------
        result = coupling.step()
        flow = result["flow_direction"]
        coherence = result["coherence"]

        # project flow into 2D (simple)
        flow_x, flow_y = flow[0], flow[1]

        # ----------------------------------------------------
        # 2. navigator step (with external direction)
        # ----------------------------------------------------
        new_x, new_y, ch, sw, sig = nexah_kernel_step(
            x + 0.2 * flow_x,
            y + 0.2 * flow_y,
            prev_x,
            prev_y,
            t
        )

        traj.append((new_x, new_y))
        coherence_list.append(coherence)
        drift_list.append(sig["drift"])
        collapse_list.append(sig["collapse"])

        prev_x, prev_y = x, y
        x, y = new_x, new_y

    traj = np.array(traj)

    print("Final position:", traj[-1])
    print("Mean coherence:", np.mean(coherence_list))

    # --------------------------------------------------------
    # PLOT 1 — trajectory
    # --------------------------------------------------------
    plt.figure(figsize=(8,6))
    plt.plot(traj[:,0], traj[:,1], linewidth=1.5)
    plt.title("Hybrid Navigation Trajectory")
    plt.grid(alpha=0.3)

    plt.savefig(OUT_DIR / "figure_01_trajectory.png", dpi=150)
    plt.close()

    # --------------------------------------------------------
    # PLOT 2 — coherence
    # --------------------------------------------------------
    plt.figure(figsize=(8,4))
    plt.plot(coherence_list)
    plt.title("Coupling Coherence")

    plt.savefig(OUT_DIR / "figure_02_coherence.png", dpi=150)
    plt.close()

    # --------------------------------------------------------
    # PLOT 3 — drift + collapse
    # --------------------------------------------------------
    plt.figure(figsize=(8,4))
    plt.plot(drift_list, label="drift")
    plt.plot(collapse_list, label="collapse")
    plt.legend()

    plt.savefig(OUT_DIR / "figure_03_signals.png", dpi=150)
    plt.close()

    print(f"\nSaved to: {OUT_DIR}")
