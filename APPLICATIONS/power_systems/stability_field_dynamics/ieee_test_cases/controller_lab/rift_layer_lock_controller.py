import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")


# =============================
# LOAD
# =============================
def load_data():
    trajectory = None

    for f in ["trajectory.npy", "states.npy"]:
        path = os.path.join(BASE_DIR, f)
        if os.path.exists(path):
            trajectory = np.load(path)
            print(f"✅ Loaded trajectory: {f}")
            break

    if trajectory is None:
        raise FileNotFoundError("❌ No trajectory found")

    if trajectory.shape[1] > 2:
        trajectory = trajectory[:, :2]

    rift = None
    for f in ["rift_curve.npy", "rift.npy"]:
        path = os.path.join(RIFT_DIR, f)
        if os.path.exists(path):
            rift = np.load(path)
            print(f"✅ Loaded rift: {f}")
            break

    return trajectory, rift


# =============================
# HELPERS
# =============================
def nearest(pt, curve):
    d = np.linalg.norm(curve - pt, axis=1)
    i = np.argmin(d)
    return curve[i], i


def tangent(curve, i):
    if i <= 0:
        t = curve[1] - curve[0]
    elif i >= len(curve) - 1:
        t = curve[-1] - curve[-2]
    else:
        t = curve[i+1] - curve[i-1]

    return t / (np.linalg.norm(t) + 1e-8)


# =============================
# LAYER LOCK CONTROLLER
# =============================
def layer_lock_controller(traj, rift):

    controlled = []
    prev_tangent = np.array([1.0, 0.0])

    # 👉 automatischer Layer (statt hardcode 0.78)
    target_layer = np.median(traj[:, 1])
    print(f"🎯 Target layer detected: {target_layer:.4f}")

    global_target = traj[-1]

    for x in traj:

        rift_pt, idx = nearest(x, rift)

        # =============================
        # FIELD COMPONENTS
        # =============================

        # 🔥 Layer Lock (das ist der Gamechanger)
        F_layer = np.array([0.0, target_layer - x[1]])

        # Channel (horizontal movement)
        F_channel = tangent(rift, idx)

        # Attractor (global drift)
        F_attractor = global_target - x

        # smoothing
        if np.dot(F_channel, prev_tangent) < 0:
            F_channel = -F_channel

        F_channel = 0.7 * prev_tangent + 0.3 * F_channel
        F_channel /= (np.linalg.norm(F_channel) + 1e-8)

        prev_tangent = F_channel

        # =============================
        # WEIGHTS
        # =============================
        alpha = 0.1   # attractor
        beta = 0.4    # channel
        gamma = 1.2   # layer lock (dominant!)

        step = alpha * F_attractor + beta * F_channel + gamma * F_layer

        x_next = x + step
        controlled.append(x_next)

    return np.array(controlled), target_layer


# =============================
# MAIN
# =============================
def main():

    traj, rift = load_data()

    controlled, layer = layer_lock_controller(traj, rift)

    plt.figure(figsize=(8, 5))

    plt.plot(traj[:, 0], traj[:, 1], 'g', label='original')
    plt.plot(rift[:, 0], rift[:, 1], 'c', label='rift')
    plt.plot(controlled[:, 0], controlled[:, 1], 'gold', label='layer-lock')

    # 🔥 visualisierung des layers
    plt.axhline(layer, color='magenta', linestyle='--', label='target layer')

    plt.scatter(traj[-1, 0], traj[-1, 1], c='red', label='orig end')
    plt.scatter(controlled[-1, 0], controlled[-1, 1], c='orange', label='controlled end')

    plt.legend()
    plt.title("Layer Lock Controller (V75)")
    plt.grid()

    out = os.path.join(RIFT_DIR, "layer_lock_controller.png")
    plt.savefig(out, dpi=150)

    print(f"💾 Saved → {out}")
    print("🚀 Layer lock control complete")


if __name__ == "__main__":
    main()
