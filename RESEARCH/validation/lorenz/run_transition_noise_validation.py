"""
NEXAH — Transition Structure Noise Validation

Compares transition matrices between:
- clean Lorenz runs
- noisy Lorenz runs

Goal:
Check if transition structure is robust under noise.
"""

import numpy as np
import matplotlib.pyplot as plt
import os


# =========================
# Lorenz System
# =========================

def lorenz_step(x, y, z, sigma=10.0, rho=28.0, beta=8/3):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz


def simulate_lorenz(n_steps=5000, dt=0.01, noise=0.0):
    x, y, z = 1.0, 1.0, 1.0

    traj = []

    for _ in range(n_steps):
        dx, dy, dz = lorenz_step(x, y, z)

        # noise injection
        dx += noise * np.random.randn()
        dy += noise * np.random.randn()
        dz += noise * np.random.randn()

        x += dx * dt
        y += dy * dt
        z += dz * dt

        traj.append([x, y, z])

    return np.array(traj)


# =========================
# Simple Sheet Partition
# =========================

def assign_sheets(traj, n_sheets=6):
    """
    Simple partition based on x-coordinate
    (can be replaced with your real sheet logic later)
    """
    x = traj[:, 0]
    bins = np.linspace(np.min(x), np.max(x), n_sheets + 1)
    sheets = np.digitize(x, bins) - 1
    sheets = np.clip(sheets, 0, n_sheets - 1)
    return sheets


# =========================
# Transition Matrix
# =========================

def compute_transition_matrix(sheets, n_sheets):
    T = np.zeros((n_sheets, n_sheets))

    for i in range(len(sheets) - 1):
        a = sheets[i]
        b = sheets[i + 1]
        T[a, b] += 1

    # normalize
    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    T = T / row_sums

    return T


# =========================
# Multi-run Aggregation
# =========================

def aggregate_transition_matrix(n_runs=10, noise=0.0, n_sheets=6):
    matrices = []

    for _ in range(n_runs):
        traj = simulate_lorenz(noise=noise)
        sheets = assign_sheets(traj, n_sheets)
        T = compute_transition_matrix(sheets, n_sheets)
        matrices.append(T)

    return np.mean(matrices, axis=0)


# =========================
# Main Validation
# =========================

def main():
    out_dir = "RESEARCH/validation/lorenz/results"
    os.makedirs(out_dir, exist_ok=True)

    n_runs = 10
    noise_level = 1.0
    n_sheets = 6

    print("Running transition noise validation...")

    T_clean = aggregate_transition_matrix(n_runs, noise=0.0, n_sheets=n_sheets)
    T_noisy = aggregate_transition_matrix(n_runs, noise=noise_level, n_sheets=n_sheets)

    diff = np.abs(T_clean - T_noisy)
    mean_diff = np.mean(diff)

    print("\n=== TRANSITION VALIDATION ===")
    print(f"Runs: {n_runs}")
    print(f"Noise level: {noise_level}")
    print(f"Mean transition difference: {mean_diff:.4f}")

    # =========================
    # Plot
    # =========================

    fig, axs = plt.subplots(1, 3, figsize=(15, 4))

    im0 = axs[0].imshow(T_clean)
    axs[0].set_title("Clean Transition Matrix")
    plt.colorbar(im0, ax=axs[0])

    im1 = axs[1].imshow(T_noisy)
    axs[1].set_title("Noisy Transition Matrix")
    plt.colorbar(im1, ax=axs[1])

    im2 = axs[2].imshow(diff)
    axs[2].set_title("Absolute Difference")
    plt.colorbar(im2, ax=axs[2])

    plt.tight_layout()

    path = os.path.join(out_dir, "transition_noise_comparison.png")
    plt.savefig(path, dpi=200)
    print(f"✅ Saved: {path}")

    # =========================
    # Save summary
    # =========================

    summary = f"""NEXAH — Transition Noise Validation

Runs: {n_runs}
Noise level: {noise_level}

Mean transition difference: {mean_diff:.4f}
"""

    summary_path = os.path.join(out_dir, "transition_noise_summary.txt")
    with open(summary_path, "w") as f:
        f.write(summary)

    print(f"✅ Saved summary: {summary_path}")
    print("\n✅ Validation complete.")


if __name__ == "__main__":
    main()
