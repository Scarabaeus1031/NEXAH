# 🧭 NEXAH Minimal Demo
# Goal: Trajectory + Field + Regime + Separatrix (+ optional Risk)

import numpy as np
import matplotlib.pyplot as plt

# 1. Trajectory
from ENGINE.analysis.navigation_level61_multi_loop_engine import simulate_trajectory

# 2. Flow Field
from ENGINE.analysis.flow_field_analysis import compute_flow_field

# 3. Regime Classification
from ENGINE.analysis.stability_landscape_generator import classify_regime_grid

# 4. Separatrix
from ENGINE.analysis.stability_basin_map import detect_separatrix

# 5. Optional Risk
from ENGINE.analysis.stability_gradient_field import compute_risk_field


def main():

    print("🚀 Running NEXAH Demo...")

    # --------------------------------------------------
    # 1. Generate trajectory (Lorenz or internal system)
    # --------------------------------------------------
    trajectory = simulate_trajectory()

    print("✔ Trajectory generated")

    # --------------------------------------------------
    # 2. Compute Flow Field
    # --------------------------------------------------
    field = compute_flow_field(trajectory)

    print("✔ Flow field computed")

    # --------------------------------------------------
    # 3. Classify regimes
    # --------------------------------------------------
    regime_grid = classify_regime_grid(field)

    print("✔ Regime zones computed")

    # --------------------------------------------------
    # 4. Detect separatrix
    # --------------------------------------------------
    separatrix = detect_separatrix(regime_grid)

    print("✔ Separatrix extracted")

    # --------------------------------------------------
    # 5. Optional risk layer
    # --------------------------------------------------
    try:
        risk = compute_risk_field(field)
        print("✔ Risk field computed")
    except Exception:
        risk = None
        print("⚠ Risk field not available")

    # --------------------------------------------------
    # SIMPLE VISUALIZATION (minimal)
    # --------------------------------------------------
    plt.figure(figsize=(8, 6))

    # Trajectory
    traj = np.array(trajectory)
    plt.plot(traj[:, 0], traj[:, 1], linewidth=0.5, label="Trajectory")

    # Optional: separatrix overlay (if 2D compatible)
    if separatrix is not None:
        try:
            plt.scatter(separatrix[:, 0], separatrix[:, 1], s=1, label="Separatrix")
        except:
            pass

    plt.title("NEXAH Demo — Trajectory + Structure")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
