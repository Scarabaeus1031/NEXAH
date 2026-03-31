# rift_field_navigation_controller_v19.py

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
            print(f"Loaded trajectory: {name}")
            break

    if trajectory is None:
        raise FileNotFoundError("No trajectory file found")

    rift_path = os.path.join(RIFT_DIR, "rift_curve.npy")
    if not os.path.exists(rift_path):
        raise FileNotFoundError("No rift_curve.npy found")

    rift = np.load(rift_path)
    print("Loaded rift")

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


def estimate_layers(traj):
    pc2 = traj[:, 1]
    center = np.median(pc2)
    spread = np.std(pc2)

    base_layer = center
    upper_layer = center + 0.95 * spread
    lower_layer = center - 0.65 * spread

    print(f"Base Layer: {center:.4f} ± {spread:.4f}")
    print(f"Upper Layer: {upper_layer:.4f}")
    print(f"Lower Layer: {lower_layer:.4f}")

    return base_layer, upper_layer, lower_layer, spread


def nearest_rift_point(p, rift):
    dists = np.linalg.norm(rift - p, axis=1)
    return rift[np.argmin(dists)]


def wrap_angle(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def safe_normalize(v):
    n = np.linalg.norm(v)
    if n < 1e-12:
        return np.zeros_like(v)
    return v / n


def compute_local_flow(controlled, t):
    if t < 2:
        return np.array([1.0, 0.0])

    v1 = controlled[t - 1] - controlled[t - 2]

    if t >= 3:
        v2 = controlled[t - 2] - controlled[t - 3]
        flow = 0.72 * v1 + 0.28 * v2
    else:
        flow = v1

    return safe_normalize(flow)


def compute_instability(controlled, t):
    if t < 3:
        return 0.0

    v_now = controlled[t - 1] - controlled[t - 2]
    v_prev = controlled[t - 2] - controlled[t - 3]

    speed_now = np.linalg.norm(v_now)
    speed_prev = np.linalg.norm(v_prev)

    speed_jump = abs(speed_now - speed_prev)
    turn = np.linalg.norm(v_now - v_prev)

    return speed_jump + turn


def smooth_gate(x, sharpness=8.0):
    return 0.5 * (1.0 + np.tanh(sharpness * x))


def layer_index(y, lower_layer, base_layer, upper_layer):
    refs = np.array([lower_layer, base_layer, upper_layer])
    return int(np.argmin(np.abs(refs - y)))


def choose_target_channel(
    drive_value,
    phase_error,
    instability,
    current_channel,
    lower_layer,
    base_layer,
    upper_layer
):
    """
    Channel logic:
    0 = lower
    1 = base
    2 = upper
    """

    layers = np.array([lower_layer, base_layer, upper_layer])

    # strong positive drive → upper tendency
    if drive_value > 0.45:
        preferred = 2
    # strong negative drive → lower tendency
    elif drive_value < -0.45:
        preferred = 0
    else:
        preferred = 1

    # escape trigger:
    # if instability and phase error are both elevated,
    # allow adjacent transfer away from current channel
    escape_strength = abs(phase_error) + 2.2 * instability

    if escape_strength > 0.42:
        if drive_value >= 0 and current_channel < 2:
            preferred = current_channel + 1
        elif drive_value < 0 and current_channel > 0:
            preferred = current_channel - 1

    return preferred, layers[preferred], escape_strength


# --------------------------------------------------
# V19 CHANNEL + ESCAPE FIELD NAVIGATION
# --------------------------------------------------

def field_navigation_controller_v19(trajectory, rift):
    controlled = trajectory.copy()

    pc1 = trajectory[:, 0]
    pc2 = trajectory[:, 1]

    f1 = dominant_freq(pc1)
    f2 = dominant_freq(pc2)
    f0 = 0.5 * (f1 + f2)

    base_layer, upper_layer, lower_layer, spread = estimate_layers(trajectory)
    print(f"Base frequency: {f0:.4f}")

    n = len(controlled)

    phi = np.zeros(n)
    ref_phi = np.zeros(n)
    drive = np.zeros(n)
    phase_error = np.zeros(n)
    dphi_series = np.zeros(n)

    momentum = np.zeros_like(controlled)
    instability_series = np.zeros(n)
    target_layers = np.zeros(n)
    target_channels = np.zeros(n, dtype=int)
    current_channels = np.zeros(n, dtype=int)
    escape_strengths = np.zeros(n)
    transfer_events = np.zeros(n)

    flow_vectors = np.zeros_like(controlled)

    rng = np.random.default_rng(1033)

    phi[0] = 0.0
    current_channels[0] = layer_index(controlled[0, 1], lower_layer, base_layer, upper_layer)

    # ----------------------------------------------
    # V19 parameters
    # ----------------------------------------------
    alpha_flow = 0.38
    beta_layer = 0.34
    gamma_forward = 0.15
    delta_instab = 0.22
    rho_rift = 0.05
    eta_explore = 0.08

    k_lock = 0.045
    k_relax = 0.03
    k_speed = 0.014
    k_turn = 0.010
    k_drive_phase = 0.022
    k_layer_phase = 0.018

    # new V19
    transfer_gain = 0.24
    escape_gain = 0.20
    ring2_gain = 0.08   # second ring smoothing shell

    dt = 1.0

    for t in range(n):
        ref_phi[t] = (2 * np.pi * f0 * t) % (2 * np.pi)

        if t > 0:
            pe = wrap_angle(phi[t - 1] - ref_phi[t - 1])
            phase_error[t] = pe

            if t >= 2:
                local_vel = controlled[t - 1] - controlled[t - 2]
                speed = np.linalg.norm(local_vel)
            else:
                speed = 0.0

            if t >= 3:
                v_now = controlled[t - 1] - controlled[t - 2]
                v_prev = controlled[t - 2] - controlled[t - 3]
                turn = np.linalg.norm(v_now - v_prev)
            else:
                turn = 0.0

            dphi = (
                2 * np.pi * f0
                + k_speed * speed
                + k_turn * turn
                + k_drive_phase * np.sin(phi[t - 1])
                + k_layer_phase * np.cos(phi[t - 1])
                - k_lock * pe
                - k_relax * np.sin(pe)
                + 0.002 * rng.normal()
            )

            dphi_series[t] = dphi
            phi[t] = (phi[t - 1] + dphi * dt) % (2 * np.pi)

        drive[t] = (
            np.sin(phi[t])
            + 0.5 * np.sin(2 * phi[t])
            + 0.3 * np.sin(3 * phi[t])
        )

        current = controlled[t]
        rift_target = nearest_rift_point(current, rift)

        # ------------------------------------------
        # FLOW
        # ------------------------------------------
        flow_dir = compute_local_flow(controlled, t)
        flow_vectors[t] = flow_dir
        flow_force = alpha_flow * flow_dir

        # ------------------------------------------
        # INSTABILITY
        # ------------------------------------------
        instability = compute_instability(controlled, t)
        instability_series[t] = instability

        if t >= 2:
            local_vel = controlled[t - 1] - controlled[t - 2]
            instability_force = -delta_instab * instability * safe_normalize(local_vel)
        else:
            instability_force = np.zeros(2)

        # ------------------------------------------
        # CURRENT CHANNEL
        # ------------------------------------------
        current_channel = layer_index(current[1], lower_layer, base_layer, upper_layer)
        current_channels[t] = current_channel

        target_channel, target_layer, escape_strength = choose_target_channel(
            drive[t],
            phase_error[t],
            instability,
            current_channel,
            lower_layer,
            base_layer,
            upper_layer
        )

        target_channels[t] = target_channel
        target_layers[t] = target_layer
        escape_strengths[t] = escape_strength

        transfer_active = 1.0 if target_channel != current_channel else 0.0
        transfer_events[t] = transfer_active

        # ------------------------------------------
        # LAYER FORCE
        # ------------------------------------------
        layer_force = beta_layer * np.array([0.0, target_layer - current[1]])

        # ------------------------------------------
        # TRANSFER FORCE (channel jump tendency)
        # ------------------------------------------
        transfer_force = transfer_gain * transfer_active * np.array([0.0, target_layer - current[1]])

        # ------------------------------------------
        # ESCAPE FORCE
        # small x/y deflection if instability + phase error are high
        # ------------------------------------------
        perp = np.array([-flow_dir[1], flow_dir[0]])
        escape_mod = smooth_gate(escape_strength - 0.42, sharpness=10.0)
        escape_force = escape_gain * escape_mod * np.sign(drive[t] + 1e-9) * perp

        # ------------------------------------------
        # SECOND RING SMOOTHING
        # interpret as outer shell that redistributes energy
        # ------------------------------------------
        ring2_force = ring2_gain * np.array([
            np.cos(phi[t]) * 0.25,
            np.sin(phi[t]) * 0.25
        ])

        # ------------------------------------------
        # FORWARD DRIFT
        # ------------------------------------------
        forward_force = gamma_forward * np.array([1.0, 0.0])

        # ------------------------------------------
        # LIGHT EXPLORATION
        # ------------------------------------------
        explore_force = eta_explore * np.sin(phi[t]) * perp

        # ------------------------------------------
        # RIFT TETHER
        # ------------------------------------------
        rift_force = rho_rift * (rift_target - current)

        correction = (
            flow_force
            + layer_force
            + transfer_force
            + escape_force
            + ring2_force
            + forward_force
            + explore_force
            + instability_force
            + rift_force
        )

        if t > 0:
            momentum[t] = 0.80 * momentum[t - 1] + 0.20 * correction
        else:
            momentum[t] = correction

        controlled[t] += np.tanh(momentum[t]) * 0.05

    return {
        "controlled": controlled,
        "phi": phi,
        "ref_phi": ref_phi,
        "drive": drive,
        "phase_error": phase_error,
        "dphi": dphi_series,
        "flow_vectors": flow_vectors,
        "instability": instability_series,
        "target_layers": target_layers,
        "current_channels": current_channels,
        "target_channels": target_channels,
        "escape_strengths": escape_strengths,
        "transfer_events": transfer_events,
        "base_layer": base_layer,
        "upper_layer": upper_layer,
        "lower_layer": lower_layer,
        "f0": f0,
    }


# --------------------------------------------------
# PLOTS
# --------------------------------------------------

def plot_trajectory(original, controlled, rift, base_layer, upper_layer, lower_layer):
    plt.figure(figsize=(10, 6))

    plt.plot(original[:, 0], original[:, 1], label="original", color="blue")
    plt.plot(controlled[:, 0], controlled[:, 1], label="v19 field-nav", color="orange")
    plt.plot(rift[:, 0], rift[:, 1], label="rift", color="cyan", alpha=0.6)

    plt.axhline(base_layer, linestyle="--", color="magenta", label="base layer")
    plt.axhline(upper_layer, linestyle="--", color="orange", label="upper layer")
    plt.axhline(lower_layer, linestyle="--", color="purple", label="lower layer")

    plt.legend()
    plt.grid(True)
    plt.title("V19 Channel + Escape Navigation Trajectory")

    path = os.path.join(RIFT_DIR, "v19_trajectory.png")
    plt.savefig(path, dpi=150)
    print(f"Saved → {path}")
    plt.close()


def plot_phase(phi, ref_phi, drive, phase_error, dphi):
    fig, axes = plt.subplots(3, 1, figsize=(11, 9), sharex=True)

    axes[0].plot(phi, label="phi", color="blue")
    axes[0].plot(ref_phi, label="ref phi", color="orange")
    axes[0].plot(drive, label="drive", color="black", alpha=0.75)
    axes[0].set_title("V19 Phase / Reference / Drive")
    axes[0].grid(True)
    axes[0].legend()

    axes[1].plot(phase_error, color="red", label="phase error")
    axes[1].axhline(0.0, linestyle="--", color="gray")
    axes[1].set_title("V19 Phase Error")
    axes[1].grid(True)
    axes[1].legend()

    axes[2].plot(dphi, color="darkgreen", label="dphi/dt")
    axes[2].set_title("V19 Phase Velocity")
    axes[2].grid(True)
    axes[2].legend()

    path = os.path.join(RIFT_DIR, "v19_phase.png")
    plt.savefig(path, dpi=150)
    print(f"Saved → {path}")
    plt.close()


def plot_channels_and_instability(
    instability,
    target_layers,
    current_channels,
    target_channels,
    transfer_events,
    base_layer,
    upper_layer,
    lower_layer
):
    fig, axes = plt.subplots(3, 1, figsize=(11, 10), sharex=True)

    axes[0].plot(instability, color="darkred", label="instability")
    axes[0].set_title("V19 Local Instability")
    axes[0].grid(True)
    axes[0].legend()

    axes[1].plot(target_layers, color="green", label="target layer")
    axes[1].axhline(base_layer, linestyle="--", color="magenta", label="base")
    axes[1].axhline(upper_layer, linestyle="--", color="orange", label="upper")
    axes[1].axhline(lower_layer, linestyle="--", color="purple", label="lower")
    axes[1].set_title("V19 Channel Targeting")
    axes[1].grid(True)
    axes[1].legend()

    axes[2].plot(current_channels, label="current channel", color="blue")
    axes[2].plot(target_channels, label="target channel", color="orange")
    axes[2].plot(transfer_events, label="transfer event", color="red", alpha=0.7)
    axes[2].set_title("V19 Channel Transfer Logic")
    axes[2].grid(True)
    axes[2].legend()

    path = os.path.join(RIFT_DIR, "v19_channels.png")
    plt.savefig(path, dpi=150)
    print(f"Saved → {path}")
    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    trajectory, rift = load_data()

    result = field_navigation_controller_v19(trajectory, rift)

    np.save(os.path.join(RIFT_DIR, "field_navigation_v19.npy"), result["controlled"])
    print("Saved controlled trajectory → field_navigation_v19.npy")

    plot_trajectory(
        trajectory,
        result["controlled"],
        rift,
        result["base_layer"],
        result["upper_layer"],
        result["lower_layer"],
    )

    plot_phase(
        result["phi"],
        result["ref_phi"],
        result["drive"],
        result["phase_error"],
        result["dphi"],
    )

    plot_channels_and_instability(
        result["instability"],
        result["target_layers"],
        result["current_channels"],
        result["target_channels"],
        result["transfer_events"],
        result["base_layer"],
        result["upper_layer"],
        result["lower_layer"],
    )

    print("V19 Channel + Escape Navigation DONE")


if __name__ == "__main__":
    main()
