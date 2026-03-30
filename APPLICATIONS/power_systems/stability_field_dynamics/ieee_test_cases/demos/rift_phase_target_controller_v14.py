# rift_phase_target_controller_v14.py

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


def phase_to_drive(phi):
    return (
        1.00 * np.sin(phi) +
        0.50 * np.sin(2 * phi) +
        0.30 * np.sin(3 * phi)
    )


# --------------------------------------------------
# TARGET REGIME MAPPING
# --------------------------------------------------

def compute_target_phase(y, base_layer, upper_layer, lower_layer, spread):
    mid_upper = 0.5 * (base_layer + upper_layer)
    mid_lower = 0.5 * (base_layer + lower_layer)

    if y >= mid_upper:
        regime = "upper"
        phi_target = 0.35 * np.pi
    elif y <= mid_lower:
        regime = "lower"
        phi_target = 1.35 * np.pi
    else:
        regime = "base"
        phi_target = np.pi

    return phi_target, regime


# --------------------------------------------------
# V14 PHASE TARGET CONTROLLER
# --------------------------------------------------

def phase_target_controller_v14(trajectory, rift):
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

    n = len(controlled)

    phi = np.zeros(n)
    ref_phi = np.zeros(n)
    target_phi = np.zeros(n)
    drive = np.zeros(n)

    phase_error_ref = np.zeros(n)
    phase_error_target = np.zeros(n)

    layer_index = np.zeros(n, dtype=int)   # -1 lower, 0 base, +1 upper
    momentum = np.zeros_like(controlled)

    # --------------------------------------------------
    # KEY V14 SETTINGS
    # --------------------------------------------------
    k_target = 1.10   # primary control
    k_ref = 0.15      # weak stabilizer only
    k_damp = 0.10     # smooth phase overshoot
    k_speed = 0.08    # motion-sensitive phase modulation

    dt = 1.0

    phi[0] = 0.0
    ref_phi[0] = 0.0
    target_phi[0] = np.pi

    for t in range(n):
        ref_phi[t] = (2 * np.pi * f0 * t) % (2 * np.pi)

        if t > 1:
            current_prev = controlled[t - 1]
            vel = controlled[t - 1] - controlled[t - 2]
            speed = np.linalg.norm(vel)

            phi_target, regime = compute_target_phase(
                current_prev[1], base_layer, upper_layer, lower_layer, spread
            )
            target_phi[t] = phi_target

            if regime == "upper":
                layer_index[t] = 1
            elif regime == "lower":
                layer_index[t] = -1
            else:
                layer_index[t] = 0

            pe_target = wrap_angle(phi[t - 1] - target_phi[t])
            pe_ref = wrap_angle(phi[t - 1] - ref_phi[t - 1])

            phase_error_target[t] = pe_target
            phase_error_ref[t] = pe_ref

            # --------------------------------------------------
            # V14 CORE:
            # phase is driven primarily toward target phase
            # --------------------------------------------------
            dphi = (
                2 * np.pi * f0
                - k_target * pe_target
                - k_ref * pe_ref
                - k_damp * np.sin(pe_target)
                + k_speed * speed
            )

            phi[t] = (phi[t - 1] + dphi * dt) % (2 * np.pi)

        elif t > 0:
            target_phi[t] = target_phi[t - 1]
            phi[t] = (phi[t - 1] + 2 * np.pi * f0) % (2 * np.pi)
            phase_error_target[t] = wrap_angle(phi[t] - target_phi[t])
            phase_error_ref[t] = wrap_angle(phi[t] - ref_phi[t])

        drive[t] = phase_to_drive(phi[t])

        current = controlled[t]
        rift_target = nearest_rift_point(current, rift)
        d = drive[t]

        # --------------------------------------------------
        # Layer target chosen from phase regime
        # --------------------------------------------------
        if d > 0.35:
            target_layer = upper_layer
            target_dx = 0.025
            gain_layer = 0.42
            gain_x = 0.11
            gain_rift = 0.015
        elif 0.0 < d <= 0.35:
            target_layer = 0.5 * (base_layer + upper_layer)
            target_dx = 0.016
            gain_layer = 0.32
            gain_x = 0.08
            gain_rift = 0.015
        elif -0.35 <= d <= 0.0:
            target_layer = base_layer
            target_dx = 0.010
            gain_layer = 0.26
            gain_x = 0.05
            gain_rift = 0.010
        else:
            target_layer = lower_layer
            target_dx = 0.004
            gain_layer = 0.40
            gain_x = 0.03
            gain_rift = 0.010

        pe_t_abs = abs(phase_error_target[t])

        # stronger layer pull when target phase is missed
        target_boost = 1.0 + min(pe_t_abs / np.pi, 1.0) * 0.9
        gain_layer *= target_boost

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

        controlled[t] += np.tanh(momentum[t]) * 0.05

    return (
        controlled,
        phi,
        ref_phi,
        target_phi,
        drive,
        phase_error_ref,
        phase_error_target,
        layer_index,
        base_layer,
        upper_layer,
        lower_layer,
        f0
    )


