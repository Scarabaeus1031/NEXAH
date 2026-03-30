# rift_controller_metrics.py

import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"

def load_data():
    trajectory = np.load(os.path.join(BASE_DIR, "states.npy"))
    rift = np.load(os.path.join(BASE_DIR, "rift_curve.npy"))
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

    # 👉 hier kannst du später verschiedene Controller laden
    # aktuell: wir nehmen die letzten Punkte als "controlled"
    # → oder du ersetzt das durch echte controller outputs

    controlled = np.load(".../final_controller_v7.npy")

    metrics, orig_dist, ctrl_dist = compute_metrics(trajectory, controlled, rift)

    print("\n📊 CONTROLLER METRICS\n")
    for k, v in metrics.items():
        print(f"{k}: {v:.6f}")

    plot_metrics(orig_dist, ctrl_dist)

    print("\n🚀 Metrics analysis complete")


if __name__ == "__main__":
    main()
