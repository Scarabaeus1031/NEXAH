# ============================================================
# NEXAH — Flow Signature Visualization (Halvorsen)
# ============================================================
#
# Purpose:
# Create higher-level structural visuals from the Halvorsen
# transition / policy matrix.
#
# Visuals:
# 1. Stability vs Movement Signature
# 2. Flow Energy Map
# 3. Gate Influence Field
# 4. Flow Signature Summary
#
# Input priority:
# - latest gate_aware_policy_matrix_*.npy
# - latest policy_gradient_matrix_*.npy
# - latest adaptive_matrix_*.npy
# - latest connected_matrix_*.npy
# - latest coarse_matrix_*.npy
#
# Outputs:
# - flow_signature_*.txt
# - flow_signature_stability_movement_*.png
# - flow_signature_energy_map_*.png
# - flow_signature_gate_field_*.png
# - flow_signature_summary_*.png
#
# ============================================================

import os
import glob
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# LOAD MATRIX
# ============================================================

def load_latest_matrix():
    base = "APPLICATIONS/dynamical_systems/halvorsen/outputs"

    patterns = [
        "gate_aware_policy_matrix_*.npy",
        "policy_gradient_matrix_*.npy",
        "adaptive_matrix_*.npy",
        "connected_matrix_*.npy",
        "coarse_matrix_*.npy",
    ]

    for pattern in patterns:
        files = sorted(glob.glob(os.path.join(base, pattern)))
        if files:
            path = files[-1]
            print(f"→ loading matrix: {path}")
            return np.load(path), path

    raise RuntimeError("No matrix found.")


# ============================================================
# SIGNATURE EXTRACTION
# ============================================================

def compute_signature(M):
    diagonal = np.diag(M)

    movement = M.copy()
    np.fill_diagonal(movement, 0.0)

    stability_mass = diagonal
    movement_mass = movement.sum(axis=1)

    total_stability = stability_mass.mean()
    total_movement = movement_mass.mean()

    max_gate = movement.max()
    active_edges = int(np.sum(movement > 0.05))

    entropy = []
    for i in range(M.shape[0]):
        row = M[i]
        row = row[row > 0]
        if len(row) == 0:
            entropy.append(0.0)
        else:
            entropy.append(float(-np.sum(row * np.log(row))))

    entropy = np.array(entropy)

    gate_field = movement / (diagonal[:, None] + 1e-9)

    return {
        "diagonal": diagonal,
        "movement": movement,
        "stability_mass": stability_mass,
        "movement_mass": movement_mass,
        "total_stability": total_stability,
        "total_movement": total_movement,
        "max_gate": max_gate,
        "active_edges": active_edges,
        "entropy": entropy,
        "gate_field": gate_field,
    }


# ============================================================
# SAVE REPORT
# ============================================================

def save_report(sig, source, timestamp, base):
    path = f"{base}/flow_signature_{timestamp}.txt"

    with open(path, "w") as f:
        f.write("NEXAH — Halvorsen Flow Signature\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Source matrix: {source}\n\n")

        f.write("GLOBAL SIGNATURE\n")
        f.write("-" * 60 + "\n")
        f.write(f"mean stability mass: {sig['total_stability']:.6f}\n")
        f.write(f"mean movement mass: {sig['total_movement']:.6f}\n")
        f.write(f"max gate strength: {sig['max_gate']:.6f}\n")
        f.write(f"active edges > 0.05: {sig['active_edges']}\n\n")

        f.write("LOCAL SIGNATURE\n")
        f.write("-" * 60 + "\n")
        for i in range(len(sig["diagonal"])):
            f.write(
                f"{i}: stability={sig['stability_mass'][i]:.4f} "
                f"movement={sig['movement_mass'][i]:.4f} "
                f"entropy={sig['entropy'][i]:.4f}\n"
            )

    print(f"[✓] Report saved: {path}")


# ============================================================
# VISUAL 1 — STABILITY VS MOVEMENT
# ============================================================

