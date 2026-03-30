# rift_phase_field_metrics.py

import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")


# --------------------------------------------------
# LOAD
# --------------------------------------------------

def load_data():

    trajectory = np.load(os.path.join(BASE_DIR, "states.npy"))
    controlled = np.load(os.path.join(RIFT_DIR, "phase_controller.npy"))

    print("✅ Loaded: states.npy")
    print("✅ Loaded: phase_controller.npy")

    return trajectory[:, :2], controlled[:, :2]


# --------------------------------------------------
# PHASE
# --------------------------------------------------

def dominant_freq(signal):
    fft_vals = np.fft.rfft(signal)
    power = np.abs(fft_vals)
    freqs = np.fft.rfftfreq(len(signal))
    idx = np.argmax(power[1:]) + 1
    return freqs[idx]


def compute_phase(n, freq):
    t = np.arange(n)
    return (2 * np.pi * freq * t) % (2 * np.pi)


# --------------------------------------------------
# METRICS
# --------------------------------------------------

def compute_phase_metrics(traj):

    pc1 = traj[:, 0]
    pc2 = traj[:, 1]

    f = dominant_freq(pc1)
    phase = compute_phase(len(traj), f)

    # velocity
    velocity = np.diff(traj, axis=0)
    speed = np.linalg.norm(velocity, axis=1)

    # expansion / contraction (signed)
    expansion = np.diff(speed)

    # phase alignment (are we moving WITH phase?)
    phase_dir = np.sin(phase[:-1])
    alignment = np.sign(expansion) * np.sign(phase_dir)

    # coherence
    phase_coherence = np.mean(alignment)

    # smoothness
    smoothness = np.std(expansion)

    return {
        "phase_coherence": phase_coherence,
        "expansion_std": np.std(expansion),
        "speed_mean": np.mean(speed),
        "speed_std": np.std(speed)
    }, phase, expansion


# --------------------------------------------------
# PLOT
# --------------------------------------------------

def plot_phase_metrics(phase, expansion):

    plt.figure(figsize=(10, 4))
    plt.plot(phase[:-1], label="phase")
    plt.plot(expansion, label="expansion", alpha=0.7)

    plt.legend()
    plt.grid(True)
    plt.title("Phase vs Expansion")

    save_path = os.path.join(RIFT_DIR, "phase_field_metrics.png")
    plt.savefig(save_path)
    print(f"💾 Saved → {save_path}")

    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    original, controlled = load_data()

    print("\n📊 ORIGINAL")
    m_orig, phase_orig, exp_orig = compute_phase_metrics(original)

    for k, v in m_orig.items():
        print(f"{k}: {v:.6f}")

    print("\n📊 CONTROLLED (PHASE)")
    m_ctrl, phase_ctrl, exp_ctrl = compute_phase_metrics(controlled)

    for k, v in m_ctrl.items():
        print(f"{k}: {v:.6f}")

    plot_phase_metrics(phase_ctrl, exp_ctrl)

    print("\n🚀 Phase field metrics complete")


if __name__ == "__main__":
    main()    plt.figure(figsize=(10, 4))
    plt.plot(phase[:-1], label="phase")
    plt.plot(expansion, label="expansion", alpha=0.7)

    plt.legend()
    plt.grid(True)
    plt.title("Phase vs Expansion")

    save_path = os.path.join(RIFT_DIR, "phase_field_metrics.png")
    plt.savefig(save_path)
    print(f"💾 Saved → {save_path}")

    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    original, controlled = load_data()

    print("\n📊 ORIGINAL")
    m_orig, phase_orig, exp_orig = compute_phase_metrics(original)

    for k, v in m_orig.items():
        print(f"{k}: {v:.6f}")

    print("\n📊 CONTROLLED (PHASE)")
    m_ctrl, phase_ctrl, exp_ctrl = compute_phase_metrics(controlled)

    for k, v in m_ctrl.items():
        print(f"{k}: {v:.6f}")

    plot_phase_metrics(phase_ctrl, exp_ctrl)

    print("\n🚀 Phase field metrics complete")


if __name__ == "__main__":
    main()
