# NEXAH — Gate Operator Experiment 3 (Ablation Study)

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================================
# SYSTEM (Lorenz)
# ============================================================

def lorenz(x, y, z, s=10, r=28, b=8/3):
    return s*(y-x), x*(r-z)-y, x*y - b*z

def simulate(steps=8000, dt=0.01):
    xs, ys, zs = np.zeros(steps), np.zeros(steps), np.zeros(steps)
    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

    for i in range(steps - 1):
        dx, dy, dz = lorenz(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx*dt
        ys[i+1] = ys[i] + dy*dt
        zs[i+1] = zs[i] + dz*dt

    return xs, ys

# ============================================================
# FIELD
# ============================================================

def density(xs, ys, grid_n=220):
    kde = gaussian_kde(np.vstack([xs, ys]))

    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()

    X, Y = np.mgrid[xmin:xmax:complex(grid_n), ymin:ymax:complex(grid_n)]
    Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

    return X, Y, Z

def rotation(Z):
    dZdx, dZdy = np.gradient(Z)
    return np.sqrt(dZdx**2 + dZdy**2)

def normalize(Z):
    return (Z - Z.min()) / (Z.max() - Z.min() + 1e-8)

# ============================================================
# GATE VARIANTS
# ============================================================

def gate_density(Z):
    return (1 - normalize(Z))

def gate_rotation(R):
    return (1 - normalize(R))

def gate_full(Z, R):
    return (1 - normalize(Z)) * (1 - normalize(R))

# ============================================================
# MAIN
# ============================================================

def main():

    print("Running Experiment 3 — Ablation Study")

    xs, ys = simulate()
    X, Y, Z = density(xs, ys)
    R = rotation(Z)

    G_rho = gate_density(Z)
    G_rot = gate_rotation(R)
    G_full = gate_full(Z, R)

    extent = [xs.min(), xs.max(), ys.min(), ys.max()]

    fig, axes = plt.subplots(1, 5, figsize=(18, 4))

    # Trajectory
    axes[0].plot(xs, ys, lw=0.3)
    axes[0].set_title("Trajectory")
    axes[0].axis("off")

    # Density
    axes[1].imshow(np.rot90(Z), cmap="viridis", extent=extent)
    axes[1].set_title("Density ρ(x)")
    axes[1].axis("off")

    # Density Gate
    axes[2].imshow(np.rot90(G_rho), cmap="inferno", extent=extent)
    axes[2].set_title("G₁ = 1 - ρ̂")
    axes[2].axis("off")

    # Rotation Gate
    axes[3].imshow(np.rot90(G_rot), cmap="plasma", extent=extent)
    axes[3].set_title("G₂ = 1 - R̂")
    axes[3].axis("off")

    # Full Gate
    axes[4].imshow(np.rot90(G_full), cmap="inferno", extent=extent)
    axes[4].set_title("G_full")
    axes[4].axis("off")

    plt.suptitle(
        "NEXAH Experiment 3 — Component Ablation\n"
        "Which component defines the gate?",
        fontsize=14
    )

    plt.tight_layout()

    plt.savefig(
        "RESEARCH/NEXAH_DEVELOPMENT/gate_operator/output_results/experiment_3_result.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

# ============================================================

if __name__ == "__main__":
    main()
