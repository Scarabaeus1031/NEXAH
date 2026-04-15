# rift_phase_target_controller_v14_2_smooth.py

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


def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


# --------------------------------------------------
# SMOOTH TARGET PHASE
# --------------------------------------------------

def compute_smooth_target_phase(y, base_layer, upper_layer, lower_layer):
    """
    Map y smoothly into a phase target:
    lower  -> 1.35*pi
    base   -> 1.00*pi
    upper  -> 0.35*pi

    We interpolate in two smooth segments:
    lower -> base
    base  -> upper
    """
    phi_lower = 1.35 * np.pi
    phi_base = 1.00 * np.pi
    phi_upper = 0.35 * np.pi

    if y <= base_layer:
        denom = max(base_layer - lower_layer, 1e-8)
        a = (y - lower_layer) / denom
        a = smoothstep(a)
        phi_target = (1.0 - a) * phi_lower + a * phi_base
    else:
        denom = max(upper_layer - base_layer, 1e-8)
        a = (y - base_layer) / denom
        a = smoothstep(a)
        phi_target = (1.0 - a) * phi_base + a * phi_upper

    phi_target = np.clip(phi_target, min(phi_upper, phi_lower), max(phi_upper, phi_lower))
    return phi_target


def compute_soft_regime(y, base_layer, upper_layer, lower_layer):
    mid_upper = 0.5 * (base_layer + upper_layer)
    mid_lower = 0.5 * (base_layer + lower_layer)

    if y >= mid_upper:
        return 1
    elif y <= mid_lower:
        return -1
    return 0


def regime_name(idx):
    if idx == 1:
        return "upper"
    if idx == -1:
        return "lower"
    return "base"


# --------------------------------------------------
# V14.2 SMOOTH CONTROLLER
# --------------------------------------------------

