import numpy as np
import os
import matplotlib.pyplot as plt

# =============================
# CONFIG
# =============================

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")

ALPHA = 0.15   # pull toward rift (normal)
BETA = 0.7     # original dynamics
GAMMA = 0.25   # tangent flow strength

# =============================
# LOAD DATA
# =============================

def load_data():
    trajectory = np.load(os.path.join(BASE_DIR, "trajectory.npy"))

    possible_names = ["rift_curve.npy", "rift.npy", "rift_points.npy"]
    rift_curve = None

    for name in possible_names:
        path = os.path.join(RIFT_DIR, name)
        if os.path.exists(path):
            rift_curve = np.load(path)
            print(f"✅ Loaded rift file: {name}")
            break

    if rift_curve is None:
        raise FileNotFoundError("❌ No rift file found")

    print(f"✅ Trajectory loaded: {trajectory.shape}")
    print(f"✅ Rift curve loaded: {rift_curve.shape}")

    return trajectory, rift_curve


# =============================
# HELPERS
# =============================

def find_nearest_rift_point(point, rift_curve):
    dists = np.linalg.norm(rift_curve - point, axis=1)
    idx = np.argmin(dists)
    return rift_curve[idx], idx


def compute_tangent(rift_curve, idx):
    if idx == 0:
        tangent = rift_curve[1] - rift_curve[0]
    elif idx == len(rift_curve) - 1:
        tangent = rift_curve[-1] - rift_curve[-2]
    else:
        tangent = rift_curve[idx + 1] - rift_curve[idx - 1]

    norm = np.linalg.norm(tangent)
    if norm > 0:
        tangent = tangent / norm

    return tangent


# =============================
# CONTROL WITH TANGENT FLOW
# =============================

def apply_rift_tangent_control(trajectory, rift_curve):
    controlled = [trajectory[0]]

    for i in range(1, len(trajectory)):
        current = controlled[-1]
        original_step = trajectory[i] - trajectory[i - 1]

        nearest, idx = find_nearest_rift_point(current, rift_curve)

        # Normal (toward rift)
        normal_vec = nearest - current

        # Tangent (along rift)
        tangent_vec = compute_tangent(rift_curve, idx)

        # Combine
        new_step = (
            BETA * original_step
            + ALPHA * normal_vec
            + GAMMA * tangent_vec
        )

        new_point = current + new_step
        controlled.append(new_point)

    return np.array(controlled)


# =============================
# VISUALIZATION
# =============================

def plot_results(trajectory, rift_curve, controlled):
    plt.figure(figsize=(10, 6))

    plt.plot(trajectory[:, 0], trajectory[:, 1], color="green", label="original")
    plt.plot(rift_curve[:, 0], rift_curve[:, 1], color="cyan", linewidth=2, label="rift")
    plt.plot(controlled[:, 0], controlled[:, 1], color="yellow", label="controlled")

    plt.scatter(trajectory[-1, 0], trajectory[-1, 1], color="red", label="original end")
    plt.scatter(controlled[-1, 0], controlled[-1, 1], color="orange", label="controlled end")

    plt.title("Rift Tangent Control")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "rift_tangent_control.png")
    plt.savefig(save_path)
    print(f"💾 Saved → {save_path}")

    plt.show()


def plot_distance_comparison(trajectory, controlled, rift_curve):
    def compute_distance(traj):
        dists = []
        for p in traj:
            d = np.min(np.linalg.norm(rift_curve - p, axis=1))
            dists.append(d)
        return np.array(dists)

    d_orig = compute_distance(trajectory)
    d_ctrl = compute_distance(controlled)

    plt.figure(figsize=(10, 4))
    plt.plot(d_orig, label="original")
    plt.plot(d_ctrl, label="controlled")

    plt.title("Distance to Rift: Original vs Tangent-Controlled")
    plt.xlabel("step")
    plt.ylabel("distance")
    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "rift_tangent_distance.png")
    plt.savefig(save_path)
    print(f"💾 Saved → {save_path}")

    plt.show()


# =============================
# MAIN
# =============================

def main():
    trajectory, rift_curve = load_data()

    controlled = apply_rift_tangent_control(trajectory, rift_curve)

    plot_results(trajectory, rift_curve, controlled)
    plot_distance_comparison(trajectory, controlled, rift_curve)

    np.save(os.path.join(RIFT_DIR, "trajectory_controlled_tangent.npy"), controlled)
    print("💾 Controlled trajectory saved")

    print("🚀 Tangent control complete")


if __name__ == "__main__":
    main()
