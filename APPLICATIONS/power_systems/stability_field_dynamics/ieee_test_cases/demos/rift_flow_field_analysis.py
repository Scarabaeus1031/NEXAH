# rift_flow_field_analysis.py

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
    traj = safe_load([
        "states.npy",
        "trajectory.npy"
    ])

    ctrl = safe_load([
        "rift_extraction/final_controller_v9_1.npy",
        "rift_extraction/final_controller_v9.npy",
        "rift_extraction/final_controller_v7.npy"
    ])

    return traj[:, :2], ctrl[:, :2]


# --------------------------------------------------
# FLOW COMPUTATION
# --------------------------------------------------

def compute_velocity(traj):
    return np.diff(traj, axis=0)


def compute_acceleration(vel):
    return np.diff(vel, axis=0)


def compute_divergence(vel):
    speed = np.linalg.norm(vel, axis=1)
    return np.diff(speed)


def compute_alignment(vel):
    v1 = vel[:-1]
    v2 = vel[1:]

    v1n = v1 / (np.linalg.norm(v1, axis=1, keepdims=True) + 1e-8)
    v2n = v2 / (np.linalg.norm(v2, axis=1, keepdims=True) + 1e-8)

    return np.sum(v1n * v2n, axis=1)


# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_flow(traj, vel, title, filename):

    plt.figure(figsize=(8, 6))

    plt.plot(traj[:, 0], traj[:, 1], color="gray", alpha=0.5)

    skip = 2
    plt.quiver(
        traj[:-1:skip, 0],
        traj[:-1:skip, 1],
        vel[::skip, 0],
        vel[::skip, 1],
        angles='xy',
        scale_units='xy',
        scale=1,
        color='blue',
        width=0.003
    )

    plt.title(title)
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, filename)
    plt.savefig(save_path, dpi=150)
    print(f"💾 Saved → {save_path}")
    plt.close()


def plot_divergence(div, title, filename):

    plt.figure(figsize=(10, 3))
    plt.plot(div)

    plt.axhline(0, linestyle="--")

    plt.title(title)
    plt.xlabel("time")
    plt.ylabel("Δ speed")

    save_path = os.path.join(RIFT_DIR, filename)
    plt.savefig(save_path)
    print(f"💾 Saved → {save_path}")
    plt.close()


def plot_alignment(align, title, filename):

    plt.figure(figsize=(10, 3))
    plt.plot(align)

    plt.axhline(0, linestyle="--")

    plt.title(title)
    plt.xlabel("time")
    plt.ylabel("cos(angle)")

    save_path = os.path.join(RIFT_DIR, filename)
    plt.savefig(save_path)
    print(f"💾 Saved → {save_path}")
    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def analyze(traj, name):

    vel = compute_velocity(traj)
    div = compute_divergence(vel)
    align = compute_alignment(vel)

    print(f"\n📊 {name}")
    print(f"mean divergence: {np.mean(div):.6f}")
    print(f"mean alignment: {np.mean(align):.6f}")

    plot_flow(traj, vel, f"{name} Flow Field", f"{name}_flow.png")
    plot_divergence(div, f"{name} Expansion / Contraction", f"{name}_divergence.png")
    plot_alignment(align, f"{name} Flow Alignment", f"{name}_alignment.png")


def main():

    traj, ctrl = load_data()

    analyze(traj, "original")
    analyze(ctrl, "controlled")

    print("\n🚀 Flow field analysis complete")


if __name__ == "__main__":
    main()
