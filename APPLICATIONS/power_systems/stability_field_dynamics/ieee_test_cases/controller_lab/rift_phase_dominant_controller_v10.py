# rift_phase_dominant_controller_v10.py

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
# SIGNAL / PHASE
# --------------------------------------------------

def dominant_freq(signal):
    fft_vals = np.fft.rfft(signal)
    power = np.abs(fft_vals)
    freqs = np.fft.rfftfreq(len(signal))
    idx = np.argmax(power[1:]) + 1
    return freqs[idx]


def compute_phase(n, freq):
    t = np.arange(n)
    return (2 * np.pi * freq * t) % (2 * np.pi)


def estimate_layer(traj):
    pc2 = traj[:, 1]
    center = np.median(pc2)
    spread = np.std(pc2)
    print(f"🎯 Base Layer: {center:.4f} ± {spread:.4f}")
    return center, spread


def nearest_rift_point(p, rift):
    dists = np.linalg.norm(rift - p, axis=1)
    return rift[np.argmin(dists)]


# --------------------------------------------------
# PHASE DOMINANT CONTROLLER
# --------------------------------------------------

def phase_dominant_controller(trajectory, rift):
    controlled = trajectory.copy()

    pc1 = trajectory[:, 0]
    pc2 = trajectory[:, 1]

    f1 = dominant_freq(pc1)
    f2 = dominant_freq(pc2)
    f = 0.5 * (f1 + f2)

    phase = compute_phase(len(trajectory), f)

    base_layer, spread = estimate_layer(trajectory)
    upper_layer = base_layer + 0.95 * spread
    lower_layer = base_layer - 0.65 * spread

    print(f"🔊 Dominant phase frequency: {f:.4f}")
    print(f"🎯 Upper Layer: {upper_layer:.4f}")
    print(f"🎯 Lower Layer: {lower_layer:.4f}")

    momentum = np.zeros_like(controlled)

    for t in range(len(controlled)):
        current = controlled[t]
        phi = phase[t]

        rift_target = nearest_rift_point(current, rift)

        # ------------------------------------------
        # PHASE DOMINANT REGIMES
        # ------------------------------------------
        # 0 → pi/2       : push up + forward
        # pi/2 → pi      : hold high + turn
        # pi → 3pi/2     : pull down + stabilize
        # 3pi/2 → 2pi    : relock near base
        # ------------------------------------------

        if 0.0 <= phi < 0.5 * np.pi:
            target_layer = upper_layer
            target_dx = 0.030
            gain_layer = 0.42
            gain_x = 0.18
            gain_rift = 0.04

        elif 0.5 * np.pi <= phi < np.pi:
            target_layer = upper_layer
            target_dx = 0.015
            gain_layer = 0.34
            gain_x = 0.10
            gain_rift = 0.03

        elif np.pi <= phi < 1.5 * np.pi:
            target_layer = lower_layer
            target_dx = 0.008
            gain_layer = 0.44
            gain_x = 0.06
            gain_rift = 0.02

        else:
            target_layer = base_layer
            target_dx = 0.004
            gain_layer = 0.36
            gain_x = 0.03
            gain_rift = 0.02

        # dominant layer force
        layer_target = np.array([current[0], target_layer])
        layer_corr = gain_layer * (layer_target - current)

        # forward transport
        x_target = np.array([current[0] + target_dx, current[1]])
        x_corr = gain_x * (x_target - current)

        # weak rift anchor only
        rift_corr = gain_rift * (rift_target - current)

        correction = layer_corr + x_corr + rift_corr

        # smooth with memory
        if t > 0:
            momentum[t] = 0.78 * momentum[t - 1] + 0.22 * correction
        else:
            momentum[t] = correction

        correction = np.tanh(momentum[t]) * 0.05
        controlled[t] += correction

    return controlled, phase, base_layer, upper_layer, lower_layer


# --------------------------------------------------
# PLOT
# --------------------------------------------------

def plot_result(original, controlled, rift, phase, base_layer, upper_layer, lower_layer):
    plt.figure(figsize=(10, 6))

    plt.plot(original[:, 0], original[:, 1], label="original", color="green")
    plt.plot(rift[:, 0], rift[:, 1], label="rift", color="cyan")
    plt.plot(controlled[:, 0], controlled[:, 1], label="phase-dominant v10", color="gold")

    plt.axhline(base_layer, linestyle="--", color="magenta", label="base layer")
    plt.axhline(upper_layer, linestyle="--", color="orange", label="upper layer")
    plt.axhline(lower_layer, linestyle="--", color="purple", label="lower layer")

    plt.scatter(original[-1, 0], original[-1, 1], color="red", label="orig end")
    plt.scatter(controlled[-1, 0], controlled[-1, 1], color="orange", label="controlled end")

    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "phase_dominant_v10.png")
    plt.savefig(save_path, dpi=150)
    print(f"💾 Saved → {save_path}")
    plt.close()

    plt.figure(figsize=(10, 3))
    plt.plot(phase, color="purple")
    plt.axhline(0.5 * np.pi, linestyle="--", color="gray")
    plt.axhline(np.pi, linestyle="--", color="gray")
    plt.axhline(1.5 * np.pi, linestyle="--", color="gray")
    plt.title("Phase progression (V10)")
    plt.xlabel("time step")
    plt.ylabel("phase")

    save_path = os.path.join(RIFT_DIR, "phase_dominant_v10_phase.png")
    plt.savefig(save_path, dpi=150)
    print(f"💾 Saved → {save_path}")
    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    trajectory, rift = load_data()

    controlled, phase, base_layer, upper_layer, lower_layer = phase_dominant_controller(
        trajectory, rift
    )

    np.save(os.path.join(RIFT_DIR, "phase_dominant_v10.npy"), controlled)
    print("💾 Saved controlled trajectory → phase_dominant_v10.npy")

    plot_result(
        trajectory,
        controlled,
        rift,
        phase,
        base_layer,
        upper_layer,
        lower_layer
    )

    print("🚀 Phase Dominant Controller V10 complete")


if __name__ == "__main__":
    main()
