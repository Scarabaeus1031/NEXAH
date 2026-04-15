# rift_field_navigation_controller_v20.py

import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")


# --------------------------------------------------
# LOAD
# --------------------------------------------------

def load_data():
    for name in ["trajectory.npy", "states.npy"]:
        path = os.path.join(BASE_DIR, name)
        if os.path.exists(path):
            traj = np.load(path)
            print(f"Loaded trajectory: {name}")
            break
    else:
        raise FileNotFoundError("No trajectory found")

    rift = np.load(os.path.join(RIFT_DIR, "rift_curve.npy"))
    print("Loaded rift")

    return traj[:, :2], rift


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def dominant_freq(signal):
    fft_vals = np.fft.rfft(signal)
    power = np.abs(fft_vals)
    freqs = np.fft.rfftfreq(len(signal))
    idx = np.argmax(power[1:]) + 1
    return freqs[idx]


def wrap_angle(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def smooth_signal(x, window=9):
    if window < 3:
        return x.copy()
    pad = window // 2
    xp = np.pad(x, (pad, pad), mode="edge")
    kernel = np.ones(window) / window
    return np.convolve(xp, kernel, mode="valid")


def compute_instability(traj):
    n = len(traj)
    inst = np.zeros(n)

    for t in range(2, n):
        v1 = traj[t - 1] - traj[t - 2]
        v2 = traj[t] - traj[t - 1]
        inst[t] = np.linalg.norm(v2 - v1)

    return inst


def regime_from_drive(d, high=0.30, low=-0.30):
    if d > high:
        return 1
    elif d < low:
        return -1
    return 0


# --------------------------------------------------
# LAYERS / CHANNELS
# --------------------------------------------------

def extract_layers(traj):
    y = traj[:, 1]
    y_mean = np.mean(y)
    y_std = np.std(y)

    base = y_mean
    upper = y_mean + 0.95 * y_std
    lower = y_mean - 0.65 * y_std

    print(f"Base Layer:  {base:.4f} ± {y_std:.4f}")
    print(f"Upper Layer: {upper:.4f}")
    print(f"Lower Layer: {lower:.4f}")

    return base, upper, lower


def layer_to_channel(y_target, base, upper, lower):
    vals = np.array([lower, base, upper])
    idx = np.argmin(np.abs(vals - y_target))
    return idx


def channel_radius(channel):
    # 0 = lower, 1 = base, 2 = upper
    radii = {
        0: 0.85,
        1: 1.00,
        2: 1.18,
    }
    return radii[channel]


# --------------------------------------------------
# TORUS / RING NAVIGATION
# --------------------------------------------------

def run_v20_torus_navigation(traj, rift):
    n = len(traj)

    base, upper, lower = extract_layers(traj)
    instability = compute_instability(traj)
    instability_s = smooth_signal(instability, window=11)

    f0 = dominant_freq(traj[:, 0])
    print(f"Base frequency: {f0:.4f}")

    phi = np.zeros(n)
    ref_phi = np.zeros(n)
    dphi = np.zeros(n)
    drive = np.zeros(n)
    phase_error = np.zeros(n)

    target_layer = np.zeros(n)
    target_channel = np.zeros(n, dtype=int)
    current_channel = np.zeros(n, dtype=int)
    transfer_event = np.zeros(n)

    controlled = np.zeros_like(traj)
    torus_xy = np.zeros_like(traj)

    # initialize from original
    controlled[0] = traj[0]

    # start in base channel
    current_channel[0] = 1
    target_channel[0] = 1
    target_layer[0] = base

    for t in range(1, n):
        # reference phase
        ref_phi[t] = ref_phi[t - 1] + 2 * np.pi * f0

        # drive from reference phase
        drive[t] = (
            np.sin(ref_phi[t])
            + 0.45 * np.sin(2 * ref_phi[t])
            + 0.22 * np.sin(3 * ref_phi[t])
        )

        # local instability
        inst = instability_s[t]

        # continuous target layer
        layer_field = (
            base
            + 0.85 * (upper - base) * max(drive[t], 0.0)
            - 0.85 * (base - lower) * max(-drive[t], 0.0)
        )

        # instability-triggered pull
        if inst > 0.050:
            if drive[t] > 0.20:
                layer_field = upper
            elif drive[t] < -0.20:
                layer_field = lower
            else:
                layer_field = base

        target_layer[t] = layer_field
        target_channel[t] = layer_to_channel(target_layer[t], base, upper, lower)

        # channel transfer logic
        if target_channel[t] != current_channel[t - 1]:
            if inst > 0.038 or abs(drive[t]) > 0.55:
                current_channel[t] = target_channel[t]
                transfer_event[t] = 1
            else:
                current_channel[t] = current_channel[t - 1]
        else:
            current_channel[t] = current_channel[t - 1]

        # phase feedback
        channel_bias = (current_channel[t] - 1) * 0.004
        pe = wrap_angle(phi[t - 1] - ref_phi[t - 1])
        phase_error[t] = pe

        dphi[t] = (
            2 * np.pi * f0
            + 0.018 * inst
            + 0.010 * abs(drive[t])
            + channel_bias
            - 0.060 * pe
        )

        phi[t] = phi[t - 1] + dphi[t]

        # torus / ring projection
        r = channel_radius(current_channel[t])
        torus_xy[t, 0] = r * np.cos(phi[t])
        torus_xy[t, 1] = r * np.sin(phi[t])

        # keep comparable PCA-like trajectory by blending original x with target layer
        alpha = 0.24
        controlled[t, 0] = (1 - alpha) * traj[t, 0] + alpha * torus_xy[t, 0]
        controlled[t, 1] = (1 - alpha) * traj[t, 1] + alpha * target_layer[t]

    return {
        "controlled": controlled,
        "torus_xy": torus_xy,
        "phi": phi,
        "ref_phi": ref_phi,
        "dphi": dphi,
        "drive": drive,
        "phase_error": phase_error,
        "instability": instability_s,
        "target_layer": target_layer,
        "target_channel": target_channel,
        "current_channel": current_channel,
        "transfer_event": transfer_event,
        "base": base,
        "upper": upper,
        "lower": lower,
    }


# --------------------------------------------------
# PLOTS
# --------------------------------------------------

def plot_v20_trajectory(traj, controlled, rift, base, upper, lower):
    plt.figure(figsize=(10, 7))

    plt.plot(traj[:, 0], traj[:, 1], color="blue", linewidth=2, label="original")
    plt.plot(controlled[:, 0], controlled[:, 1], color="orange", linewidth=2, label="v20 torus-nav")
    plt.plot(rift[:, 0], rift[:, 1], color="cyan", linewidth=2, alpha=0.8, label="rift")

    plt.axhline(base, color="magenta", linestyle="--", label="base layer")
    plt.axhline(upper, color="orange", linestyle="--", label="upper layer")
    plt.axhline(lower, color="purple", linestyle="--", label="lower layer")

    plt.title("V20 Torus / Ring Navigation Trajectory")
    plt.legend()
    plt.grid(True)

    path = os.path.join(RIFT_DIR, "v20_trajectory.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved → {path}")
    plt.close()


def plot_v20_phase(phi, ref_phi, drive, phase_error, dphi):
    fig, axes = plt.subplots(3, 1, figsize=(11, 10), sharex=True)

    axes[0].plot(phi, color="blue", label="phi")
    axes[0].plot(ref_phi, color="orange", label="ref phi")
    axes[0].plot(drive, color="black", label="drive")
    axes[0].set_title("V20 Phase / Reference / Drive")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(phase_error, color="red", label="phase error")
    axes[1].axhline(0, color="gray", linestyle="--")
    axes[1].set_title("V20 Phase Error")
    axes[1].legend()
    axes[1].grid(True)

    axes[2].plot(dphi, color="green", label="dphi/dt")
    axes[2].set_title("V20 Phase Velocity")
    axes[2].legend()
    axes[2].grid(True)

    path = os.path.join(RIFT_DIR, "v20_phase.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved → {path}")
    plt.close()


def plot_v20_channels(instability, target_layer, current_channel, target_channel, transfer_event, base, upper, lower):
    fig, axes = plt.subplots(3, 1, figsize=(11, 10), sharex=True)

    axes[0].plot(instability, color="darkred", label="instability")
    axes[0].set_title("V20 Local Instability")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(target_layer, color="green", label="target layer")
    axes[1].axhline(base, color="magenta", linestyle="--", label="base")
    axes[1].axhline(upper, color="orange", linestyle="--", label="upper")
    axes[1].axhline(lower, color="purple", linestyle="--", label="lower")
    axes[1].set_title("V20 Ring-Layer Targeting")
    axes[1].legend()
    axes[1].grid(True)

    axes[2].plot(current_channel, color="blue", label="current channel")
    axes[2].plot(target_channel, color="orange", label="target channel")
    axes[2].plot(transfer_event, color="red", label="transfer event")
    axes[2].set_title("V20 Ring Transfer Logic")
    axes[2].legend()
    axes[2].grid(True)

    path = os.path.join(RIFT_DIR, "v20_channels.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved → {path}")
    plt.close()


def plot_v20_torus(torus_xy, current_channel, transfer_event):
    plt.figure(figsize=(8, 8))

    for ch, color, label in [
        (0, "purple", "lower ring"),
        (1, "gold", "base ring"),
        (2, "green", "upper ring"),
    ]:
        mask = current_channel == ch
        plt.scatter(
            torus_xy[mask, 0],
            torus_xy[mask, 1],
            s=26,
            color=color,
            alpha=0.9,
            label=label
        )

    cut_mask = transfer_event > 0
    if np.any(cut_mask):
        plt.scatter(
            torus_xy[cut_mask, 0],
            torus_xy[cut_mask, 1],
            s=60,
            color="red",
            marker="x",
            label="transfer"
        )

    circle1 = plt.Circle((0, 0), channel_radius(0), fill=False, linestyle="--", alpha=0.5)
    circle2 = plt.Circle((0, 0), channel_radius(1), fill=False, linestyle="--", alpha=0.5)
    circle3 = plt.Circle((0, 0), channel_radius(2), fill=False, linestyle="--", alpha=0.5)

    ax = plt.gca()
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.add_patch(circle3)

    plt.axhline(0, color="gray", linestyle=":")
    plt.axvline(0, color="gray", linestyle=":")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.title("V20 Torus / Ring Manifold Projection")
    plt.legend()
    plt.grid(True)

    path = os.path.join(RIFT_DIR, "v20_torus.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved → {path}")
    plt.close()


# --------------------------------------------------
# SAVE
# --------------------------------------------------

def save_outputs(results):
    np.save(os.path.join(RIFT_DIR, "field_navigation_v20.npy"), results["controlled"])
    np.save(os.path.join(RIFT_DIR, "field_navigation_v20_torus.npy"), results["torus_xy"])
    print("Saved controlled trajectory → field_navigation_v20.npy")
    print("Saved torus projection   → field_navigation_v20_torus.npy")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    traj, rift = load_data()

    results = run_v20_torus_navigation(traj, rift)

    save_outputs(results)

    plot_v20_trajectory(
        traj,
        results["controlled"],
        rift,
        results["base"],
        results["upper"],
        results["lower"],
    )

    plot_v20_phase(
        results["phi"],
        results["ref_phi"],
        results["drive"],
        results["phase_error"],
        results["dphi"],
    )

    plot_v20_channels(
        results["instability"],
        results["target_layer"],
        results["current_channel"],
        results["target_channel"],
        results["transfer_event"],
        results["base"],
        results["upper"],
        results["lower"],
    )

    plot_v20_torus(
        results["torus_xy"],
        results["current_channel"],
        results["transfer_event"],
    )

    print("V20 Torus / Ring Navigation DONE")


if __name__ == "__main__":
    main()
