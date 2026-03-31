# rift_phase_state_space_v16_2.py

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

def wrap(x):
    return (x + np.pi) % (2*np.pi) - np.pi

def regime_from_drive(d):
    if d > 0.3:
        return 1
    elif d < -0.3:
        return -1
    else:
        return 0


# --------------------------------------------------
# STATE EVOLUTION (MULTI-BRANCH)
# --------------------------------------------------

def run_state_model(traj):

    x = traj[:, 0].copy()
    y = traj[:, 1].copy()

    f0 = dominant_freq(x)
    N = len(x)

    phi_wrapped = np.zeros(N)
    phi_unwrapped = np.zeros(N)
    dphi = np.zeros(N)
    drive = np.zeros(N)
    regime = np.zeros(N)
    branch = np.zeros(N, dtype=int)

    ref_phi = np.zeros(N)

    phi_unwrapped[0] = 0.0

    for t in range(1, N):

        ref_phi[t] = (2*np.pi*f0*t)

        # velocity
        v = traj[t] - traj[t-1]
        speed = np.linalg.norm(v)

        # curvature
        if t > 1:
            v_prev = traj[t-1] - traj[t-2]
            turn = np.linalg.norm(v - v_prev)
        else:
            turn = 0.0

        # phase error
        pe = wrap(phi_unwrapped[t-1] - ref_phi[t-1])

        # 🔥 stronger dynamics to force cuts
        dphi[t] = (
            2*np.pi*f0
            + 0.06 * speed
            + 0.05 * turn
            - 0.2 * pe
        )

        # unwrapped phase grows continuously
        phi_unwrapped[t] = phi_unwrapped[t-1] + dphi[t]

        # wrapped phase
        phi_wrapped[t] = phi_unwrapped[t] % (2*np.pi)

        # branch index
        branch[t] = int(np.floor(phi_unwrapped[t] / (2*np.pi)))

        # drive
        drive[t] = (
            np.sin(phi_wrapped[t])
            + 0.5*np.sin(2*phi_wrapped[t])
            + 0.3*np.sin(3*phi_wrapped[t])
        )

        regime[t] = regime_from_drive(drive[t])

    return phi_wrapped, phi_unwrapped, dphi, drive, regime, branch


# --------------------------------------------------
# CUT DETECTION
# --------------------------------------------------

def detect_cuts(phi_unwrapped):
    cuts = []
    prev = int(np.floor(phi_unwrapped[0] / (2*np.pi)))

    for t in range(1, len(phi_unwrapped)):
        curr = int(np.floor(phi_unwrapped[t] / (2*np.pi)))
        if curr != prev:
            cuts.append(t)
        prev = curr

    return cuts


# --------------------------------------------------
# PLOTS
# --------------------------------------------------

def plot_state_space(phi_wrapped, dphi, regime, cuts):

    plt.figure(figsize=(8, 6))

    for r, c in [(-1, "purple"), (0, "gold"), (1, "green")]:
        mask = regime == r
        plt.scatter(phi_wrapped[mask], dphi[mask], s=20, color=c, label=f"regime {r}")

    for c in cuts:
        plt.axvline(phi_wrapped[c], color="red", linestyle="--", alpha=0.5)

    plt.xlabel("φ (wrapped)")
    plt.ylabel("dφ/dt")
    plt.title("V16.2 Multi-Branch State Space")

    plt.legend()
    plt.grid(True)

    path = os.path.join(RIFT_DIR, "v16_2_state_space.png")
    plt.savefig(path, dpi=150)
    print(f"Saved → {path}")
    plt.close()


def plot_branch(phi_unwrapped, branch):

    plt.figure(figsize=(10, 5))

    plt.plot(phi_unwrapped, label="φ_unwrapped", color="blue")
    plt.plot(branch, label="branch index", color="black")

    plt.legend()
    plt.grid(True)
    plt.title("Branch Evolution")

    path = os.path.join(RIFT_DIR, "v16_2_branch_evolution.png")
    plt.savefig(path, dpi=150)
    print(f"Saved → {path}")
    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    traj, _ = load_data()

    phi_w, phi_u, dphi, drive, regime, branch = run_state_model(traj)

    cuts = detect_cuts(phi_u)

    print(f"Total cuts: {len(cuts)}")
    print(f"Cut indices: {cuts[:10]}")

    plot_state_space(phi_w, dphi, regime, cuts)
    plot_branch(phi_u, branch)

    print("V16.2 Multi-Branch DONE")


if __name__ == "__main__":
    main()
