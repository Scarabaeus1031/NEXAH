# NEXAH — Gate Operator Experiment 2 (Cross-System Consistency)

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================================
# SYSTEMS
# ============================================================

def lorenz(x, y, z, s=10, r=28, b=8/3):
    return s*(y-x), x*(r-z)-y, x*y - b*z

def rossler(x, y, z, a=0.2, b=0.2, c=5.7):
    dx = -y - z
    dy = x + a*y
    dz = b + z*(x - c)
    return dx, dy, dz

def simulate_3d(system, steps=8000, dt=0.01):
    xs, ys, zs = np.zeros(steps), np.zeros(steps), np.zeros(steps)
    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

    for i in range(steps - 1):
        dx, dy, dz = system(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx*dt
        ys[i+1] = ys[i] + dy*dt
        zs[i+1] = zs[i] + dz*dt

    return xs, ys

# ============================================================
# KURAMOTO (2D projection)
# ============================================================

def simulate_kuramoto(n=64, steps=4000, dt=0.05, K=2.0):
    theta = np.random.uniform(0, 2*np.pi, n)
    omega = np.random.normal(0, 0.5, n)

    r_vals = []
    psi_vals = []

    for _ in range(steps):
        order = np.mean(np.exp(1j * theta))
        r = np.abs(order)
        psi = np.angle(order)

        theta += dt * (omega + K*r*np.sin(psi - theta))
        theta = np.mod(theta, 2*np.pi)

        r_vals.append(r)
        psi_vals.append(psi)

    return np.array(r_vals), np.unwrap(np.array(psi_vals))

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

def gate(Z, R):
    return (1 - normalize(Z)) * (1 - normalize(R))

# ============================================================
# RUN ONE SYSTEM
# ============================================================

def run_system(xs, ys, title, ax_row):

    X, Y, Z = density(xs, ys)
    R = rotation(Z)
    G = gate(Z, R)

    extent = [xs.min(), xs.max(), ys.min(), ys.max()]

    # Trajectory
    ax_row[0].plot(xs, ys, lw=0.3)
    ax_row[0].set_title(f"{title} — Trajectory")
    ax_row[0].axis("off")

    # Density
    ax_row[1].imshow(np.rot90(Z), cmap="viridis", extent=extent)
    ax_row[1].set_title("Density")
    ax_row[1].axis("off")

    # Rotation
    ax_row[2].imshow(np.rot90(R), cmap="plasma", extent=extent)
    ax_row[2].set_title("Rotation")
    ax_row[2].axis("off")

    # Gate
    ax_row[3].imshow(np.rot90(G), cmap="inferno", extent=extent)
    ax_row[3].set_title("Gate G(x)")
    ax_row[3].axis("off")

# ============================================================
# MAIN
# ============================================================

def main():

    print("Running Experiment 2 — Cross-System Consistency")

    fig, axes = plt.subplots(3, 4, figsize=(16, 10))

    # Lorenz
    xs, ys = simulate_3d(lorenz)
    run_system(xs, ys, "Lorenz", axes[0])

    # Rössler
    xs, ys = simulate_3d(rossler)
    run_system(xs, ys, "Rössler", axes[1])

    # Kuramoto (2D projection)
    xs, ys = simulate_kuramoto()
    run_system(xs, ys, "Kuramoto", axes[2])

    plt.suptitle("NEXAH Experiment 2 — Cross-System Gate Structure", fontsize=16)
    plt.tight_layout()

    plt.savefig(
        "RESEARCH/NEXAH_DEVELOPMENT/gate_operator/output_results/experiment_2_result.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

# ============================================================

if __name__ == "__main__":
    main()