# --------------------------------------------------
# PLOT
# --------------------------------------------------

def plot_result(original, controlled, rift,
                phi, ref_phi, target_phi, drive,
                phase_error_ref, phase_error_target,
                base_layer, upper_layer, lower_layer):

    # 1. trajectory
    plt.figure(figsize=(10, 6))
    plt.plot(original[:, 0], original[:, 1], label="original", color="blue")
    plt.plot(controlled[:, 0], controlled[:, 1], label="v14", color="orange")
    plt.plot(rift[:, 0], rift[:, 1], label="rift", color="cyan", alpha=0.6)

    plt.axhline(base_layer, linestyle="--", color="magenta", label="base layer")
    plt.axhline(upper_layer, linestyle="--", color="orange", label="upper layer")
    plt.axhline(lower_layer, linestyle="--", color="purple", label="lower layer")

    plt.legend()
    plt.grid(True)
    plt.title("Trajectory (V14 Phase Target Control)")
    path = os.path.join(RIFT_DIR, "v14_trajectory.png")
    plt.savefig(path, dpi=150)
    print(f"💾 Saved → {path}")
    plt.close()

    # 2. phase
    plt.figure(figsize=(10, 4))
    plt.plot(phi, label="φ", color="blue")
    plt.plot(ref_phi, label="ref", color="orange")
    plt.plot(target_phi, label="target", color="green")
    plt.plot(drive, label="drive", color="black", alpha=0.6)

    plt.legend()
    plt.grid(True)
    plt.title("Phase / Reference / Target / Drive (V14)")
    path = os.path.join(RIFT_DIR, "v14_phase.png")
    plt.savefig(path, dpi=150)
    print(f"💾 Saved → {path}")
    plt.close()

    # 3. errors
    plt.figure(figsize=(10, 3))
    plt.plot(phase_error_ref, label="ref error", color="blue")
    plt.plot(phase_error_target, label="target error", color="orange")
    plt.axhline(0.0, linestyle="--", color="gray")
    plt.legend()
    plt.grid(True)
    plt.title("Phase Errors (V14)")
    path = os.path.join(RIFT_DIR, "v14_errors.png")
    plt.savefig(path, dpi=150)
    print(f"💾 Saved → {path}")
    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    trajectory, rift = load_data()

    results = phase_target_controller_v14(trajectory, rift)

    (controlled, phi, ref_phi, target_phi, drive,
     pe_ref, pe_target, layer_index,
     base_layer, upper_layer, lower_layer, f0) = results

    np.save(os.path.join(RIFT_DIR, "phase_target_v14.npy"), controlled)
    print("💾 Saved controlled trajectory → phase_target_v14.npy")

    plot_result(
        trajectory,
        controlled,
        rift,
        phi,
        ref_phi,
        target_phi,
        drive,
        pe_ref,
        pe_target,
        base_layer,
        upper_layer,
        lower_layer
    )

    print("🚀 V14 Phase Target Controller complete")


if __name__ == "__main__":
    main()
