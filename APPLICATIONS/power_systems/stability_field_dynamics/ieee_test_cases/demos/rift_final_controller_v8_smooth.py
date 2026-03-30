# rift_final_controller_v8_smooth.py

import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")


# -----------------------------
# LOAD
# -----------------------------

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

    rift = np.load(os.path.join(RIFT_DIR, "rift_curve.npy"))
    print("✅ Loaded rift")

    return trajectory[:, :2], rift


# -----------------------------
# CORE
# -----------------------------

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
    return center, spread


# -----------------------------
# V8.1 SMOOTH CONTROLLER
# -----------------------------

def final_controller_v8_smooth(trajectory, rift):

    controlled = trajectory.copy()

    pc1 = trajectory[:, 0]
    pc2 = trajectory[:, 1]

    events = sorted(set(
        list(detect_events(pc1)) +
        list(detect_events(pc2))
    ))

    f1 = dominant_freq(pc1)
    f2 = dominant_freq(pc2)

    layer_center, layer_spread = estimate_layer(trajectory)

    print(f"⚡ Events: {events}")
    print(f"🔊 Frequencies: {f1:.4f}, {f2:.4f}")

    for t in range(len(controlled)):

        current = controlled[t]

        # -------------------
        # RIFT
        # -------------------
        rift_target = nearest_rift_point(current, rift)
        rift_corr = 0.18 * (rift_target - current)

        # -------------------
        # FREQUENCY
        # -------------------
        phase = 0.5 * (
            np.sin(2 * np.pi * f1 * t) +
            np.sin(2 * np.pi * f2 * t)
        )
        freq_corr = 0.12 * phase * (rift_target - current)

        # -------------------
        # EVENT (reduced)
        # -------------------
        event_corr = np.zeros_like(current)
        if t in events:
            event_corr = 0.4 * (rift_target - current)

        # -------------------
        # ADAPTIVE LAYER
        # -------------------
        deviation = abs(current[1] - layer_center)
        layer_gain = 0.2 + 0.6 * (deviation / (layer_spread + 1e-6))

        layer_target = np.array([current[0], layer_center])
        layer_corr = layer_gain * (layer_target - current)

        # -------------------
        # COMBINE
        # -------------------
        correction = rift_corr + freq_corr + event_corr + layer_corr

        # 🔥 SMOOTH CLAMP (kein hartes clipping)
        correction = np.tanh(correction) * 0.07

        # 🔥 MOMENTUM (wichtig!)
        if t > 0:
            momentum = controlled[t] - controlled[t - 1]
            correction = 0.7 * correction + 0.3 * momentum

        controlled[t] += correction

    return controlled, layer_center


# -----------------------------
# PLOT
# -----------------------------

def plot_result(original, controlled, rift, layer_center):

    plt.figure(figsize=(10, 6))

    plt.plot(original[:, 0], original[:, 1], label="original", color="green")
    plt.plot(rift[:, 0], rift[:, 1], label="rift", color="cyan")
    plt.plot(controlled[:, 0], controlled[:, 1], label="V8.1 smooth", color="gold")

    plt.axhline(layer_center, linestyle="--", color="magenta", label="layer")

    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "final_controller_v8_smooth.png")
    plt.savefig(save_path)
    print(f"💾 Saved → {save_path}")

    plt.close()


# -----------------------------
# MAIN
# -----------------------------

def main():

    trajectory, rift = load_data()

    controlled, layer_center = final_controller_v8_smooth(trajectory, rift)

    np.save(os.path.join(RIFT_DIR, "final_controller_v8_smooth.npy"), controlled)
    print("💾 Saved controlled trajectory → final_controller_v8_smooth.npy")

    plot_result(trajectory, controlled, rift, layer_center)

    print("🚀 FINAL CONTROLLER V8.1 SMOOTH complete")


if __name__ == "__main__":
    main()
