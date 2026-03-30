# rift_controller_metrics.py (FIXED + ROBUST)

import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"


def safe_load(filename_options):
    for fname in filename_options:
        path = os.path.join(BASE_DIR, fname)
        if os.path.exists(path):
            print(f"✅ Loaded: {fname}")
            return np.load(path)
    raise FileNotFoundError(f"❌ None of these files found: {filename_options}")


def load_data():
    trajectory = safe_load([
        "states.npy",
        "trajectory.npy"
    ])

    rift = safe_load([
        "rift_curve.npy",
        "rift_curve_smoothed.npy",
        "rift_extraction/rift_curve.npy"
    ])

    return trajectory, rift


def nearest_rift_distance(points, rift):
    dists = []
    for p in points:
        dist = np.min(np.linalg.norm(rift - p, axis=1))
        dists.append(dist)
    return np.array(dists)


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


def plot_metrics(orig_dist, ctrl_dist):
    plt.figure(figsize=(10, 4))
    plt.plot(orig_dist, label="original distance")
    plt.plot(ctrl_dist, label="controlled distance")
    plt.xlabel("time step")
    plt.ylabel("distance to rift")
    plt.legend()
    plt.title("Controller Performance")
    plt.grid(True)
    plt.tight_layout()

    save_path = os.path.join(BASE_DIR, "rift_extraction/controller_metrics.png")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    print(f"💾 Saved → {save_path}")
    plt.close()


def main():
    trajectory, rift = load_data()

    # 🔥 IMPORTANT: hier richtigen Controller laden!
    # Wenn du V7 gespeichert hast → hier eintragen

    try:
        controlled = np.load(os.path.join(BASE_DIR, "rift_extraction/final_controller_v7.npy"))
        print("✅ Loaded controlled trajectory (V7)")
    except:
        print("⚠️ No saved controlled trajectory found → using original (placeholder)")
        controlled = trajectory.copy()

    metrics, orig_dist, ctrl_dist = compute_metrics(trajectory, controlled, rift)

    print("\n📊 CONTROLLER METRICS\n")
    for k, v in metrics.items():
        print(f"{k}: {v:.6f}")

    plot_metrics(orig_dist, ctrl_dist)

    print("\n🚀 Metrics analysis complete")


if __name__ == "__main__":
    main()
