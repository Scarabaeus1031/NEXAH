# rift_phase_target_controller_v14_3_phase_portrait.py

import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")


# --------------------------------------------------
# LOAD
# --------------------------------------------------

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

    return trajectory[:, :2], rift


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def wrap_angle(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def dominant_freq(signal):
    fft_vals = np.fft.rfft(signal)
    power = np.abs(fft_vals)
    freqs = np.fft.rfftfreq(len(signal))
    idx = np.argmax(power[1:]) + 1
    return freqs[idx]


def estimate_layer(traj):
    pc2 = traj[:, 1]
    center = np.median(pc2)
    spread = np.std(pc2)
    print(f"🎯 Base Layer: {center:.4f} ± {spread:.4f}")
    return center, spread


# --------------------------------------------------
# CONTROLLER (V14.2 CORE REUSED)
# --------------------------------------------------

def run_controller(trajectory):

    controlled = trajectory.copy()

    pc1 = trajectory[:, 0]
    pc2 = trajectory[:, 1]

    f0 = 0.5 * (dominant_freq(pc1) + dominant_freq(pc2))

    base_layer, spread = estimate_layer(trajectory)
    upper_layer = base_layer + 0.95 * spread
    lower_layer = base_layer - 0.65 * spread

    print(f"🔊 Base frequency: {f0:.4f}")

    N = len(controlled)

    phi = np.zeros(N)
    ref_phi = np.zeros(N)
    target_phi = np.zeros(N)
    dphi = np.zeros(N)

    regime = np.zeros(N)  # -1, 0, +1

    phi[0] = 0.0

    for t in range(1, N):

        ref_phi[t] = (2 * np.pi * f0 * t)

        y = controlled[t - 1, 1]

        if y > base_layer + 0.3 * spread:
            target_phi[t] = 0.35 * np.pi
            regime[t] = 1
        elif y < base_layer - 0.3 * spread:
            target_phi[t] = 1.35 * np.pi
            regime[t] = -1
        else:
            target_phi[t] = np.pi
            regime[t] = 0

        pe_ref = wrap_angle(phi[t - 1] - ref_phi[t - 1])
        pe_target = wrap_angle(phi[t - 1] - target_phi[t - 1])

        dphi[t] = (
            2 * np.pi * f0
            - 0.55 * pe_ref
            - 0.35 * pe_target
        )

        phi[t] = phi[t - 1] + dphi[t]

    return phi, dphi, regime


# --------------------------------------------------
# PHASE PORTRAIT
# --------------------------------------------------

def plot_phase_portrait(phi, dphi, regime):

    plt.figure(figsize=(8, 8))

    # color mapping
    colors = {
        -1: "purple",
         0: "gold",
         1: "green"
    }

    for r in [-1, 0, 1]:
        mask = regime == r
        plt.scatter(phi[mask], dphi[mask],
                    s=12,
                    color=colors[r],
                    label=f"regime {r}",
                    alpha=0.7)

    plt.axhline(0, linestyle="--", color="gray")
    plt.axvline(0, linestyle="--", color="gray")

    plt.xlabel("φ (phase)")
    plt.ylabel("dφ/dt (phase velocity)")
    plt.title("V14.3 Phase Portrait (φ vs dφ/dt)")

    plt.legend()
    plt.grid(True)

    path = os.path.join(RIFT_DIR, "v14_3_phase_portrait.png")
    plt.savefig(path, dpi=150)
    print(f"💾 Saved → {path}")
    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    trajectory, _ = load_data()

    phi, dphi, regime = run_controller(trajectory)

    plot_phase_portrait(phi, dphi, regime)

    print("🚀 V14.3 Phase Portrait DONE")


if __name__ == "__main__":
    main()
