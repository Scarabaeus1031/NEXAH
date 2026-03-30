# rift_field_metrics.py

import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")


# --------------------------------------------------
# LOAD
# --------------------------------------------------

def safe_load(options):
    for f in options:
        path = os.path.join(BASE_DIR, f)
        if os.path.exists(path):
            print(f"✅ Loaded: {f}")
            return np.load(path)
    raise FileNotFoundError(f"❌ Missing files: {options}")


def load_data():
    trajectory = safe_load([
        "states.npy",
        "trajectory.npy"
    ])

    controlled = safe_load([
        "rift_extraction/final_controller_v9_1.npy",
        "rift_extraction/final_controller_v9.npy",
        "rift_extraction/final_controller_v8_1.npy",
        "rift_extraction/final_controller_v7.npy"
    ])

    trajectory = trajectory[:, :2]
    controlled = controlled[:, :2]

    return trajectory, controlled


# --------------------------------------------------
# METRICS
# --------------------------------------------------

def estimate_layer(traj):
    pc2 = traj[:, 1]
    return np.median(pc2)


def compute_layer_stability(traj, layer):
    return np.abs(traj[:, 1] - layer)


def compute_smoothness(traj):
    velocity = np.diff(traj, axis=0)
    accel = np.diff(velocity, axis=0)
    curvature = np.linalg.norm(accel, axis=1)
    return curvature


def compute_flow_alignment(traj):
    velocity = np.diff(traj, axis=0)
    directions = velocity / (np.linalg.norm(velocity, axis=1, keepdims=True) + 1e-8)

    # alignment = cos(angle between consecutive directions)
    dots = np.sum(directions[:-1] * directions[1:], axis=1)
    return dots  # closer to 1 = smoother direction


def compute_energy(traj):
    velocity = np.diff(traj, axis=0)
    return np.linalg.norm(velocity, axis=1)


# --------------------------------------------------
# MAIN METRIC FUNCTION
# --------------------------------------------------

def compute_field_metrics(original, controlled):

    layer = estimate_layer(original)

    orig_layer_err = compute_layer_stability(original, layer)
    ctrl_layer_err = compute_layer_stability(controlled, layer)

    orig_smooth = compute_smoothness(original)
    ctrl_smooth = compute_smoothness(controlled)

    orig_align = compute_flow_alignment(original)
    ctrl_align = compute_flow_alignment(controlled)

    orig_energy = compute_energy(original)
    ctrl_energy = compute_energy(controlled)

    metrics = {
        "layer_error_original": np.mean(orig_layer_err),
        "layer_error_controlled": np.mean(ctrl_layer_err),

        "smoothness_original": np.mean(orig_smooth),
        "smoothness_controlled": np.mean(ctrl_smooth),

        "flow_alignment_original": np.mean(orig_align),
        "flow_alignment_controlled": np.mean(ctrl_align),

        "energy_original": np.mean(orig_energy),
        "energy_controlled": np.mean(ctrl_energy),
    }

    return metrics


# --------------------------------------------------
# PLOT
# --------------------------------------------------

def plot_metrics(orig, ctrl):

    plt.figure(figsize=(10, 4))

    plt.plot(orig[:, 1], label="original (PC2)")
    plt.plot(ctrl[:, 1], label="controlled (PC2)")

    plt.xlabel("time step")
    plt.ylabel("layer position (PC2)")

    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "field_metrics.png")
    os.makedirs(RIFT_DIR, exist_ok=True)

    plt.savefig(save_path)
    print(f"💾 Saved → {save_path}")

    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    trajectory, controlled = load_data()

    metrics = compute_field_metrics(trajectory, controlled)

    print("\n📊 FIELD METRICS\n")

    for k, v in metrics.items():
        print(f"{k}: {v:.6f}")

    plot_metrics(trajectory, controlled)

    print("\n🚀 Field metrics complete")


if __name__ == "__main__":
    main()
