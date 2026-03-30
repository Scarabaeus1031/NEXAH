# rift_final_controller_v7.py

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
# CORE COMPONENTS
# --------------------------------------------------

def compute_instability(signal):
    return np.abs(np.diff(signal))


def detect_events(signal, factor=2.0):
    inst = compute_instability(signal)
    threshold = np.mean(inst) + factor * np.std(inst)
    return np.where(inst > threshold)[0]


def dominant_freq(signal):
    fft_vals = np.fft.rfft(signal)
    power = np.abs(fft_vals)
    freqs = np.fft.rfftfreq(len(signal))
    idx = np.argmax(power[1:]) + 1
    return freqs[idx]


def nearest_rift_point(p, rift):
    dists = np.linalg.norm(rift - p, axis=1)
    return rift[np.argmin(dists)]


def estimate_layer(traj):
    pc2 = traj[:, 1]
    center = np.median(pc2)
    spread = np.std(pc2)
    print(f"🎯 Layer: {center:.4f} ± {spread:.4f}")
    return center


# --------------------------------------------------
# FINAL CONTROLLER
# --------------------------------------------------

def final_controller(trajectory, rift):

    controlled = trajectory.copy()

    pc1 = trajectory[:, 0]
    pc2 = trajectory[:, 1]

    # components
    events = sorted(set(
        list(detect_events(pc1)) +
        list(detect_events(pc2))
    ))

    f1 = dominant_freq(pc1)
    f2 = dominant_freq(pc2)

    layer_center = estimate_layer(trajectory)

    print(f"⚡ Events: {events}")
    print(f"🔊 Frequencies: {f1:.4f}, {f2:.4f}")

    # gains
    gain_rift = 0.18
    gain_freq = 0.12
    gain_event = 0.35
    gain_layer = 0.22

    for t in range(len(controlled)):

        current = controlled[t]

        # --- RIFT ---
        rift_target = nearest_rift_point(current, rift)
        rift_corr = gain_rift * (rift_target - current)

        # --- FREQUENCY ---
        phase = 0.5 * (
            np.sin(2 * np.pi * f1 * t) +
            np.sin(2 * np.pi * f2 * t)
        )
        freq_corr = gain_freq * phase * (rift_target - current)

        # --- EVENT ---
        event_corr = np.zeros_like(current)
        if t in events:
            event_corr = gain_event * (rift_target - current)

        # --- LAYER ---
        layer_target = np.array([current[0], layer_center])
        layer_corr = gain_layer * (layer_target - current)

        # --- COMBINE ---
        correction = rift_corr + freq_corr + event_corr + layer_corr

        # clamp = stabilität
        correction = np.clip(correction, -0.05, 0.05)

        controlled[t] += correction

    return controlled, layer_center


# --------------------------------------------------
# PLOT
# --------------------------------------------------

def plot_result(original, controlled, rift, layer_center):
    plt.figure(figsize=(10, 6))

    plt.plot(original[:, 0], original[:, 1], label="original", color="green")
    plt.plot(rift[:, 0], rift[:, 1], label="rift", color="cyan")
    plt.plot(controlled[:, 0], controlled[:, 1], label="final v7", color="gold")

    plt.axhline(layer_center, linestyle="--", color="magenta", label="layer")

    plt.scatter(original[-1, 0], original[-1, 1], color="red", label="orig end")
    plt.scatter(controlled[-1, 0], controlled[-1, 1], color="orange", label="controlled end")

    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "final_controller_v7.png")
    plt.savefig(save_path, dpi=150)
    print(f"💾 Saved → {save_path}")

    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    trajectory, rift = load_data()

    controlled, layer_center = final_controller(trajectory, rift)

    # 🔥 HIER EINFÜGEN
    np.save(
        os.path.join(RIFT_DIR, "final_controller_v7.npy"),
        controlled
    )
    print("💾 Saved controlled trajectory → final_controller_v7.npy")

    plot_result(trajectory, controlled, rift, layer_center)

    print("🚀 FINAL CONTROLLER V7 complete")

if __name__ == "__main__":
    main()
