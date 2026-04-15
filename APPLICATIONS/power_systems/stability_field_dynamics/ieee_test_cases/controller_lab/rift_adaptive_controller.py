import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")

# =============================
# LOAD
# =============================

def load_data():
    traj_path = os.path.join(BASE_DIR, "trajectory.npy")

    if os.path.exists(traj_path):
        trajectory = np.load(traj_path)
        print("✅ trajectory.npy loaded")
    else:
        states = np.load(os.path.join(BASE_DIR, "states.npy"))
        pca = PCA(n_components=2)
        trajectory = pca.fit_transform(states)
        print("✅ states.npy → PCA")

    for name in ["rift_curve.npy", "rift.npy", "rift_points.npy"]:
        path = os.path.join(RIFT_DIR, name)
        if os.path.exists(path):
            rift = np.load(path)
            print(f"✅ rift loaded: {name}")
            return trajectory, rift

    raise FileNotFoundError("❌ No rift file found")


# =============================
# HELPERS
# =============================

def nearest(point, rift):
    d = np.linalg.norm(rift - point, axis=1)
    idx = np.argmin(d)
    return rift[idx], idx, d[idx]


def tangent(rift, idx):
    if idx == 0:
        t = rift[1] - rift[0]
    elif idx == len(rift) - 1:
        t = rift[-1] - rift[-2]
    else:
        t = rift[idx + 1] - rift[idx - 1]

    n = np.linalg.norm(t)
    return t / n if n > 0 else t


# =============================
# ADAPTIVE CONTROL
# =============================

def adaptive_control(traj, rift):
    controlled = [traj[0]]

    for i in range(1, len(traj)):
        current = controlled[-1]
        orig_step = traj[i] - traj[i - 1]

        rift_pt, idx, dist = nearest(current, rift)

        normal = rift_pt - current
        tang = tangent(rift, idx)

        # =============================
        # ADAPTIVE WEIGHTS
        # =============================

        # normalize distance
        d = min(dist * 50, 1.0)

        # far → pull hard
        alpha = 0.3 * d

        # near → follow tangent
        gamma = 0.4 * (1 - d)

        # damping (reduce chaos)
        beta = 0.6 + 0.2 * (1 - d)

        # =============================
        # COMBINE
        # =============================

        step = (
            beta * orig_step
            + alpha * normal
            + gamma * tang
        )

        controlled.append(current + step)

    return np.array(controlled)


# =============================
# PLOT
# =============================

def plot(traj, rift, ctrl):
    plt.figure(figsize=(10, 6))

    plt.plot(traj[:,0], traj[:,1], 'g', label='original')
    plt.plot(rift[:,0], rift[:,1], 'c', linewidth=2, label='rift')
    plt.plot(ctrl[:,0], ctrl[:,1], 'y', label='adaptive')

    plt.scatter(traj[-1,0], traj[-1,1], c='red', label='orig end')
    plt.scatter(ctrl[-1,0], ctrl[-1,1], c='orange', label='adaptive end')

    plt.legend()
    plt.grid()
    plt.title("Adaptive Rift Control")

    save = os.path.join(RIFT_DIR, "rift_adaptive_control.png")
    plt.savefig(save)
    print(f"💾 Saved → {save}")

    plt.show()


# =============================
# MAIN
# =============================

def main():
    traj, rift = load_data()

    ctrl = adaptive_control(traj, rift)

    plot(traj, rift, ctrl)

    np.save(os.path.join(RIFT_DIR, "trajectory_adaptive.npy"), ctrl)

    print("🚀 Adaptive control complete")


if __name__ == "__main__":
    main()
