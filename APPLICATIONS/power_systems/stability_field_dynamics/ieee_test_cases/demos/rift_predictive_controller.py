import numpy as np
import matplotlib.pyplot as plt
import os

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")

def load_data():
    trajectory = np.load(os.path.join(BASE_DIR, "trajectory.npy"))
    rift = np.load(os.path.join(RIFT_DIR, "rift_curve.npy"))
    return trajectory, rift

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

def predictive_control(trajectory, rift, lookahead=5):
    controlled = []
    prev_tangent = np.array([1.0, 0.0])

    for i in range(len(trajectory)):
        current = trajectory[i]

        rift_pt, idx, dist = nearest(current, rift)

        # 🔮 LOOKAHEAD TARGET
        target_idx = min(idx + lookahead, len(rift) - 1)
        target = rift[target_idx]

        # normal → toward future point
        normal = target - current

        # tangent at future point
        raw_tangent = tangent(rift, target_idx)

        # 🔥 direction consistency
        if np.dot(raw_tangent, prev_tangent) < 0:
            raw_tangent = -raw_tangent

        tang = 0.7 * prev_tangent + 0.3 * raw_tangent
        tang = tang / (np.linalg.norm(tang) + 1e-8)

        prev_tangent = tang

        # 🎛️ adaptive weights
        alpha = min(2.0, dist * 50)   # pull strength
        beta = 0.3                    # flow strength

        step = alpha * normal + beta * tang
        next_point = current + step

        controlled.append(next_point)

    return np.array(controlled)

def main():
    trajectory, rift = load_data()

    controlled = predictive_control(trajectory, rift, lookahead=8)

    # plot
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
    print(f"Saved → {out_path}")

    print("🚀 Predictive control complete")

if __name__ == "__main__":
    main()
