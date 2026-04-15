# rift_phase_multifrequency_controller_v11.py

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
# FREQUENCY / PHASE
# --------------------------------------------------

def fft_spectrum(signal):
    fft_vals = np.fft.rfft(signal)
    power = np.abs(fft_vals)
    freqs = np.fft.rfftfreq(len(signal))
    return freqs, power


def dominant_freq(signal):
    freqs, power = fft_spectrum(signal)
    idx = np.argmax(power[1:]) + 1
    return freqs[idx]


def build_multiphase(n, f):
    t = np.arange(n)

    phi1 = 2 * np.pi * f * t
    phi2 = 2 * np.pi * (2 * f) * t
    phi3 = 2 * np.pi * (3 * f) * t

    # weighted composite phase drive
    drive = (
        1.00 * np.sin(phi1) +
        0.50 * np.sin(phi2) +
        0.30 * np.sin(phi3)
    )

    return phi1 % (2 * np.pi), drive


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
# MULTI-FREQUENCY CONTROLLER
# --------------------------------------------------

def multifrequency_phase_controller(trajectory, rift):
    controlled = trajectory.copy()

    pc1 = trajectory[:, 0]
    pc2 = trajectory[:, 1]

    f1 = dominant_freq(pc1)
    f2 = dominant_freq(pc2)
    f = 0.5 * (f1 + f2)

    phase, drive = build_multiphase(len(trajectory), f)

    base_layer, spread = estimate_layer(trajectory)
    upper_layer = base_layer + 0.95 * spread
    lower_layer = base_layer - 0.65 * spread

    print(f"🔊 Base frequency: {f:.4f}")
    print(f"🎯 Upper Layer: {upper_layer:.4f}")
    print(f"🎯 Lower Layer: {lower_layer:.4f}")

    momentum = np.zeros_like(controlled)

    for t in range(len(controlled)):
        current = controlled[t]
        d = drive[t]

        rift_target = nearest_rift_point(current, rift)

        # --------------------------------------------------
        # MULTI-MODE REGIMES
        # d > +0.35  -> strong expansion
        # 0 < d <= .35 -> upper transit
        # -0.35 <= d <= 0 -> base / relock
        # d < -0.35 -> contraction toward lower
        # --------------------------------------------------

        if d > 0.35:
            target_layer = upper_layer
            target_dx = 0.030
            gain_layer = 0.40
            gain_x = 0.16
            gain_rift = 0.03

        elif 0.0 < d <= 0.35:
            target_layer = 0.5 * (base_layer + upper_layer)
            target_dx = 0.018
            gain_layer = 0.28
            gain_x = 0.10
            gain_rift = 0.03

        elif -0.35 <= d <= 0.0:
            target_layer = base_layer
            target_dx = 0.010
            gain_layer = 0.26
            gain_x = 0.06
            gain_rift = 0.02

        else:
            target_layer = lower_layer
            target_dx = 0.004
            gain_layer = 0.38
            gain_x = 0.03
            gain_rift = 0.02

        # layer pull
        layer_target = np.array([current[0], target_layer])
        layer_corr = gain_layer * (layer_target - current)

        # forward drift
        x_target = np.array([current[0] + target_dx, current[1]])
        x_corr = gain_x * (x_target - current)

        # weak rift anchor
        rift_corr = gain_rift * (rift_target - current)

        correction = layer_corr + x_corr + rift_corr

        # memory
        if t > 0:
            momentum[t] = 0.80 * momentum[t - 1] + 0.20 * correction
        else:
            momentum[t] = correction

        correction = np.tanh(momentum[t]) * 0.05
        controlled[t] += correction

    return controlled, phase, drive, base_layer, upper_layer, lower_layer, f


# --------------------------------------------------
# PLOT
# --------------------------------------------------

def plot_result(original, controlled, rift, phase, drive, base_layer, upper_layer, lower_layer):
    plt.figure(figsize=(10, 6))

    plt.plot(original[:, 0], original[:, 1], label="original", color="green")
    plt.plot(rift[:, 0], rift[:, 1], label="rift", color="cyan")
    plt.plot(controlled[:, 0], controlled[:, 1], label="phase-multifrequency v11", color="gold")

    plt.axhline(base_layer, linestyle="--", color="magenta", label="base layer")
    plt.axhline(upper_layer, linestyle="--", color="orange", label="upper layer")
    plt.axhline(lower_layer, linestyle="--", color="purple", label="lower layer")

    plt.scatter(original[-1, 0], original[-1, 1], color="red", label="orig end")
    plt.scatter(controlled[-1, 0], controlled[-1, 1], color="orange", label="controlled end")

    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "phase_multifrequency_v11.png")
    plt.savefig(save_path, dpi=150)
    print(f"💾 Saved → {save_path}")
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(phase, label="base phase", color="purple")
    plt.plot(drive, label="multi-frequency drive", color="black", alpha=0.8)
    plt.axhline(0.35, linestyle="--", color="gray")
    plt.axhline(0.0, linestyle="--", color="gray")
    plt.axhline(-0.35, linestyle="--", color="gray")
    plt.legend()
    plt.grid(True)
    plt.title("Phase + Multi-Frequency Drive")

    save_path = os.path.join(RIFT_DIR, "phase_multifrequency_v11_phase.png")
    plt.savefig(save_path, dpi=150)
    print(f"💾 Saved → {save_path}")
    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    trajectory, rift = load_data()

    controlled, phase, drive, base_layer, upper_layer, lower_layer, f = multifrequency_phase_controller(
        trajectory, rift
    )

    np.save(os.path.join(RIFT_DIR, "phase_multifrequency_v11.npy"), controlled)
    print("💾 Saved controlled trajectory → phase_multifrequency_v11.npy")

    plot_result(
        trajectory,
        controlled,
        rift,
        phase,
        drive,
        base_layer,
        upper_layer,
        lower_layer
    )

    print("🚀 Multi-Frequency Phase Controller V11 complete")


if __name__ == "__main__":
    main()
