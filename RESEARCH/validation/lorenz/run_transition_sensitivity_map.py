"""
NEXAH — Transition Sensitivity Map

Goal:
Identify which transitions are sensitive to noise.

Output:
- mean difference matrix
- variance matrix
- sensitivity heatmap
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

        dx += noise * np.random.randn()
        dy += noise * np.random.randn()
        dz += noise * np.random.randn()

        x += dx * dt
        y += dy * dt
        z += dz * dt

        traj.append([x, y, z])

    return np.array(traj)


# =========================
# Sheet Assignment
# =========================

def assign_sheets(traj, n_sheets=6):
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
        T[sheets[i], sheets[i + 1]] += 1

    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    return T / row_sums


# =========================
# Multi-run Collection
# =========================

def collect_matrices(n_runs, noise, n_sheets):
    matrices = []

    for _ in range(n_runs):
        traj = simulate_lorenz(noise=noise)
        sheets = assign_sheets(traj, n_sheets)
        T = compute_transition_matrix(sheets, n_sheets)
        matrices.append(T)

    return np.array(matrices)


# =========================
# MAIN
# =========================

def main():
    out_dir = "RESEARCH/validation/lorenz/results"
    os.makedirs(out_dir, exist_ok=True)

    n_runs = 20
    noise_level = 1.0
    n_sheets = 6

    print("Running transition sensitivity analysis...")

    clean = collect_matrices(n_runs, noise=0.0, n_sheets=n_sheets)
    noisy = collect_matrices(n_runs, noise=noise_level, n_sheets=n_sheets)

    # mean matrices
    T_clean = np.mean(clean, axis=0)
    T_noisy = np.mean(noisy, axis=0)

    # absolute diff
    diff = np.abs(T_clean - T_noisy)

    # variance across runs (important!)
    var_clean = np.var(clean, axis=0)
    var_noisy = np.var(noisy, axis=0)

    # sensitivity = diff + variability
    sensitivity = diff + var_noisy

    print("\n=== TRANSITION SENSITIVITY ===")
    print(f"Mean diff: {np.mean(diff):.6f}")
    print(f"Mean variance (noisy): {np.mean(var_noisy):.6f}")

    # =========================
    # PLOTS
    # =========================

    fig, axs = plt.subplots(2, 3, figsize=(15, 8))

    axs[0, 0].imshow(T_clean)
    axs[0, 0].set_title("Clean Mean")

    axs[0, 1].imshow(T_noisy)
    axs[0, 1].set_title("Noisy Mean")

    im = axs[0, 2].imshow(diff)
    axs[0, 2].set_title("Absolute Difference")
    plt.colorbar(im, ax=axs[0, 2])

    axs[1, 0].imshow(var_clean)
    axs[1, 0].set_title("Clean Variance")

    axs[1, 1].imshow(var_noisy)
    axs[1, 1].set_title("Noisy Variance")

    im2 = axs[1, 2].imshow(sensitivity)
    axs[1, 2].set_title("Sensitivity Map")
    plt.colorbar(im2, ax=axs[1, 2])

    plt.tight_layout()

    path = os.path.join(out_dir, "transition_sensitivity_map.png")
    plt.savefig(path, dpi=200)
    print(f"✅ Saved: {path}")

    # =========================
    # SUMMARY
    # =========================

    summary = f"""NEXAH — Transition Sensitivity

Runs: {n_runs}
Noise: {noise_level}

Mean diff: {np.mean(diff):.6f}
Mean noisy variance: {np.mean(var_noisy):.6f}
"""

    with open(os.path.join(out_dir, "transition_sensitivity_summary.txt"), "w") as f:
        f.write(summary)

    print("✅ Done.")


if __name__ == "__main__":
    main()
