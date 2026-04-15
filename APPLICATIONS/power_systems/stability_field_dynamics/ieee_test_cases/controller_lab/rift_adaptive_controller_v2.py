import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")

LOCK_THRESHOLD = 0.03   # critical distance
SOFT_THRESHOLD = 0.015  # transition zone


# =============================
# LOAD
# =============================

def load_data():
    traj_path = os.path.join(BASE_DIR, "trajectory.npy")

    if os.path.exists(traj_path):
        trajectory = np.load(traj_path)
    else:
        states = np.load(os.path.join(BASE_DIR, "states.npy"))
        trajectory = PCA(n_components=2).fit_transform(states)

    for name in ["rift_curve.npy", "rift.npy", "rift_points.npy"]:
        path = os.path.join(RIFT_DIR, name)
        if os.path.exists(path):
            rift = np.load(path)
            return trajectory, rift

    raise FileNotFoundError("No rift found")


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
        t = rift[idx+1] - rift[idx-1]

    n = np.linalg.norm(t)
    return t / n if n > 0 else t


# =============================
# LOCKING CONTROLLER
# =============================

def control(traj, rift):
    controlled = [traj[0]]

    for i in range(1, len(traj)):
        current = controlled[-1]
        orig = traj[i] - traj[i-1]

        rift_pt, idx, dist = nearest(current, rift)
        normal = rift_pt - current
        tang = tangent(rift, idx)

        # =============================
        # ZONE LOGIC
        # =============================

        if dist > LOCK_THRESHOLD:
            # HARD LOCK → go back to rift
            step = 0.2 * normal

        elif dist > SOFT_THRESHOLD:
            # TRANSITION ZONE
            step = (
                0.5 * orig
                + 0.3 * normal
                + 0.2 * tang
            )

        else:
            # ON RIFT → glide
            step = (
                0.7 * orig
                + 0.1 * normal
                + 0.4 * tang
            )

        controlled.append(current + step)

    return np.array(controlled)


# =============================
# PLOT
# =============================

def plot(traj, rift, ctrl):
    plt.figure(figsize=(10,6))

    plt.plot(traj[:,0], traj[:,1], 'g', label='original')
    plt.plot(rift[:,0], rift[:,1], 'c', linewidth=2, label='rift')
    plt.plot(ctrl[:,0], ctrl[:,1], 'y', label='adaptive-lock')

    plt.scatter(traj[-1,0], traj[-1,1], c='red', label='orig end')
    plt.scatter(ctrl[-1,0], ctrl[-1,1], c='orange', label='controlled end')

    plt.legend()
    plt.grid()
    plt.title("Adaptive Lock Controller")

    save = os.path.join(RIFT_DIR, "rift_adaptive_lock.png")
    plt.savefig(save)
    print(f"Saved → {save}")

    plt.show()


# =============================
# MAIN
# =============================

def main():
    traj, rift = load_data()

    ctrl = control(traj, rift)

    plot(traj, rift, ctrl)

    np.save(os.path.join(RIFT_DIR, "trajectory_lock.npy"), ctrl)

    print("🚀 Lock control complete")


if __name__ == "__main__":
    main()