def phase_target_controller_v14_2_smooth(trajectory, rift):
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

    regime_idx = np.zeros(n, dtype=int)
    dphi_series = np.zeros(n)
    switch_flag = np.zeros(n, dtype=int)

    momentum = np.zeros_like(controlled)

    # smoother than v14.1
    k_target = 0.85
    k_ref = 0.12
    k_damp = 0.18
    k_speed = 0.06

    dt = 1.0

    phi[0] = 0.0
    ref_phi[0] = 0.0
    target_phi[0] = np.pi
    regime_idx[0] = 0

    for t in range(n):
        ref_phi[t] = (2 * np.pi * f0 * t) % (2 * np.pi)

        if t > 1:
            current_prev = controlled[t - 1]
            vel = controlled[t - 1] - controlled[t - 2]
            speed = np.linalg.norm(vel)

            y_prev = current_prev[1]

            target_phi[t] = compute_smooth_target_phase(
                y_prev, base_layer, upper_layer, lower_layer
            )
            regime_idx[t] = compute_soft_regime(
                y_prev, base_layer, upper_layer, lower_layer
            )

            if regime_idx[t] != regime_idx[t - 1]:
                switch_flag[t] = 1

            pe_target = wrap_angle(phi[t - 1] - target_phi[t])
            pe_ref = wrap_angle(phi[t - 1] - ref_phi[t - 1])

            phase_error_target[t] = pe_target
            phase_error_ref[t] = pe_ref

            dphi = (
                2 * np.pi * f0
                - k_target * pe_target
                - k_ref * pe_ref
                - k_damp * np.sin(pe_target)
                + k_speed * speed
            )

            dphi_series[t] = dphi
            phi[t] = (phi[t - 1] + dphi * dt) % (2 * np.pi)

        elif t > 0:
            target_phi[t] = target_phi[t - 1]
            regime_idx[t] = regime_idx[t - 1]
            phi[t] = (phi[t - 1] + 2 * np.pi * f0) % (2 * np.pi)
            dphi_series[t] = 2 * np.pi * f0
            phase_error_target[t] = wrap_angle(phi[t] - target_phi[t])
            phase_error_ref[t] = wrap_angle(phi[t] - ref_phi[t])

        drive[t] = phase_to_drive(phi[t])

        current = controlled[t]
        rift_target = nearest_rift_point(current, rift)
        d = drive[t]

        # smoother geometry coupling
        gain_layer = 0.22 + 0.16 * np.clip(abs(d), 0.0, 1.0)
        gain_x = 0.04 + 0.05 * max(d, 0.0)
        gain_rift = 0.010

        # smooth layer target from target phase itself
        phi_lower = 1.35 * np.pi
        phi_upper = 0.35 * np.pi
        phi_base = 1.00 * np.pi

        if target_phi[t] >= phi_base:
            denom = max(phi_lower - phi_base, 1e-8)
            a = (target_phi[t] - phi_base) / denom
            a = np.clip(a, 0.0, 1.0)
            target_layer = (1.0 - a) * base_layer + a * lower_layer
        else:
            denom = max(phi_base - phi_upper, 1e-8)
            a = (phi_base - target_phi[t]) / denom
            a = np.clip(a, 0.0, 1.0)
            target_layer = (1.0 - a) * base_layer + a * upper_layer

        target_dx = 0.006 + 0.018 * max(d, 0.0)

        pe_t_abs = abs(phase_error_target[t])
        target_boost = 1.0 + 0.5 * min(pe_t_abs / np.pi, 1.0)
        gain_layer *= target_boost

        layer_target = np.array([current[0], target_layer])
        layer_corr = gain_layer * (layer_target - current)

        x_target = np.array([current[0] + target_dx, current[1]])
        x_corr = gain_x * (x_target - current)

        rift_corr = gain_rift * (rift_target - current)

        correction = layer_corr + x_corr + rift_corr

        if t > 0:
            momentum[t] = 0.86 * momentum[t - 1] + 0.14 * correction
        else:
            momentum[t] = correction

        controlled[t] += np.tanh(momentum[t]) * 0.05

    return {
        "controlled": controlled,
        "phi": phi,
        "ref_phi": ref_phi,
        "target_phi": target_phi,
        "drive": drive,
        "phase_error_ref": phase_error_ref,
        "phase_error_target": phase_error_target,
        "regime_idx": regime_idx,
        "dphi_series": dphi_series,
        "switch_flag": switch_flag,
        "base_layer": base_layer,
        "upper_layer": upper_layer,
        "lower_layer": lower_layer,
        "f0": f0,
    }


# --------------------------------------------------
# PLOT
# --------------------------------------------------

def plot_regime_colored_trajectory(original, controlled, regime_idx,
                                   base_layer, upper_layer, lower_layer):
    plt.figure(figsize=(10, 6))

    plt.plot(original[:, 0], original[:, 1], color="lightgray", linewidth=1.4, label="original")

    colors = {
        -1: "purple",
         0: "gold",
         1: "green",
    }

    for i in range(1, len(controlled)):
        ridx = int(regime_idx[i])
        plt.plot(
            controlled[i-1:i+1, 0],
            controlled[i-1:i+1, 1],
            color=colors[ridx],
            linewidth=2.0
        )

    plt.axhline(base_layer, linestyle="--", color="magenta", label="base layer")
    plt.axhline(upper_layer, linestyle="--", color="orange", label="upper layer")
    plt.axhline(lower_layer, linestyle="--", color="purple", label="lower layer")

    plt.plot([], [], color="green", label="upper regime")
    plt.plot([], [], color="gold", label="base regime")
    plt.plot([], [], color="purple", label="lower regime")

    plt.title("V14.2 Smooth Regime-Colored Trajectory")
    plt.grid(True)
    plt.legend(loc="best")

    path = os.path.join(RIFT_DIR, "v14_2_smooth_regime_trajectory.png")
    plt.savefig(path, dpi=150)
    print(f"💾 Saved → {path}")
    plt.close()


