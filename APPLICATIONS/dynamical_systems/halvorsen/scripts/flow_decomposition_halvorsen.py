# ============================================================
# NEXAH — Dual System Overlay
# Lorenz ↔ Halvorsen Structural Comparison
# ============================================================

import os
import glob
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt


def load_halvorsen_matrix():
    base = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    patterns = [
        "gate_aware_policy_matrix_*.npy",
        "adaptive_matrix_*.npy",
        "coarse_matrix_*.npy",
    ]

    for pattern in patterns:
        files = sorted(glob.glob(os.path.join(base, pattern)))
        if files:
            path = files[-1]
            print(f"→ loading Halvorsen: {path}")
            return np.load(path), path

    raise RuntimeError("No Halvorsen matrix found.")


def synthetic_lorenz_reference():
    """
    Minimal Lorenz-like reference matrix:
    two regimes + transition corridor.
    Not a Lorenz simulation.
    Used only as structural comparison.
    """

    M = np.array([
        [0.85, 0.10, 0.05],
        [0.10, 0.85, 0.05],
        [0.45, 0.45, 0.10],
    ])

    return M


def extract_signature(M):
    diag_strength = np.mean(np.diag(M))

    movement = M.copy()
    np.fill_diagonal(movement, 0.0)

    offdiag_mass = movement.sum() / M.shape[0]
    max_gate = movement.max()
    active_edges = np.sum(movement > 0.05)

    return {
        "diag_strength": diag_strength,
        "offdiag_mass": offdiag_mass,
        "max_gate": max_gate,
        "active_edges": active_edges,
    }


def save_outputs(lorenz_ref, halvorsen, sig_lorenz, sig_halvorsen, source):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    os.makedirs(base, exist_ok=True)

    txt_path = f"{base}/dual_system_overlay_{timestamp}.txt"
    with open(txt_path, "w") as f:
        f.write("NEXAH — Dual System Overlay\n")
        f.write("=" * 60 + "\n\n")
        f.write("NOTE\n")
        f.write("-" * 60 + "\n")
        f.write("Lorenz reference is synthetic and structural only.\n")
        f.write("It is not a simulation output.\n\n")

        f.write(f"Halvorsen source: {source}\n\n")

        f.write("LORENZ-LIKE SIGNATURE\n")
        f.write("-" * 60 + "\n")
        for k, v in sig_lorenz.items():
            f.write(f"{k}: {v}\n")

        f.write("\nHALVORSEN SIGNATURE\n")
        f.write("-" * 60 + "\n")
        for k, v in sig_halvorsen.items():
            f.write(f"{k}: {v}\n")

        f.write("\nINTERPRETATION\n")
        f.write("-" * 60 + "\n")
        f.write("Lorenz-like: discrete regime switching.\n")
        f.write("Halvorsen: distributed cyclic transition structure.\n")
        f.write("They should not be overlaid geometrically.\n")
        f.write("They can be compared structurally via transition topology.\n")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].imshow(lorenz_ref)
    axes[0].set_title("Lorenz-like Reference\nDiscrete Regime Switch")

    axes[1].imshow(halvorsen)
    axes[1].set_title("Halvorsen\nCyclic / Distributed Flow")

    for ax in axes:
        ax.set_xlabel("to state / cluster")
        ax.set_ylabel("from state / cluster")

    plt.tight_layout()
    png_path = f"{base}/dual_system_overlay_{timestamp}.png"
    plt.savefig(png_path, dpi=300)
    plt.close()

    print(f"[✓] TXT saved: {txt_path}")
    print(f"[✓] PNG saved: {png_path}")


if __name__ == "__main__":
    print("→ load Halvorsen matrix")
    H, source = load_halvorsen_matrix()

    print("→ build Lorenz-like reference")
    L = synthetic_lorenz_reference()

    print("→ extract signatures")
    sig_lorenz = extract_signature(L)
    sig_halvorsen = extract_signature(H)

    print("Lorenz-like:", sig_lorenz)
    print("Halvorsen:", sig_halvorsen)

    print("→ save")
    save_outputs(L, H, sig_lorenz, sig_halvorsen, source)

    print("✔ DONE")
