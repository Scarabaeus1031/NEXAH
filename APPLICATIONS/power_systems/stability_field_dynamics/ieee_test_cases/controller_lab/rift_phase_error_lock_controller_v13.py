# rift_phase_error_lock_controller_v13.py

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
# SIGNAL / GEOMETRY HELPERS
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


def estimate_layer(traj):
    pc2 = traj[:, 1]
    center = np.median(pc2)
    spread = np.std(pc2)
    print(f"🎯 Base Layer: {center:.4f} ± {spread:.4f}")
    return center, spread


def nearest_rift_point(p, rift):
    dists = np.linalg.norm(rift - p, axis=1)
    return rift[np.argmin(dists)]


def wrap_angle(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


# --------------------------------------------------
# V13 PHASE ERROR LOCK CONTROLLER
# --------------------------------------------------

def phase_error_lock_controller(trajectory, rift):
    controlled = trajectory.copy()

    pc1 = trajectory[:, 0]
    pc2 = trajectory[:, 1]

    f1 = dominant_freq(pc1)
    f2 = dominant_freq(pc2)
    f0 = 0.5 * (f1 + f2)

    base_layer, spread = estimate_layer(trajectory)
    upper_layer = base_layer + 0.95 * spread
    lower_layer = base_layer - 0.65 * spread

    print(f"🔊 Base frequency: {f0:.4f}")
    print(f"🎯 Upper Layer: {upper_layer:.4f}")
    print(f"🎯 Lower Layer: {lower_layer:.4f}")

    # persistent states
    phi = np.zeros(len(controlled))
    ref_phi = np.zeros(len(controlled))
    drive = np.zeros(len(controlled))
    phase_error = np.zeros(len(controlled))

    momentum = np.zeros_like(controlled)

    # initial phase
    phi[0] = 0.0
    ref_phi[0] = 0.0

    # coupling strengths
    k_layer = 1.2
    k_speed = 1.5
    k_turn = 0.9
    k_lock = 0.55   # phase error correction
    k_relax = 0.08  # return toward base oscillator

    dt = 1.0

    for t in range(len(controlled)):

        # ideal reference phase = pure clock
        ref_phi[t] = (2 * np.pi * f0 * t) % (2 * np.pi)

        if t > 1:
            vel = controlled[t - 1] - controlled[t - 2]
            speed = np.linalg.norm(vel)

            if t > 2:
                prev_vel = controlled[t - 2] - controlled[t - 3]
            else:
                prev_vel = vel

            turn = np.linalg.norm(vel - prev_vel)
            layer_dev = (controlled[t - 1, 1] - base_layer) / (spread + 1e-8)

            # current phase error relative to reference
            pe = wrap_angle(phi[t - 1] - ref_phi[t - 1])
            phase_error[t] = pe

            # feedback phase increment
            dphi = (
                2 * np.pi * f0
                + k_layer * layer_dev * 0.025
                + k_speed * speed * 0.018
                + k_turn * turn * 0.015
                - k_lock * pe
                - k_relax * np.sin(pe)
            )

            phi[t] = (phi[t - 1] + dphi * dt) % (2 * np.pi)

        elif t > 0:
            phi[t] = (phi[t - 1] + 2 * np.pi * f0) % (2 * np.pi)
            phase_error[t] = wrap_angle(phi[t] - ref_phi[t])

        # multi-frequency drive from corrected phase
        drive[t] = (
            1.00 * np.sin(phi[t]) +
            0.50 * np.sin(2 * phi[t]) +
            0.30 * np.sin(3 * phi[t])
        )

        d = drive[t]
        current = controlled[t]
        rift_target = nearest_rift_point(current, rift)

        # phase-error-sensitive layer targeting
        pe_abs = abs(phase_error[t])

        if d > 0.35:
            target_layer = upper_layer
            target_dx = 0.028
            gain_layer = 0.40
            gain_x = 0.15
            gain_rift = 0.03

        elif 0.0 < d <= 0.35:
            target_layer = 0.5 * (base_layer + upper_layer)
            target_dx = 0.018
            gain_layer = 0.30
            gain_x = 0.10
            gain_rift = 0.03

        elif -0.35 <= d <= 0.0:
            target_layer = base_layer
            target_dx = 0.010
            gain_layer = 0.28
            gain_x = 0.06
            gain_rift = 0.02

        else:
            target_layer = lower_layer
            target_dx = 0.004
            gain_layer = 0.38
            gain_x = 0.03
            gain_rift = 0.02

        # lock harder when phase error grows
        lock_boost = 1.0 + min(pe_abs / np.pi, 1.0) * 0.8
        gain_layer *= lock_boost

        layer_target = np.array([current[0], target_layer])
        layer_corr = gain_layer * (layer_target - current)

        x_target = np.array([current[0] + target_dx, current[1]])
        x_corr = gain_x * (x_target - current)

        rift_corr = gain_rift * (rift_target - current)

        correction = layer_corr + x_corr + rift_corr

        if t > 0:
            momentum[t] = 0.82 * momentum[t - 1] + 0.18 * correction
        else:
            momentum[t] = correction

        correction = np.tanh(momentum[t]) * 0.05
        controlled[t] += correction

    return controlled, phi, ref_phi, drive, phase_error, base_layer, upper_layer, lower_layer, f0


# --------------------------------------------------
# PLOT
# --------------------------------------------------

def plot_result(original, controlled, rift, phi, ref_phi, drive, phase_error,
                base_layer, upper_layer, lower_layer):
    plt.figure(figsize=(10, 6))

    plt.plot(original[:, 0], original[:, 1], label="original", color="green")
    plt.plot(rift[:, 0], rift[:, 1], label="rift", color="cyan")
    plt.plot(controlled[:, 0], controlled[:, 1], label="phase-error-lock v13", color="gold")

    plt.axhline(base_layer, linestyle="--", color="magenta", label="base layer")
    plt.axhline(upper_layer, linestyle="--", color="orange", label="upper layer")
    plt.axhline(lower_layer, linestyle="--", color="purple", label="lower layer")

    plt.scatter(original[-1, 0], original[-1, 1], color="red", label="orig end")
    plt.scatter(controlled[-1, 0], controlled[-1, 1], color="orange", label="controlled end")

    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "phase_error_lock_v13.png")
    plt.savefig(save_path, dpi=150)
    print(f"💾 Saved → {save_path}")
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(phi, label="feedback phase", color="purple")
    plt.plot(ref_phi, label="reference phase", color="blue", alpha=0.8)
    plt.plot(drive, label="drive", color="black", alpha=0.8)
    plt.axhline(0.35, linestyle="--", color="gray")
    plt.axhline(0.0, linestyle="--", color="gray")
    plt.axhline(-0.35, linestyle="--", color="gray")
    plt.legend()
    plt.grid(True)
    plt.title("Phase Error Lock + Drive (V13)")

    save_path = os.path.join(RIFT_DIR, "phase_error_lock_v13_phase.png")
    plt.savefig(save_path, dpi=150)
    print(f"💾 Saved → {save_path}")
    plt.close()

    plt.figure(figsize=(10, 3))
    plt.plot(phase_error, color="red")
    plt.axhline(0.0, linestyle="--", color="gray")
    plt.title("Phase Error (V13)")
    plt.xlabel("time step")
    plt.ylabel("wrapped error")

    save_path = os.path.join(RIFT_DIR, "phase_error_lock_v13_error.png")
    plt.savefig(save_path, dpi=150)
    print(f"💾 Saved → {save_path}")
    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    trajectory, rift = load_data()

    controlled, phi, ref_phi, drive, phase_error, base_layer, upper_layer, lower_layer, f0 = (
        phase_error_lock_controller(trajectory, rift)
    )

    np.save(os.path.join(RIFT_DIR, "phase_error_lock_v13.npy"), controlled)
    print("💾 Saved controlled trajectory → phase_error_lock_v13.npy")

    plot_result(
        trajectory,
        controlled,
        rift,
        phi,
        ref_phi,
        drive,
        phase_error,
        base_layer,
        upper_layer,
        lower_layer
    )

    print("🚀 Phase Error Lock Controller V13 complete")


if __name__ == "__main__":
    main()
