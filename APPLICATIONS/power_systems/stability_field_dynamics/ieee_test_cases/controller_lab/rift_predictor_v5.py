# rift_corridor_lock_v5.py

import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")


def load_data():
    trajectory = None

    for name in ["trajectory.npy", "states.npy"]:
        path = os.path.join(BASE_DIR, name)
        if os.path.exists(path):
            trajectory = np.load(path)
            print(f"✅ Loaded trajectory: {name}")
            break

    if trajectory is None:
        raise FileNotFoundError("❌ No trajectory file found")

    rift_path = os.path.join(RIFT_DIR, "rift_curve.npy")
    if not os.path.exists(rift_path):
        raise FileNotFoundError("❌ No rift_curve.npy found")

    rift = np.load(rift_path)
    print("✅ Loaded rift")

    return trajectory, rift


def estimate_corridor(rift):
    # simple corridor: mean + band
    mean_line = np.mean(rift[:, 1])
    std = np.std(rift[:, 1])

    lower = mean_line - std
    upper = mean_line + std

    print(f"🎯 Corridor: [{lower:.4f}, {upper:.4f}]")

    return mean_line, lower, upper


def corridor_lock_control(trajectory, rift, gain=0.3):
    controlled = trajectory.copy()

    mean_line, lower, upper = estimate_corridor(rift)

    for t in range(len(controlled)):

        current = controlled[t]

        # project to corridor center
        target = np.array([current[0], mean_line])

        correction = gain * (target - current)

        correction = np.clip(correction, -0.03, 0.03)

        controlled[t] += correction

    return controlled, mean_line


def plot_result(original, controlled, rift, mean_line):
    plt.figure(figsize=(10, 6))

    plt.plot(original[:, 0], original[:, 1], label="original", color="green")
    plt.plot(rift[:, 0], rift[:, 1], label="rift", color="cyan")
    plt.plot(controlled[:, 0], controlled[:, 1], label="corridor lock v5", color="gold")

    plt.axhline(mean_line, linestyle="--", color="magenta", label="corridor center")

    plt.scatter(original[-1, 0], original[-1, 1], color="red", label="orig end")
    plt.scatter(controlled[-1, 0], controlled[-1, 1], color="orange", label="controlled end")

    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "corridor_lock_v5.png")
    plt.savefig(save_path, dpi=150)
    print(f"💾 Saved → {save_path}")

    plt.close()


def main():
    trajectory, rift = load_data()
    trajectory = trajectory[:, :2]

    controlled, mean_line = corridor_lock_control(trajectory, rift)

    plot_result(trajectory, controlled, rift, mean_line)

    print("🚀 Corridor Lock V5 complete")


if __name__ == "__main__":
    main()
