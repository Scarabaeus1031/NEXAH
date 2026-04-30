# NEXAH — Experiment 3.1 (Transition Alignment)

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================================
# SYSTEM
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

    return xs, ys, zs

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
# INTERPOLATION
# ============================================================

def interp(X, Y, Z, x, y):
    xi = np.searchsorted(X[:,0], x) - 1
    yi = np.searchsorted(Y[0,:], y) - 1

    xi = np.clip(xi, 0, Z.shape[0]-1)
    yi = np.clip(yi, 0, Z.shape[1]-1)

    return Z[xi, yi]

# ============================================================
# TRANSITION DETECTION
# ============================================================

def detect_transitions(xs):
    signs = np.sign(xs)
    transitions = np.where(np.diff(signs) != 0)[0]
    return transitions

# ============================================================
# MAIN
# ============================================================

def main():

    print("Running Experiment 3.1 — Transition Alignment")

    xs, ys, zs = simulate()
    X, Y, Z = density(xs, ys)
    R = rotation(Z)
    G = gate(Z, R)

    # detect transitions
    transition_idx = detect_transitions(xs)

    # sample G along trajectory
    G_vals = []
    for i in range(len(xs)):
        g_val = interp(X, Y, G, xs[i], ys[i])
        G_vals.append(g_val)

    G_vals = np.array(G_vals)

    # split values
    G_transition = G_vals[transition_idx]
    G_normal = np.delete(G_vals, transition_idx)

    # ============================================================
    # PLOT
    # ============================================================

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # trajectory with transitions
    axes[0].plot(xs, ys, lw=0.3)
    axes[0].scatter(xs[transition_idx], ys[transition_idx],
                    color='red', s=10, label="Transitions")
    axes[0].set_title("Trajectory + Transitions")
    axes[0].axis("off")

    # G distribution
    axes[1].hist(G_normal, bins=50, alpha=0.6, label="Normal")
    axes[1].hist(G_transition, bins=50, alpha=0.6, label="Transitions")
    axes[1].set_title("G(x) Distribution")
    axes[1].legend()

    # G over time
    axes[2].plot(G_vals, lw=1)
    axes[2].scatter(transition_idx, G_vals[transition_idx],
                    color='red', s=10)
    axes[2].set_title("G(x) over Time")

    plt.suptitle("Experiment 3.1 — Gate Alignment with Transitions")

    plt.tight_layout()

    plt.savefig(
        "RESEARCH/NEXAH_DEVELOPMENT/gate_operator/output_results/experiment_3_1_result.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

# ============================================================

if __name__ == "__main__":
    main()
