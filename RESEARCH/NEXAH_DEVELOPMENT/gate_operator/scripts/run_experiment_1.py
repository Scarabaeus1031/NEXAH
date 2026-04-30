# NEXAH — Gate Operator Experiment 1 (Lorenz Baseline)
# Location:
# RESEARCH/NEXAH_DEVELOPMENT/gate_operator/scripts/run_experiment_1.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================================
# 1. SYSTEM: LORENZ
# ============================================================

def lorenz(x, y, z, s=10, r=28, b=8/3):
    dx = s * (y - x)
    dy = x * (r - z) - y
    dz = x * y - b * z
    return dx, dy, dz


def simulate_lorenz(steps=8000, dt=0.01):
    xs = np.zeros(steps)
    ys = np.zeros(steps)
    zs = np.zeros(steps)

    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

    for i in range(steps - 1):
        dx, dy, dz = lorenz(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx * dt
        ys[i+1] = ys[i] + dy * dt
        zs[i+1] = zs[i] + dz * dt

    return xs, ys, zs


# ============================================================
# 2. DENSITY FIELD (ρ)
# ============================================================

def compute_density(xs, ys, grid_n=250):
    data = np.vstack([xs, ys])
    kde = gaussian_kde(data)

    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()

    X, Y = np.mgrid[xmin:xmax:complex(grid_n), ymin:ymax:complex(grid_n)]
    Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

    return X, Y, Z


# ============================================================
# 3. FLOW FIELD APPROXIMATION
# ============================================================

def compute_flow(xs, ys):
    dx = np.gradient(xs)
    dy = np.gradient(ys)
    return dx, dy


# ============================================================
# 4. ROTATION (R)
# ============================================================

def compute_rotation(Z):
    dZdx, dZdy = np.gradient(Z)
    R = np.sqrt(dZdx**2 + dZdy**2)
    return R


# ============================================================
# 5. COHERENCE (C) — SIMPLE PROXY
# ============================================================

def compute_coherence(xs, ys):
    dx = np.gradient(xs)
    dy = np.gradient(ys)

    mag = np.sqrt(dx**2 + dy**2) + 1e-8
    C = (dx / mag)**2 + (dy / mag)**2  # proxy: directional consistency

    return C


# ============================================================
# 6. NORMALIZATION
# ============================================================

def normalize(field):
    f_min, f_max = np.min(field), np.max(field)
    return (field - f_min) / (f_max - f_min + 1e-8)


# ============================================================
# 7. GATE OPERATOR
# ============================================================

def compute_gate(Z, R):
    rho_hat = normalize(Z)
    R_hat = normalize(R)

    # NOTE: coherence not spatially aligned yet → skip for v1
    G = (1 - rho_hat) * (1 - R_hat)

    return G


# ============================================================
# 8. MAIN PIPELINE
# ============================================================

def main():

    print("Running Experiment 1 — Lorenz Baseline")

    # simulate
    xs, ys, zs = simulate_lorenz()

    # density
    X, Y, Z = compute_density(xs, ys)

    # rotation
    R = compute_rotation(Z)

    # gate operator (v1: rho + rotation)
    G = compute_gate(Z, R)

    extent = [xs.min(), xs.max(), ys.min(), ys.max()]

    # ========================================================
    # PLOT
    # ========================================================

    fig, axes = plt.subplots(1, 4, figsize=(18, 4))

    # Trajectory
    axes[0].plot(xs, ys, lw=0.3)
    axes[0].set_title("Trajectory")
    axes[0].axis("off")

    # Density
    axes[1].imshow(np.rot90(Z), cmap="viridis", extent=extent)
    axes[1].set_title("Density ρ(x)")
    axes[1].axis("off")

    # Rotation
    axes[2].imshow(np.rot90(R), cmap="plasma", extent=extent)
    axes[2].set_title("Rotation Proxy R(x)")
    axes[2].axis("off")

    # Gate
    axes[3].imshow(np.rot90(G), cmap="inferno", extent=extent)
    axes[3].set_title("Gate Field G(x)")
    axes[3].axis("off")

    plt.suptitle("NEXAH Experiment 1 — Gate Operator (Lorenz)", fontsize=14)
    plt.tight_layout()

    plt.savefig(
        "RESEARCH/NEXAH_DEVELOPMENT/gate_operator/experiment_1_result.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
