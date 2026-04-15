# rift_field_navigation_controller_v17.py

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


def estimate_layer(traj):
    pc2 = traj[:, 1]
    center = np.median(pc2)
    spread = np.std(pc2)
    print(f"Base Layer: {center:.4f} ± {spread:.4f}")
    return center, spread


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
    """
    Estimate local flow from recent motion.
    """
    if t < 2:
        return np.array([1.0, 0.0])

    v1 = controlled[t - 1] - controlled[t - 2]

    if t >= 3:
        v2 = controlled[t - 2] - controlled[t - 3]
        flow = 0.7 * v1 + 0.3 * v2
    else:
        flow = v1

    return safe_normalize(flow)


def compute_instability(controlled, t):
    """
    Simple local instability estimate:
    curvature + speed change
    """
    if t < 3:
        return 0.0

    v_now = controlled[t - 1] - controlled[t - 2]
    v_prev = controlled[t - 2] - controlled[t - 3]

    speed_now = np.linalg.norm(v_now)
    speed_prev = np.linalg.norm(v_prev)

    speed_jump = abs(speed_now - speed_prev)
    turn = np.linalg.norm(v_now - v_prev)

    return speed_jump + turn


# --------------------------------------------------
# V17 FIELD NAVIGATION CONTROLLER
# --------------------------------------------------

def field_navigation_controller_v17(trajectory, rift):
    controlled = trajectory.copy()

    pc1 = trajectory[:, 0]
    pc2 = trajectory[:, 1]

    f1 = dominant_freq(pc1)
    f2 = dominant_freq(pc2)
    f0 = 0.5 * (f1 + f2)

    base_layer, spread = estimate_layer(trajectory)
    upper_layer = base_layer + 0.95 * spread
    lower_layer = base_layer - 0.65 * spread

    print(f"Base frequency: {f0:.4f}")
    print(f"Upper Layer: {upper_layer:.4f}")
    print(f"Lower Layer: {lower_layer:.4f}")

    n = len(controlled)

    phi = np.zeros(n)
    ref_phi = np.zeros(n)
    drive = np.zeros(n)
    phase_error = np.zeros(n)

    momentum = np.zeros_like(controlled)

    # ----------------------------------------------
    # V17 weights
    # ----------------------------------------------
    alpha_flow = 0.42      # follow local field
    beta_layer = 0.32      # soft layer retention
    gamma_forward = 0.18   # forward progression
    delta_instab = 0.22    # instability damping
    rho_rift = 0.08        # weak tether only
    k_lock = 0.25          # weak phase lock
    k_relax = 0.05         # smooth phase return

    dt = 1.0

    phi[0] = 0.0
    ref_phi[0] = 0.0

    # diagnostics
    flow_vectors = np.zeros_like(controlled)
    instability_series = np.zeros(n)
    target_layers = np.zeros(n)

    for t in range(n):
        ref_phi[t] = (2 * np.pi * f0 * t) % (2 * np.pi)

        if t > 1:
            pe = wrap_angle(phi[t - 1] - ref_phi[t - 1])
            phase_error[t] = pe

            # weak phase correction only
            dphi = (
                2 * np.pi * f0
                - k_lock * pe
                - k_relax * np.sin(pe)
            )

            phi[t] = (phi[t - 1] + dphi * dt) % (2 * np.pi)

        elif t > 0:
            phi[t] = (phi[t - 1] + 2 * np.pi * f0) % (2 * np.pi)
            phase_error[t] = wrap_angle(phi[t] - ref_phi[t])

        # multi-frequency phase drive stays as internal modulation
        drive[t] = (
            np.sin(phi[t])
            + 0.5 * np.sin(2 * phi[t])
            + 0.3 * np.sin(3 * phi[t])
        )

        current = controlled[t]
        rift_target = nearest_rift_point(current, rift)

        # ------------------------------------------
        # 1. FLOW FIELD
        # ------------------------------------------
        flow_dir = compute_local_flow(controlled, t)
        flow_vectors[t] = flow_dir

        flow_force = alpha_flow * flow_dir

        # ------------------------------------------
        # 2. SOFT LAYER LOCK
        # phase modulates preferred band
        # ------------------------------------------
        d = drive[t]

        if d > 0.35:
            target_layer = upper_layer
        elif d > 0.0:
            target_layer = 0.5 * (base_layer + upper_layer)
        elif d >= -0.35:
            target_layer = base_layer
        else:
            target_layer = lower_layer

        target_layers[t] = target_layer

        layer_force = beta_layer * np.array([0.0, target_layer - current[1]])

        # ------------------------------------------
        # 3. FORWARD DRIFT
        # prefer positive x progression
        # ------------------------------------------
        forward_force = gamma_forward * np.array([1.0, 0.0])

        # ------------------------------------------
        # 4. INSTABILITY DAMPING
        # oppose local turning / jumping
        # ------------------------------------------
        instability = compute_instability(controlled, t)
        instability_series[t] = instability

        if t >= 2:
            local_vel = controlled[t - 1] - controlled[t - 2]
            instability_force = -delta_instab * instability * safe_normalize(local_vel)
        else:
            instability_force = np.zeros(2)

        # ------------------------------------------
        # 5. WEAK RIFT TETHER
        # no longer target, only soft geometric hint
        # ------------------------------------------
        rift_force = rho_rift * (rift_target - current)

        correction = (
            flow_force
            + layer_force
            + forward_force
            + instability_force
            + rift_force
        )

        if t > 0:
            momentum[t] = 0.84 * momentum[t - 1] + 0.16 * correction
        else:
            momentum[t] = correction

        controlled[t] += np.tanh(momentum[t]) * 0.05

    return {
        "controlled": controlled,
        "phi": phi,
        "ref_phi": ref_phi,
        "drive": drive,
        "phase_error": phase_error,
        "base_layer": base_layer,
        "upper_layer": upper_layer,
        "lower_layer": lower_layer,
        "flow_vectors": flow_vectors,
        "instability": instability_series,
        "target_layers": target_layers,
        "f0": f0,
    }


