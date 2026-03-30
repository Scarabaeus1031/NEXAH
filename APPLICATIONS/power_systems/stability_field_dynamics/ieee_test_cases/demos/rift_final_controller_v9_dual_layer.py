# rift_final_controller_v9_dual_layer.py

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
# CORE
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
    print(f"🎯 Base Layer: {center:.4f} ± {spread:.4f}")
    return center, spread


# --------------------------------------------------
# V9 DUAL LAYER CONTROLLER
# --------------------------------------------------

def dual_layer_controller(trajectory, rift):

    controlled = trajectory.copy()

    pc1 = trajectory[:, 0]
    pc2 = trajectory[:, 1]

    # events + frequency
    events = sorted(set(
        list(detect_events(pc1)) +
        list(detect_events(pc2))
    ))

    f1 = dominant_freq(pc1)
    f2 = dominant_freq(pc2)

    base_layer, spread = estimate_layer(trajectory)

    # 👉 NEW: second layer (upper boundary)
    upper_layer = base_layer + spread * 0.95  # ≈ ~0.78 in deinem Fall

    print(f"🎯 Upper Layer: {upper_layer:.4f}")
    print(f"⚡ Events: {events}")
    print(f"🔊 Frequencies: {f1:.4f}, {f2:.4f}")

    # gains
    gain_rift = 0.18
    gain_freq = 0.12
    gain_event = 0.35
    gain_layer = 0.25

    momentum = np.zeros_like(controlled)

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

        # --- DUAL LAYER LOGIC 🔥 ---
        inst = 0
        if t > 0:
            inst = np.linalg.norm(controlled[t] - controlled[t-1])

        # 👉 switch logic
        if inst > 0.02:
            target_layer = upper_layer   # active mode
        else:
            target_layer = base_layer    # stable mode

        layer_target = np.array([current[0], target_layer])
        layer_corr = gain_layer * (layer_target - current)

        # --- COMBINE ---
        correction = rift_corr + freq_corr + event_corr + layer_corr

        # smooth momentum
        momentum[t] = 0.75 * momentum[t-1] + 0.25 * correction if t > 0 else correction
        correction = np.tanh(momentum[t]) * 0.05

        controlled[t] += correction

    return controlled, base_layer, upper_layer


# --------------------------------------------------
# PLOT
# --------------------------------------------------

def plot_result(original, controlled, rift, base_layer, upper_layer):
    plt.figure(figsize=(10, 6))

    plt.plot(original[:, 0], original[:, 1], label="original", color="green")
    plt.plot(rift[:, 0], rift[:, 1], label="rift", color="cyan")
    plt.plot(controlled[:, 0], controlled[:, 1], label="V9 dual-layer", color="gold")

    plt.axhline(base_layer, linestyle="--", color="magenta", label="base layer")
    plt.axhline(upper_layer, linestyle="--", color="orange", label="upper layer")

    plt.scatter(original[-1, 0], original[-1, 1], color="red", label="orig end")
    plt.scatter(controlled[-1, 0], controlled[-1, 1], color="orange")

    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "final_controller_v9_dual_layer.png")
    plt.savefig(save_path, dpi=150)
    print(f"💾 Saved → {save_path}")

    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    trajectory, rift = load_data()

    controlled, base_layer, upper_layer = dual_layer_controller(trajectory, rift)

    # save
    np.save(os.path.join(RIFT_DIR, "final_controller_v9.npy"), controlled)
    print("💾 Saved controlled trajectory → final_controller_v9.npy")

    plot_result(trajectory, controlled, rift, base_layer, upper_layer)

    print("🚀 FINAL CONTROLLER V9 (DUAL LAYER) complete")


if __name__ == "__main__":
    main()