def plot_stability_movement(sig, timestamp, base):
    x = np.arange(len(sig["stability_mass"]))

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, sig["stability_mass"], marker="o", label="stability / diagonal")
    ax.plot(x, sig["movement_mass"], marker="x", label="movement / off-diagonal")
    ax.plot(x, sig["entropy"], marker=".", label="transition entropy")

    ax.set_title("Halvorsen Flow Signature — Stability vs Movement")
    ax.set_xlabel("cluster")
    ax.set_ylabel("mass / entropy")
    ax.legend()
    ax.grid(alpha=0.25)

    plt.tight_layout()
    path = f"{base}/flow_signature_stability_movement_{timestamp}.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)

    print(f"[✓] Stability/movement plot saved: {path}")


# ============================================================
# VISUAL 2 — FLOW ENERGY MAP
# ============================================================

def plot_energy_map(sig, timestamp, base):
    energy = sig["movement"]

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(energy)

    ax.set_title("Halvorsen Flow Energy Map\nOff-Diagonal Movement Only")
    ax.set_xlabel("to cluster")
    ax.set_ylabel("from cluster")
    plt.colorbar(im)

    plt.tight_layout()
    path = f"{base}/flow_signature_energy_map_{timestamp}.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)

    print(f"[✓] Energy map saved: {path}")


# ============================================================
# VISUAL 3 — GATE INFLUENCE FIELD
# ============================================================

def plot_gate_field(sig, timestamp, base):
    gate_field = sig["gate_field"].copy()
    np.fill_diagonal(gate_field, 0.0)

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(gate_field)

    ax.set_title("Halvorsen Gate Influence Field\nOff-Diagonal / Stability Ratio")
    ax.set_xlabel("to cluster")
    ax.set_ylabel("from cluster")
    plt.colorbar(im)

    plt.tight_layout()
    path = f"{base}/flow_signature_gate_field_{timestamp}.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)

    print(f"[✓] Gate field saved: {path}")


# ============================================================
# VISUAL 4 — SUMMARY PANEL
# ============================================================

def plot_summary(M, sig, timestamp, base):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    im0 = axes[0, 0].imshow(M)
    axes[0, 0].set_title("Full Policy / Transition Matrix")
    plt.colorbar(im0, ax=axes[0, 0])

    im1 = axes[0, 1].imshow(sig["movement"])
    axes[0, 1].set_title("Movement Layer")
    plt.colorbar(im1, ax=axes[0, 1])

    im2 = axes[1, 0].imshow(sig["gate_field"])
    axes[1, 0].set_title("Gate Influence Field")
    plt.colorbar(im2, ax=axes[1, 0])

    x = np.arange(len(sig["stability_mass"]))
    axes[1, 1].plot(x, sig["stability_mass"], marker="o", label="stability")
    axes[1, 1].plot(x, sig["movement_mass"], marker="x", label="movement")
    axes[1, 1].plot(x, sig["entropy"], marker=".", label="entropy")
    axes[1, 1].set_title("Local Flow Signature")
    axes[1, 1].set_xlabel("cluster")
    axes[1, 1].legend()
    axes[1, 1].grid(alpha=0.25)

    for ax in axes.flat[:3]:
        ax.set_xlabel("to cluster")
        ax.set_ylabel("from cluster")

    plt.tight_layout()
    path = f"{base}/flow_signature_summary_{timestamp}.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)

    print(f"[✓] Summary saved: {path}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    base = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    os.makedirs(base, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("→ load matrix")
    M, source = load_latest_matrix()

    print("→ compute signature")
    sig = compute_signature(M)

    print("→ save report")
    save_report(sig, source, timestamp, base)

    print("→ create visuals")
    plot_stability_movement(sig, timestamp, base)
    plot_energy_map(sig, timestamp, base)
    plot_gate_field(sig, timestamp, base)
    plot_summary(M, sig, timestamp, base)

    print("✔ DONE")
