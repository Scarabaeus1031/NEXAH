import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# =============================
# CONFIG
# =============================

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")

ALPHA = 0.15
BETA = 0.7
GAMMA = 0.25

# =============================
# LOAD DATA (ROBUST)
# =============================

def load_data():
    trajectory = None

    # Try direct trajectory
    traj_path = os.path.join(BASE_DIR, "trajectory.npy")
    if os.path.exists(traj_path):
        trajectory = np.load(traj_path)
        print("✅ Loaded trajectory.npy")

    # Fallback: states.npy → PCA
    else:
        states_path = os.path.join(BASE_DIR, "states.npy")
        if not os.path.exists(states_path):
            raise FileNotFoundError("❌ No trajectory or states.npy found")

        states = np.load(states_path)
        print(f"✅ Loaded states.npy: {states.shape}")

        # PCA → 2D
        pca = PCA(n_components=2)
        trajectory = pca.fit_transform(states)
        print("✅ PCA projection applied")

    # --- Load rift ---
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

    print(f"✅ Trajectory shape: {trajectory.shape}")
    print(f"✅ Rift shape: {rift_curve.shape}")

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
        tangent /= norm

    return tangent


# =============================
# CONTROL
# =============================

def apply_control(trajectory, rift_curve):
    controlled = [trajectory[0]]

    for i in range(1, len(trajectory)):
        current = controlled[-1]
        original_step = trajectory[i] - trajectory[i - 1]

        nearest, idx = find_nearest_rift_point(current, rift_curve)

        normal_vec = nearest - current
        tangent_vec = compute_tangent(rift_curve, idx)

        new_step = (
            BETA * original_step
            + ALPHA * normal_vec
            + GAMMA * tangent_vec
        )

        controlled.append(current + new_step)

    return np.array(controlled)


# =============================
# PLOT
# =============================

def plot_all(trajectory, rift_curve, controlled):
    plt.figure(figsize=(10, 6))

    plt.plot(trajectory[:, 0], trajectory[:, 1], color="green", label="original")
    plt.plot(rift_curve[:, 0], rift_curve[:, 1], color="cyan", linewidth=2, label="rift")
    plt.plot(controlled[:, 0], controlled[:, 1], color="yellow", label="controlled")

    plt.scatter(trajectory[-1, 0], trajectory[-1, 1], color="red", label="original end")
    plt.scatter(controlled[-1, 0], controlled[-1, 1], color="orange", label="controlled end")

    plt.legend()
    plt.title("Rift Tangent Control (Robust Load)")
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "rift_tangent_control.png")
    plt.savefig(save_path)
    print(f"💾 Saved → {save_path}")

    plt.show()


# =============================
# MAIN
# =============================

def main():
    trajectory, rift_curve = load_data()

    controlled = apply_control(trajectory, rift_curve)

    plot_all(trajectory, rift_curve, controlled)

    np.save(os.path.join(RIFT_DIR, "trajectory_controlled_tangent.npy"), controlled)
    print("💾 Saved controlled trajectory")

    print("🚀 DONE")


if __name__ == "__main__":
    main()
