# rift_phase_state_space_v16_3.py

import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")


# --------------------------------------------------
# LOAD
# --------------------------------------------------

def load_data():
    traj = None

    for name in ["trajectory.npy", "states.npy"]:
        path = os.path.join(BASE_DIR, name)
        if os.path.exists(path):
            traj = np.load(path)
            print(f"Loaded trajectory: {name}")
            break

    if traj is None:
        raise FileNotFoundError("No trajectory found")

    rift_path = os.path.join(RIFT_DIR, "rift_curve.npy")
    if os.path.exists(rift_path):
        rift = np.load(rift_path)
        print("Loaded rift")
    else:
        rift = None
        print("No rift found (continuing anyway)")

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


def wrap_pm_pi(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def wrap_0_2pi(x):
    return np.mod(x, 2 * np.pi)


def regime_from_drive(d):
    if d > 0.3:
        return 1
    elif d < -0.3:
        return -1
    else:
        return 0


# --------------------------------------------------
# V16.3 MULTI-BRANCH MODEL
# --------------------------------------------------

def run_state_model_v16_3(traj):
    x = traj[:, 0].copy()
    y = traj[:, 1].copy()

    f0 = dominant_freq(x)
    n = len(x)

    phi_unwrapped = np.zeros(n)
    phi_wrapped = np.zeros(n)
    dphi = np.zeros(n)
    drive = np.zeros(n)
    regime = np.zeros(n, dtype=int)
    branch = np.zeros(n, dtype=int)
    ref_phi = np.zeros(n)

    # extra diagnostics
    phase_error = np.zeros(n)
    speed_arr = np.zeros(n)
    turn_arr = np.zeros(n)

    phi_unwrapped[0] = 0.0
    phi_wrapped[0] = 0.0

    # --------------------------------------------------
    # FORCE MULTI-BRANCHING
    # --------------------------------------------------
    # stronger base gain + explicit drift + pulse windows
    drift_bias = 0.020

    # windows where the system gets extra phase-energy
    pulse_windows = [
        (18, 28, 0.030),
        (42, 58, 0.040),
        (72, 86, 0.050),
        (96, 112, 0.035),
    ]

    for t in range(1, n):
        ref_phi[t] = 2 * np.pi * f0 * t

        v = traj[t] - traj[t - 1]
        speed = np.linalg.norm(v)
        speed_arr[t] = speed

        if t > 1:
            v_prev = traj[t - 1] - traj[t - 2]
            turn = np.linalg.norm(v - v_prev)
        else:
            turn = 0.0
        turn_arr[t] = turn

        pe = wrap_pm_pi(phi_wrapped[t - 1] - wrap_0_2pi(ref_phi[t - 1]))
        phase_error[t] = pe

        # pulse activation
        pulse = 0.0
        for t0, t1, amp in pulse_windows:
            if t0 <= t <= t1:
                pulse += amp

        # stronger dynamics than V16.2
        dphi[t] = (
            2 * np.pi * f0
            + 0.10 * speed
            + 0.08 * turn
            - 0.12 * pe
            + drift_bias
            + pulse
        )

        phi_unwrapped[t] = phi_unwrapped[t - 1] + dphi[t]
        phi_wrapped[t] = wrap_0_2pi(phi_unwrapped[t])

        branch[t] = int(np.floor(phi_unwrapped[t] / (2 * np.pi)))

        drive[t] = (
            np.sin(phi_wrapped[t])
            + 0.5 * np.sin(2 * phi_wrapped[t])
            + 0.3 * np.sin(3 * phi_wrapped[t])
        )

        regime[t] = regime_from_drive(drive[t])

    return {
        "phi_unwrapped": phi_unwrapped,
        "phi_wrapped": phi_wrapped,
        "dphi": dphi,
        "drive": drive,
        "regime": regime,
        "branch": branch,
        "ref_phi": ref_phi,
        "phase_error": phase_error,
        "speed": speed_arr,
        "turn": turn_arr,
        "f0": f0,
    }


# --------------------------------------------------
# CUT DETECTION
# --------------------------------------------------

def detect_cuts(phi_unwrapped):
    cuts = []
    prev_branch = int(np.floor(phi_unwrapped[0] / (2 * np.pi)))

    for t in range(1, len(phi_unwrapped)):
        curr_branch = int(np.floor(phi_unwrapped[t] / (2 * np.pi)))
        if curr_branch != prev_branch:
            cuts.append(t)
        prev_branch = curr_branch

    return cuts


# --------------------------------------------------
# PLOTS
# --------------------------------------------------

def plot_state_space(phi_wrapped, dphi, regime, cuts):
    plt.figure(figsize=(9, 6))

    for r, c in [(-1, "purple"), (0, "gold"), (1, "green")]:
        mask = regime == r
        plt.scatter(phi_wrapped[mask], dphi[mask], s=22, color=c, label=f"regime {r}")

    # cut positions projected into wrapped chart
    for idx in cuts:
        plt.axvline(phi_wrapped[idx], color="red", linestyle="--", alpha=0.45)

    plt.axhline(0, linestyle="--", color="gray", alpha=0.7)
    plt.axvline(0, linestyle="--", color="gray", alpha=0.7)
    plt.axvline(2 * np.pi, linestyle="--", color="gray", alpha=0.35)

    plt.xlabel("φ (wrapped)")
    plt.ylabel("dφ/dt")
    plt.title("V16.3 Forced Multi-Branch State Space")
    plt.legend()
    plt.grid(True)

    path = os.path.join(RIFT_DIR, "v16_3_state_space.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved → {path}")
    plt.close()


def plot_branch_evolution(phi_unwrapped, branch, cuts):
    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.plot(phi_unwrapped, color="blue", label="φ_unwrapped")
    ax1.set_ylabel("φ_unwrapped", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.plot(branch, color="black", linewidth=2, label="branch index")
    ax2.set_ylabel("branch", color="black")
    ax2.tick_params(axis="y", labelcolor="black")

    for idx in cuts:
        ax1.axvline(idx, color="red", linestyle="--", alpha=0.45)

    ax1.set_title("V16.3 Branch Evolution")

    path = os.path.join(RIFT_DIR, "v16_3_branch_evolution.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved → {path}")
    plt.close()


def plot_wrapped_vs_unwrapped(phi_wrapped, phi_unwrapped, cuts):
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    axes[0].plot(phi_wrapped, color="orange", label="φ_wrapped")
    axes[0].set_title("Wrapped Phase")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(phi_unwrapped, color="blue", label="φ_unwrapped")
    axes[1].set_title("Unwrapped Phase")
    axes[1].legend()
    axes[1].grid(True)

    for idx in cuts:
        axes[0].axvline(idx, color="red", linestyle="--", alpha=0.35)
        axes[1].axvline(idx, color="red", linestyle="--", alpha=0.35)

    path = os.path.join(RIFT_DIR, "v16_3_wrapped_vs_unwrapped.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved → {path}")
    plt.close()


def plot_drive_and_regime(drive, regime, cuts):
    plt.figure(figsize=(10, 5))
    plt.plot(drive, color="darkorange", label="drive")
    plt.axhline(0.3, linestyle="--", color="gray", alpha=0.6)
    plt.axhline(-0.3, linestyle="--", color="gray", alpha=0.6)
    plt.axhline(0.0, linestyle="--", color="black", alpha=0.4)

    for i in range(len(regime)):
        if regime[i] == 1:
            plt.axvline(i, color="green", alpha=0.025)
        elif regime[i] == -1:
            plt.axvline(i, color="purple", alpha=0.025)

    for idx in cuts:
        plt.axvline(idx, color="red", linestyle="--", alpha=0.45)

    plt.legend()
    plt.grid(True)
    plt.title("V16.3 Drive + Regime + Cuts")

    path = os.path.join(RIFT_DIR, "v16_3_drive_regime.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Saved → {path}")
    plt.close()


def save_summary(results, cuts):
    branch = results["branch"]
    path = os.path.join(RIFT_DIR, "v16_3_cut_summary.md")

    with open(path, "w", encoding="utf-8") as f:
        f.write("# V16.3 Cut Dynamics Summary\n\n")
        f.write(f"- Total cuts: {len(cuts)}\n")
        f.write(f"- Cut indices: {cuts}\n")
        f.write(f"- Final branch index: {int(branch[-1])}\n")
        if cuts:
            f.write(f"- First cut at t = {cuts[0]}\n")
            f.write(f"- Last cut at t = {cuts[-1]}\n")

    print(f"Saved → {path}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    traj, _ = load_data()

    results = run_state_model_v16_3(traj)

    cuts = detect_cuts(results["phi_unwrapped"])

    print(f"Base frequency f0: {results['f0']:.6f}")
    print(f"Total cuts: {len(cuts)}")
    print(f"Cut indices: {cuts}")
    print(f"Final branch index: {int(results['branch'][-1])}")

    plot_state_space(
        results["phi_wrapped"],
        results["dphi"],
        results["regime"],
        cuts
    )
    plot_branch_evolution(
        results["phi_unwrapped"],
        results["branch"],
        cuts
    )
    plot_wrapped_vs_unwrapped(
        results["phi_wrapped"],
        results["phi_unwrapped"],
        cuts
    )
    plot_drive_and_regime(
        results["drive"],
        results["regime"],
        cuts
    )
    save_summary(results, cuts)

    print("V16.3 Forced Multi-Branch DONE")


if __name__ == "__main__":
    main()
