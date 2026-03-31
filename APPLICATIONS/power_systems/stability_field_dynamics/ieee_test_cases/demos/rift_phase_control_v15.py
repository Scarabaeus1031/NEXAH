# rift_phase_control_v15.py

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


def regime_from_drive(d):
    if d > 0.3:
        return 1
    elif d < -0.3:
        return -1
    else:
        return 0


# --------------------------------------------------
# CONTROL MODEL
# --------------------------------------------------

def run_control_model(traj):

    x = traj[:, 0].copy()
    y = traj[:, 1].copy()

    f0 = dominant_freq(x)

    N = len(x)

    phi = np.zeros(N)
    dphi = np.zeros(N)
    drive = np.zeros(N)
    regime = np.zeros(N)

    ref_phi = np.zeros(N)

    phi[0] = 0.0

    # 🎯 TARGET REGIME (key control knob!)
    TARGET_REGIME = 1   # try: -1, 0, 1

    for t in range(1, N):

        ref_phi[t] = (2 * np.pi * f0 * t) % (2 * np.pi)

        # -----------------------------
        # BASE DYNAMICS
        # -----------------------------

        v = traj[t] - traj[t - 1]
        speed = np.linalg.norm(v)

        if t > 1:
            v_prev = traj[t - 1] - traj[t - 2]
            turn = np.linalg.norm(v - v_prev)
        else:
            turn = 0.0

        pe = wrap(phi[t - 1] - ref_phi[t - 1])

        # -----------------------------
        # 🔥 CONTROL: PHASE STEERING
        # -----------------------------

        # bias phase depending on target regime
        phase_bias = 0.0

        if TARGET_REGIME == 1:
            phase_bias = +0.25
        elif TARGET_REGIME == -1:
            phase_bias = -0.25
        else:
            phase_bias = 0.0

        # -----------------------------
        # PHASE UPDATE
        # -----------------------------

        dphi[t] = (
            2 * np.pi * f0
            + 0.02 * speed
            + 0.015 * turn
            - 0.4 * pe
            + phase_bias   # 🔥 CONTROL INJECTION
        )

        phi[t] = (phi[t - 1] + dphi[t]) % (2 * np.pi)

        # -----------------------------
        # DRIVE (multi-frequency)
        # -----------------------------

        drive[t] = (
            np.sin(phi[t])
            + 0.5 * np.sin(2 * phi[t])
            + 0.3 * np.sin(3 * phi[t])
        )

        # -----------------------------
        # 🔥 CONTROL: REGIME LOCK
        # -----------------------------

        r = regime_from_drive(drive[t])

        # force toward target regime
        if TARGET_REGIME == 1 and r < 1:
            drive[t] += 0.2
        elif TARGET_REGIME == -1 and r > -1:
            drive[t] -= 0.2

        regime[t] = regime_from_drive(drive[t])

    return phi, dphi, drive, regime


# --------------------------------------------------
# PLOTS
# --------------------------------------------------

def plot_control(phi, dphi, drive, regime):

    plt.figure(figsize=(10, 6))

    plt.plot(phi, label="φ", color="blue")
    plt.plot(drive, label="drive", color="orange")

    for i in range(len(regime)):
        if regime[i] == 1:
            plt.axvline(i, color="green", alpha=0.05)
        elif regime[i] == -1:
            plt.axvline(i, color="purple", alpha=0.05)

    plt.legend()
    plt.grid(True)
    plt.title("V15 Control (Phase + Drive)")

    path = os.path.join(RIFT_DIR, "v15_control_phase.png")
    plt.savefig(path, dpi=150)
    print(f"Saved → {path}")
    plt.close()


def plot_state_space(phi, dphi, regime):

    plt.figure(figsize=(8, 6))

    for r, c in [(-1, "purple"), (0, "gold"), (1, "green")]:
        mask = regime == r
        plt.scatter(phi[mask], dphi[mask], s=20, label=f"regime {r}", color=c)

    plt.axhline(0, linestyle="--")
    plt.axvline(0, linestyle="--")

    plt.xlabel("φ")
    plt.ylabel("dφ/dt")
    plt.title("V15 Controlled State Space")

    plt.legend()
    plt.grid(True)

    path = os.path.join(RIFT_DIR, "v15_state_space.png")
    plt.savefig(path, dpi=150)
    print(f"Saved → {path}")
    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    traj = load_data()

    phi, dphi, drive, regime = run_control_model(traj)

    plot_control(phi, dphi, drive, regime)
    plot_state_space(phi, dphi, regime)

    print("🚀 V15 CONTROL DONE")


if __name__ == "__main__":
    main()
