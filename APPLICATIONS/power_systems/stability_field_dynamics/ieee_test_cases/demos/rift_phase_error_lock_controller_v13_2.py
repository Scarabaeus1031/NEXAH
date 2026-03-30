# rift_phase_error_lock_controller_v13_2.py

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
# V13.2 CONTROLLER (TARGET DOMINANCE)
# --------------------------------------------------

def phase_error_lock_controller_v13_2(trajectory, rift):
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

    phi = np.zeros(len(controlled))
    ref_phi = np.zeros(len(controlled))
    target_phi = np.zeros(len(controlled))

    drive = np.zeros(len(controlled))
    phase_error_ref = np.zeros(len(controlled))
    phase_error_target = np.zeros(len(controlled))

    momentum = np.zeros_like(controlled)

    target_phi[0] = np.pi

    # 🔥 KEY CHANGE (Target Dominance)
    k_lock = 0.35     # reference weaker
    k_target = 0.75   # target stronger

    for t in range(len(controlled)):

        ref_phi[t] = (2 * np.pi * f0 * t) % (2 * np.pi)

        if t > 1:
            y = controlled[t - 1, 1]

            # --------------------------
            # TARGET REGIME MAPPING
            # --------------------------
            if y > base_layer + 0.3 * spread:
                target_phi[t] = 0.35 * np.pi
            elif y < base_layer - 0.3 * spread:
                target_phi[t] = 1.35 * np.pi
            else:
                target_phi[t] = np.pi

            pe_ref = wrap_angle(phi[t - 1] - ref_phi[t - 1])
            pe_target = wrap_angle(phi[t - 1] - target_phi[t - 1])

            phase_error_ref[t] = pe_ref
            phase_error_target[t] = pe_target

            # 🔥 TARGET DOMINANT UPDATE
            dphi = (
                2 * np.pi * f0
                - k_lock * pe_ref
                - k_target * pe_target
            )

            phi[t] = (phi[t - 1] + dphi) % (2 * np.pi)

        elif t > 0:
            phi[t] = (phi[t - 1] + 2 * np.pi * f0) % (2 * np.pi)

        # --------------------------
        # DRIVE
        # --------------------------
        drive[t] = np.sin(phi[t])

        # --------------------------
        # GEOMETRIC CORRECTION
        # --------------------------
        d = drive[t]
        current = controlled[t]
        rift_target = nearest_rift_point(current, rift)

        # stronger vertical response
        correction = np.array([
            0.01,
            0.035 * d
        ])

        # mild rift attraction
        correction += 0.01 * (rift_target - current)

        if t > 0:
            momentum[t] = 0.8 * momentum[t - 1] + 0.2 * correction
        else:
            momentum[t] = correction

        controlled[t] += np.tanh(momentum[t]) * 0.05

    return controlled, phi, ref_phi, target_phi, drive, phase_error_ref, phase_error_target, base_layer, upper_layer, lower_layer


# --------------------------------------------------
# PLOT
# --------------------------------------------------

def plot_result(original, controlled, rift,
                phi, ref_phi, target_phi,
                phase_error_ref, phase_error_target,
                base_layer, upper_layer, lower_layer):

    # TRAJECTORY
    plt.figure(figsize=(10, 6))
    plt.plot(original[:, 0], original[:, 1], label="original")
    plt.plot(controlled[:, 0], controlled[:, 1], label="v13.2", color="orange")
    plt.axhline(base_layer, linestyle="--")
    plt.axhline(upper_layer, linestyle="--")
    plt.axhline(lower_layer, linestyle="--")
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join(RIFT_DIR, "v13_2_trajectory.png"))
    plt.close()

    # PHASE
    plt.figure(figsize=(10, 4))
    plt.plot(phi, label="φ")
    plt.plot(ref_phi, label="ref")
    plt.plot(target_phi, label="target")
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join(RIFT_DIR, "v13_2_phase.png"))
    plt.close()

    # ERRORS
    plt.figure(figsize=(10, 3))
    plt.plot(phase_error_ref, label="ref error")
    plt.plot(phase_error_target, label="target error")
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join(RIFT_DIR, "v13_2_errors.png"))
    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    trajectory, rift = load_data()

    results = phase_error_lock_controller_v13_2(trajectory, rift)

    (controlled, phi, ref_phi, target_phi,
     drive, pe_ref, pe_target,
     base_layer, upper_layer, lower_layer) = results

    plot_result(
        trajectory,
        controlled,
        rift,
        phi,
        ref_phi,
        target_phi,
        pe_ref,
        pe_target,
        base_layer,
        upper_layer,
        lower_layer
    )

    print("🚀 V13.2 (Target Dominance) DONE")


if __name__ == "__main__":
    main()
