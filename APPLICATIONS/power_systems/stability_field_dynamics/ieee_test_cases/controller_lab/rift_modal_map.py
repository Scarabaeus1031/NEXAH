# rift_modal_map.py

import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")


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

    if trajectory.shape[1] < 2:
        raise ValueError("❌ Need at least 2 dimensions for modal map")

    return trajectory


def compute_instability(signal):
    velocity = np.diff(signal)
    instability = np.abs(velocity)
    return instability


def detect_events(instability, threshold_factor=2.0):
    mean = np.mean(instability)
    std = np.std(instability)
    threshold = mean + threshold_factor * std
    events = np.where(instability > threshold)[0]
    return events, threshold


def plot_modal_map(pc1, pc2, events1, events2):
    plt.figure(figsize=(9, 7))

    # base trajectory
    plt.plot(pc1, pc2, color="lightgray", linewidth=1.5, label="trajectory")

    # event points for PC1-instability
    if len(events1) > 0:
        plt.scatter(
            pc1[events1 + 1],
            pc2[events1 + 1],
            color="red",
            s=70,
            label="PC1 instability"
        )

    # event points for PC2-instability
    if len(events2) > 0:
        plt.scatter(
            pc1[events2 + 1],
            pc2[events2 + 1],
            color="blue",
            s=70,
            marker="x",
            label="PC2 instability"
        )

    # annotate event ids
    all_events = sorted(set(list(events1) + list(events2)))
    for idx in all_events:
        plt.text(
            pc1[idx + 1],
            pc2[idx + 1],
            str(idx),
            fontsize=8
        )

    plt.title("Modal Map — Instability in Phase Space")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "modal_map.png")
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"💾 Saved → {save_path}")

    plt.show(block=False)
    plt.pause(0.1)


def plot_event_timeline(events1, events2, n_steps):
    plt.figure(figsize=(10, 3))

    if len(events1) > 0:
        plt.scatter(events1, np.ones_like(events1), color="red", label="PC1 events")

    if len(events2) > 0:
        plt.scatter(events2, np.ones_like(events2) * 0.8, color="blue", marker="x", label="PC2 events")

    plt.yticks([0.8, 1.0], ["PC2", "PC1"])
    plt.ylim(0.6, 1.2)
    plt.xlim(0, n_steps)
    plt.title("Instability Event Timeline")
    plt.xlabel("time step")
    plt.legend()
    plt.grid(True, axis="x")

    save_path = os.path.join(RIFT_DIR, "modal_event_timeline.png")
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"💾 Saved → {save_path}")

    plt.show(block=False)
    plt.pause(0.1)


def main():
    trajectory = load_data()

    # optional downsampling to keep things light
    trajectory = trajectory[::2]

    pc1 = trajectory[:, 0]
    pc2 = trajectory[:, 1]

    inst1 = compute_instability(pc1)
    inst2 = compute_instability(pc2)

    events1, th1 = detect_events(inst1)
    events2, th2 = detect_events(inst2)

    print(f"✅ PC1 threshold: {th1:.4f} | events: {len(events1)}")
    print(f"✅ PC2 threshold: {th2:.4f} | events: {len(events2)}")

    if len(events1) > 0:
        print("🔍 PC1 event steps:", events1.tolist())
    if len(events2) > 0:
        print("🔍 PC2 event steps:", events2.tolist())

    plot_modal_map(pc1, pc2, events1, events2)
    plot_event_timeline(events1, events2, len(pc1))

    print("🚀 Modal map complete")


if __name__ == "__main__":
    main()
