# rift_phase_unwrap_v16.py

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

    return traj[:, :2]


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def dominant_freq(signal):
    fft_vals = np.fft.rfft(signal)
    power = np.abs(fft_vals)
    freqs = np.fft.rfftfreq(len(signal))
    idx = np.argmax(power[1:]) + 1
    return freqs[idx]


def wrap(x):
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
# MODEL
# --------------------------------------------------

def run_model(traj):
    x = traj[:, 0].copy()
    f0 = dominant_freq(x)

    n = len(x)

    phi_unwrapped = np.zeros(n)
    phi_wrapped = np.zeros(n)
    dphi = np.zeros(n)
    drive = np.zeros(n)
    regime = np.zeros(n, dtype=int)
    branch = np.zeros(n, dtype=int)

    ref_phi = np.zeros(n)

    phi_unwrapped[0] = 0.0
    phi_wrapped[0] = 0.0

    cut_indices = []

    for t in range(1, n):
        ref_phi[t] = 2 * np.pi * f0 * t

        v = traj[t] - traj[t - 1]
        speed = np.linalg.norm(v)

        if t > 1:
            v_prev = traj[t - 1] - traj[t - 2]
            turn = np.linalg.norm(v - v_prev)
        else:
            turn = 0.0

        pe = wrap(phi_wrapped[t - 1] - wrap_0_2pi(ref_phi[t - 1]))

        dphi[t] = (
            2 * np.pi * f0
            + 0.02 * speed
            + 0.015 * turn
            - 0.4 * pe
        )

        phi_unwrapped[t] = phi_unwrapped[t - 1] + dphi[t]
        phi_wrapped[t] = wrap_0_2pi(phi_unwrapped[t])

        drive[t] = (
            np.sin(phi_wrapped[t])
            + 0.5 * np.sin(2 * phi_wrapped[t])
            + 0.3 * np.sin(3 * phi_wrapped[t])
        )
        regime[t] = regime_from_drive(drive[t])

        branch[t] = int(np.floor(phi_unwrapped[t] / (2 * np.pi)))

        if branch[t] != branch[t - 1]:
            cut_indices.append(t)

    return phi_unwrapped, phi_wrapped, dphi, drive, regime, branch, cut_indices


# --------------------------------------------------
# PLOTS
# --------------------------------------------------

def plot_unwrapped_phase(phi_unwrapped, dphi, regime, cut_indices):
    plt.figure(figsize=(11, 6))

    plt.plot(phi_unwrapped, label="phi_unwrapped", color="blue")
    plt.plot(dphi, label="dphi/dt", color="red")

    for i in range(len(regime)):
        if regime[i] == 1:
            plt.axvline(i, color="green", alpha=0.03)
        elif regime[i] == -1:
            plt.axvline(i, color="purple", alpha=0.03)

    for idx in cut_indices:
        plt.axvline(idx, color="black", linestyle="--", alpha=0.5)

    plt.title("V16 Unwrapped Phase Evolution")
    plt.grid(True)
    plt.legend()

    path = os.path.join(RIFT_DIR, "v16_unwrapped_phase.png")
    plt.savefig(path, dpi=150)
    print(f"Saved -> {path}")
    plt.close()


def plot_wrapped_vs_unwrapped(phi_wrapped, phi_unwrapped, cut_indices):
    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

    axes[0].plot(phi_wrapped, color="orange", label="phi_wrapped")
    for idx in cut_indices:
        axes[0].axvline(idx, color="black", linestyle="--", alpha=0.5)
    axes[0].set_title("Wrapped Phase")
    axes[0].grid(True)
    axes[0].legend()

    axes[1].plot(phi_unwrapped, color="blue", label="phi_unwrapped")
    for idx in cut_indices:
        axes[1].axvline(idx, color="black", linestyle="--", alpha=0.5)
    axes[1].set_title("Unwrapped Phase")
    axes[1].grid(True)
    axes[1].legend()

    path = os.path.join(RIFT_DIR, "v16_wrapped_vs_unwrapped.png")
    plt.savefig(path, dpi=150)
    print(f"Saved -> {path}")
    plt.close()


def plot_cut_state_space(phi_wrapped, dphi, regime, cut_indices):
    plt.figure(figsize=(9, 6))

    for r, c in [(-1, "purple"), (0, "gold"), (1, "green")]:
        mask = regime == r
        plt.scatter(phi_wrapped[mask], dphi[mask], s=18, color=c, label=f"regime {r}")

    plt.axhline(0, linestyle="--", color="gray")
    plt.axvline(0, linestyle="--", color="gray")
    plt.axvline(2 * np.pi, linestyle="--", color="gray", alpha=0.4)

    plt.title("V16 Wrapped State Space with Cut Dynamics")
    plt.xlabel("phi_wrapped")
    plt.ylabel("dphi/dt")
    plt.grid(True)
    plt.legend()

    path = os.path.join(RIFT_DIR, "v16_cut_state_space.png")
    plt.savefig(path, dpi=150)
    print(f"Saved -> {path}")
    plt.close()


def save_cut_summary(branch, cut_indices):
    path = os.path.join(RIFT_DIR, "v16_cut_summary.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("# V16 Cut Dynamics Summary\n\n")
        f.write(f"- Total cuts: {len(cut_indices)}\n")
        f.write(f"- Cut indices: {cut_indices}\n")
        f.write(f"- Final branch index: {int(branch[-1])}\n")
    print(f"Saved -> {path}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    traj = load_data()

    phi_unwrapped, phi_wrapped, dphi, drive, regime, branch, cut_indices = run_model(traj)

    plot_unwrapped_phase(phi_unwrapped, dphi, regime, cut_indices)
    plot_wrapped_vs_unwrapped(phi_wrapped, phi_unwrapped, cut_indices)
    plot_cut_state_space(phi_wrapped, dphi, regime, cut_indices)
    save_cut_summary(branch, cut_indices)

    print("V16 unwrap + cut dynamics DONE")


if __name__ == "__main__":
    main()
