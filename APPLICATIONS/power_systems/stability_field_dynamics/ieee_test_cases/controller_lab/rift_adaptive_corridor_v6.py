# rift_adaptive_corridor_v6.py

import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")


def load_data():
    trajectory = None

    for name in ["trajectory.npy", "states.npy"]:
        path = os.path.join(BASE_DIR, name)
        if os.path.exists(path):
            trajectory = np.load(path)
            print(f"✅ Loaded trajectory: {name}")
            break

    if trajectory is None:
        raise FileNotFoundError("❌ No trajectory file found")

    rift_path = os.path.join(RIFT_DIR, "rift_curve.npy")
    if not os.path.exists(rift_path):
        raise FileNotFoundError("❌ No rift_curve.npy found")

    rift = np.load(rift_path)
    print("✅ Loaded rift")

    return trajectory, rift


def estimate_trajectory_layer(traj):
    pc2 = traj[:, 1]

    # robuster Mittelwert (kein Drift-Effekt)
    center = np.median(pc2)
    spread = np.std(pc2)

    print(f"🎯 Trajectory layer: {center:.4f} ± {spread:.4f}")

    return center, spread


def nearest_rift_point(p, rift):
    dists = np.linalg.norm(rift - p, axis=1)
    return rift[np.argmin(dists)]


def adaptive_corridor_control(trajectory, rift,
                              gain_rift=0.2,
                              gain_layer=0.25):

    controlled = trajectory.copy()

    layer_center, _ = estimate_trajectory_layer(trajectory)

    for t in range(len(controlled)):

        current = controlled[t]

        # --- rift pull (wie V3/V4)
        rift_target = nearest_rift_point(current, rift)
        rift_corr = gain_rift * (rift_target - current)

        # --- layer lock (NEU)
        layer_target = np.array([current[0], layer_center])
        layer_corr = gain_layer * (layer_target - current)

        # combine
        correction = rift_corr + layer_corr

        correction = np.clip(correction, -0.05, 0.05)

        controlled[t] += correction

    return controlled, layer_center


def plot_result(original, controlled, rift, layer_center):
    plt.figure(figsize=(10, 6))

    plt.plot(original[:, 0], original[:, 1],
             label="original", color="green")

    plt.plot(rift[:, 0], rift[:, 1],
             label="rift", color="cyan")

    plt.plot(controlled[:, 0], controlled[:, 1],
             label="adaptive corridor v6", color="gold")

    plt.axhline(layer_center, linestyle="--",
                color="magenta", label="trajectory layer")

    plt.scatter(original[-1, 0], original[-1, 1],
                color="red", label="orig end")

    plt.scatter(controlled[-1, 0], controlled[-1, 1],
                color="orange", label="controlled end")

    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "adaptive_corridor_v6.png")
    plt.savefig(save_path, dpi=150)
    print(f"💾 Saved → {save_path}")

    plt.close()


def main():
    trajectory, rift = load_data()

    trajectory = trajectory[:, :2]

    controlled, layer_center = adaptive_corridor_control(
        trajectory, rift
    )

    plot_result(trajectory, controlled, rift, layer_center)

    print("🚀 Adaptive Corridor V6 complete")


if __name__ == "__main__":
    main()