def plot_phase_analysis(phi, ref_phi, target_phi, drive, dphi_series, switch_flag):
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    axes[0].plot(phi, label="φ", color="blue")
    axes[0].plot(ref_phi, label="ref", color="orange")
    axes[0].plot(target_phi, label="target", color="green")
    axes[0].plot(drive, label="drive", color="black", alpha=0.6)

    switch_times = np.where(switch_flag == 1)[0]
    for t in switch_times:
        axes[0].axvline(t, color="red", linestyle="--", alpha=0.25)

    axes[0].set_title("V14.2 Smooth Phase / Reference / Target / Drive")
    axes[0].grid(True)
    axes[0].legend(loc="best")

    axes[1].plot(dphi_series, color="darkred", label="dphi / dt")
    for t in switch_times:
        axes[1].axvline(t, color="red", linestyle="--", alpha=0.25)

    axes[1].set_title("V14.2 Smooth Phase Velocity")
    axes[1].grid(True)
    axes[1].legend(loc="best")
    axes[1].set_xlabel("time step")

    plt.tight_layout()
    path = os.path.join(RIFT_DIR, "v14_2_smooth_phase_analysis.png")
    plt.savefig(path, dpi=150)
    print(f"💾 Saved → {path}")
    plt.close()


def plot_error_analysis(phase_error_ref, phase_error_target, switch_flag):
    plt.figure(figsize=(12, 4))

    plt.plot(phase_error_ref, label="ref error", color="blue")
    plt.plot(phase_error_target, label="target error", color="orange")
    plt.axhline(0.0, linestyle="--", color="gray")

    switch_times = np.where(switch_flag == 1)[0]
    for t in switch_times:
        plt.axvline(t, color="red", linestyle="--", alpha=0.25)

    plt.title("V14.2 Smooth Errors + Regime Switches")
    plt.grid(True)
    plt.legend(loc="best")

    path = os.path.join(RIFT_DIR, "v14_2_smooth_error_analysis.png")
    plt.savefig(path, dpi=150)
    print(f"💾 Saved → {path}")
    plt.close()


def save_regime_summary(regime_idx, switch_flag):
    switch_times = np.where(switch_flag == 1)[0].tolist()

    unique, counts = np.unique(regime_idx, return_counts=True)
    count_map = {int(k): int(v) for k, v in zip(unique, counts)}

    lines = []
    lines.append("# V14.2 Smooth Regime Summary\n")
    lines.append(f"Total steps: {len(regime_idx)}\n")
    lines.append(f"Total regime switches: {int(np.sum(switch_flag))}\n")
    lines.append(f"Switch times: {switch_times}\n\n")

    lines.append("## Regime occupancy\n")
    for idx in [-1, 0, 1]:
        lines.append(f"- {regime_name(idx)} ({idx}): {count_map.get(idx, 0)}\n")

    path = os.path.join(RIFT_DIR, "v14_2_smooth_regime_summary.md")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"💾 Saved → {path}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    trajectory, rift = load_data()
    result = phase_target_controller_v14_2_smooth(trajectory, rift)

    np.save(os.path.join(RIFT_DIR, "phase_target_v14_2_smooth.npy"), result["controlled"])
    print("💾 Saved controlled trajectory → phase_target_v14_2_smooth.npy")

    plot_regime_colored_trajectory(
        trajectory,
        result["controlled"],
        result["regime_idx"],
        result["base_layer"],
        result["upper_layer"],
        result["lower_layer"],
    )

    plot_phase_analysis(
        result["phi"],
        result["ref_phi"],
        result["target_phi"],
        result["drive"],
        result["dphi_series"],
        result["switch_flag"],
    )

    plot_error_analysis(
        result["phase_error_ref"],
        result["phase_error_target"],
        result["switch_flag"],
    )

    save_regime_summary(
        result["regime_idx"],
        result["switch_flag"],
    )

    print("🚀 V14.2 smooth analysis complete")


if __name__ == "__main__":
    main()
