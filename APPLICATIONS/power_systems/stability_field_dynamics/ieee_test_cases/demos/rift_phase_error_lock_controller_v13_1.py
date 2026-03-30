# rift_phase_error_lock_controller_v13_1.py

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
# V13.1 CONTROLLER
# --------------------------------------------------

def phase_error_lock_controller_v13_1(trajectory, rift):
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

    phi = np.zeros(len(controlled))
    ref_phi = np.zeros(len(controlled))
    target_phi = np.zeros(len(controlled))

    drive = np.zeros(len(controlled))
    phase_error_ref = np.zeros(len(controlled))
    phase_error_target = np.zeros(len(controlled))

    momentum = np.zeros_like(controlled)

    phi[0] = 0.0
    ref_phi[0] = 0.0
    target_phi[0] = np.pi

    k_layer = 1.2
    k_speed = 1.5
    k_turn = 0.9
    k_lock = 0.55
    k_target = 0.25
    k_relax = 0.08

    dt = 1.0

    for t in range(len(controlled)):

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

            y = controlled[t - 1, 1]

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

            dphi = (
                2 * np.pi * f0
                + k_layer * layer_dev * 0.025
                + k_speed * speed * 0.018
                + k_turn * turn * 0.015
                - k_lock * pe_ref
                - k_target * pe_target
                - k_relax * np.sin(pe_ref)
            )

            phi[t] = (phi[t - 1] + dphi * dt) % (2 * np.pi)

        elif t > 0:
            phi[t] = (phi[t - 1] + 2 * np.pi * f0) % (2 * np.pi)
            phase_error_ref[t] = wrap_angle(phi[t] - ref_phi[t])
            phase_error_target[t] = wrap_angle(phi[t] - target_phi[t])

        drive[t] = (
            np.sin(phi[t])
            + 0.5 * np.sin(2 * phi[t])
            + 0.3 * np.sin(3 * phi[t])
        )

        d = drive[t]
        current = controlled[t]
        rift_target = nearest_rift_point(current, rift)

        pe_abs = abs(phase_error_ref[t])

        if d > 0.35:
            target_layer = upper_layer
            target_dx = 0.028
            gain_layer = 0.40
            gain_x = 0.15
            gain_rift = 0.03
        elif d > 0.0:
            target_layer = 0.5 * (base_layer + upper_layer)
            target_dx = 0.018
            gain_layer = 0.30
            gain_x = 0.10
            gain_rift = 0.03
        elif d >= -0.35:
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

    return controlled, phi, ref_phi, target_phi, drive, phase_error_ref, phase_error_target, base_layer, upper_layer, lower_layer, f0


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    trajectory, rift = load_data()

    results = phase_error_lock_controller_v13_1(trajectory, rift)

    (controlled, phi, ref_phi, target_phi, drive,
     pe_ref, pe_target,
     base_layer, upper_layer, lower_layer, f0) = results

    np.save(os.path.join(RIFT_DIR, "phase_error_lock_v13_1.npy"), controlled)

    print("🚀 Phase Error Lock Controller V13.1 complete")


if __name__ == "__main__":
    main()
