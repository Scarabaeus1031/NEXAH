import numpy as np
import matplotlib.pyplot as plt
import os

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")


# --------------------------------------------------
# LOAD DATA (ROBUST)
# --------------------------------------------------
def load_data():

    # --- TRAJECTORY ---
    possible_traj = ["trajectory.npy", "states.npy"]

    trajectory = None
    for f in possible_traj:
        path = os.path.join(BASE_DIR, f)
        if os.path.exists(path):
            trajectory = np.load(path)
            print(f"✅ Loaded trajectory from {f}")
            break

    if trajectory is None:
        raise FileNotFoundError(
            f"❌ No trajectory file found in {BASE_DIR}\nTried: {possible_traj}"
        )

    # ggf. Dimension reduzieren
    if trajectory.shape[1] > 2:
        print("⚠️ Reducing trajectory to 2D (using first 2 components)")
        trajectory = trajectory[:, :2]

    print(f"📈 Trajectory shape: {trajectory.shape}")

    # --- RIFT ---
    possible_rift = ["rift_curve.npy", "rift.npy", "rift_points.npy"]

    rift = None
    for f in possible_rift:
        path = os.path.join(RIFT_DIR, f)
        if os.path.exists(path):
            rift = np.load(path)
            print(f"✅ Loaded rift from {f}")
            break

    if rift is None:
        raise FileNotFoundError(
            f"❌ No rift file found in {RIFT_DIR}\nTried: {possible_rift}"
        )

    print(f"📉 Rift shape: {rift.shape}")

    return trajectory, rift


# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def nearest(pt, curve):
    dists = np.linalg.norm(curve - pt, axis=1)
    idx = np.argmin(dists)
    return curve[idx], idx, dists[idx]


def tangent(curve, idx):
    if idx <= 0:
        t = curve[idx + 1] - curve[idx]
    elif idx >= len(curve) - 1:
        t = curve[idx] - curve[idx - 1]
    else:
        t = curve[idx + 1] - curve[idx - 1]
    return t / (np.linalg.norm(t) + 1e-8)


# --------------------------------------------------
# PREDICTIVE CONTROLLER
# --------------------------------------------------
def predictive_control(trajectory, rift, lookahead=8):

    controlled = []
    prev_tangent = np.array([1.0, 0.0])

    for i in range(len(trajectory)):
        current = trajectory[i]

        rift_pt, idx, dist = nearest(current, rift)

        # 🔮 LOOKAHEAD
        target_idx = min(idx + lookahead, len(rift) - 1)
        target = rift[target_idx]

        # normal (toward future)
        normal = target - current

        # tangent at future point
        raw_tangent = tangent(rift, target_idx)

        # 🔁 direction consistency
        if np.dot(raw_tangent, prev_tangent) < 0:
            raw_tangent = -raw_tangent

        tang = 0.7 * prev_tangent + 0.3 * raw_tangent
        tang = tang / (np.linalg.norm(tang) + 1e-8)

        prev_tangent = tang

        # adaptive weights
        alpha = min(2.0, dist * 50)  # pull
        beta = 0.3                   # flow

        step = alpha * normal + beta * tang
        next_point = current + step

        controlled.append(next_point)

    return np.array(controlled)


# --------------------------------------------------
# MAIN
# --------------------------------------------------
def main():

    trajectory, rift = load_data()

    controlled = predictive_control(trajectory, rift, lookahead=8)

    # --- PLOT ---
    plt.figure(figsize=(8, 5))

    plt.plot(trajectory[:, 0], trajectory[:, 1], color='green', label='original')
    plt.plot(rift[:, 0], rift[:, 1], color='cyan', label='rift')
    plt.plot(controlled[:, 0], controlled[:, 1], color='gold', label='predictive')

    plt.scatter(trajectory[-1, 0], trajectory[-1, 1], color='red', label='orig end')
    plt.scatter(controlled[-1, 0], controlled[-1, 1], color='orange', label='controlled end')

    plt.title("Predictive Rift Control")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend()
    plt.grid()

    out_path = os.path.join(RIFT_DIR, "rift_predictive_control.png")
    plt.savefig(out_path, dpi=150)

    print(f"💾 Saved → {out_path}")
    print("🚀 Predictive control complete")


if __name__ == "__main__":
    main()
