# rift_controller_metrics.py (FINAL CLEAN FIX)

import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")


# --------------------------------------------------
# SAFE LOAD
# --------------------------------------------------

def safe_load(options):
    for f in options:
        path = os.path.join(BASE_DIR, f)
        if os.path.exists(path):
            print(f"✅ Loaded: {f}")
            return np.load(path)
    raise FileNotFoundError(f"❌ Missing files: {options}")


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_data():

    trajectory = safe_load([
        "states.npy",
        "trajectory.npy"
    ])

    rift = safe_load([
        "rift_extraction/rift_curve.npy",
        "rift_curve.npy"
    ])

    controlled = safe_load([
        "rift_extraction/final_controller_v7.npy"
    ])

    # 🔥 CRITICAL FIX → ALLES in 2D
    trajectory = trajectory[:, :2]
    controlled = controlled[:, :2]

    print("📐 Shapes:")
    print("trajectory:", trajectory.shape)
    print("controlled:", controlled.shape)
    print("rift:", rift.shape)

    return trajectory, controlled, rift


# --------------------------------------------------
# DISTANCE
# --------------------------------------------------

def nearest_rift_distance(points, rift):
    dists = []

    for p in points:
        d = np.linalg.norm(rift - p, axis=1)
        dists.append(np.min(d))

    return np.array(dists)


# --------------------------------------------------
# METRICS
# --------------------------------------------------

def compute_metrics(original, controlled, rift):

    orig_dist = nearest_rift_distance(original, rift)
    ctrl_dist = nearest_rift_distance(controlled, rift)

    metrics = {
        "mean_error_original": np.mean(orig_dist),
        "mean_error_controlled": np.mean(ctrl_dist),
        "improvement": np.mean(orig_dist) - np.mean(ctrl_dist),
        "max_error_controlled": np.max(ctrl_dist),
        "stability_std": np.std(ctrl_dist)
    }

    return metrics, orig_dist, ctrl_dist


# --------------------------------------------------
# PLOT
# --------------------------------------------------

def plot_metrics(orig_dist, ctrl_dist):

    plt.figure(figsize=(10, 4))

    plt.plot(orig_dist, label="original")
    plt.plot(ctrl_dist, label="controlled")

    plt.xlabel("time step")
    plt.ylabel("distance to rift")

    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "controller_metrics.png")
    os.makedirs(RIFT_DIR, exist_ok=True)

    plt.savefig(save_path)
    print(f"💾 Saved → {save_path}")

    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    trajectory, controlled, rift = load_data()

    metrics, orig_dist, ctrl_dist = compute_metrics(
        trajectory,
        controlled,
        rift
    )

    print("\n📊 CONTROLLER METRICS\n")

    for k, v in metrics.items():
        print(f"{k}: {v:.6f}")

    plot_metrics(orig_dist, ctrl_dist)

    print("\n🚀 Metrics analysis complete")


if __name__ == "__main__":
    main()