# --------------------------------------------------
# PLOTS
# --------------------------------------------------

def plot_trajectory(original, controlled, rift, base_layer, upper_layer, lower_layer):
    plt.figure(figsize=(10, 6))

    plt.plot(original[:, 0], original[:, 1], label="original", color="blue")
    plt.plot(controlled[:, 0], controlled[:, 1], label="v17 field-nav", color="orange")
    plt.plot(rift[:, 0], rift[:, 1], label="rift", color="cyan", alpha=0.6)

    plt.axhline(base_layer, linestyle="--", color="magenta", label="base layer")
    plt.axhline(upper_layer, linestyle="--", color="orange", label="upper layer")
    plt.axhline(lower_layer, linestyle="--", color="purple", label="lower layer")

    plt.legend()
    plt.grid(True)
    plt.title("V17 Field Navigation Trajectory")

    path = os.path.join(RIFT_DIR, "v17_trajectory.png")
    plt.savefig(path, dpi=150)
    print(f"Saved → {path}")
    plt.close()


def plot_phase(phi, ref_phi, drive, phase_error):
    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)

    axes[0].plot(phi, label="phi", color="blue")
    axes[0].plot(ref_phi, label="ref phi", color="orange")
    axes[0].plot(drive, label="drive", color="black", alpha=0.7)
    axes[0].set_title("V17 Phase / Reference / Drive")
    axes[0].grid(True)
    axes[0].legend()

    axes[1].plot(phase_error, color="red", label="phase error")
    axes[1].axhline(0.0, linestyle="--", color="gray")
    axes[1].set_title("V17 Phase Error")
    axes[1].grid(True)
    axes[1].legend()

    path = os.path.join(RIFT_DIR, "v17_phase.png")
    plt.savefig(path, dpi=150)
    print(f"Saved → {path}")
    plt.close()


def plot_instability(instability, target_layers, base_layer, upper_layer, lower_layer):
    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)

    axes[0].plot(instability, color="darkred", label="instability")
    axes[0].set_title("V17 Local Instability")
    axes[0].grid(True)
    axes[0].legend()

    axes[1].plot(target_layers, color="green", label="target layer")
    axes[1].axhline(base_layer, linestyle="--", color="magenta", label="base")
    axes[1].axhline(upper_layer, linestyle="--", color="orange", label="upper")
    axes[1].axhline(lower_layer, linestyle="--", color="purple", label="lower")
    axes[1].set_title("V17 Layer Targeting")
    axes[1].grid(True)
    axes[1].legend()

    path = os.path.join(RIFT_DIR, "v17_instability_layers.png")
    plt.savefig(path, dpi=150)
    print(f"Saved → {path}")
    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    trajectory, rift = load_data()

    result = field_navigation_controller_v17(trajectory, rift)

    np.save(os.path.join(RIFT_DIR, "field_navigation_v17.npy"), result["controlled"])
    print("Saved controlled trajectory → field_navigation_v17.npy")

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
    )

    plot_instability(
        result["instability"],
        result["target_layers"],
        result["base_layer"],
        result["upper_layer"],
        result["lower_layer"],
    )

    print("V17 Field Navigation DONE")


if __name__ == "__main__":
    main()
