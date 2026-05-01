# ============================================================
# NEXAH HERO VISUAL v4
# Cross-System Structure Extraction:
# Lorenz + Halvorsen → Basins → Transition Field → Gates
#
# Output:
# NEXAH_DEMONSTRATOR/visuals/nexah_hero_cross_system_structure_v4.png
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from sklearn.cluster import KMeans


# ============================================================
# 1. SYSTEM DEFINITIONS
# ============================================================

def lorenz_step(x, y, z, sigma=10.0, rho=28.0, beta=8.0 / 3.0):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz


def halvorsen_step(x, y, z, a=1.4):
    dx = -a * x - 4.0 * y - 4.0 * z - y * y
    dy = -a * y - 4.0 * z - 4.0 * x - z * z
    dz = -a * z - 4.0 * x - 4.0 * y - x * x
    return dx, dy, dz


def simulate_system(step_fn, initial_state, dt=0.01, steps=16000, burn=1000):
    xs = np.empty(steps)
    ys = np.empty(steps)
    zs = np.empty(steps)

    xs[0], ys[0], zs[0] = initial_state

    for i in range(steps - 1):
        dx, dy, dz = step_fn(xs[i], ys[i], zs[i])
        xs[i + 1] = xs[i] + dx * dt
        ys[i + 1] = ys[i] + dy * dt
        zs[i + 1] = zs[i] + dz * dt

    return xs[burn:], ys[burn:], zs[burn:]


# ============================================================
# 2. FIELD EXTRACTION PIPELINE
# ============================================================

def extract_nexah_structure(xs, ys, n_grid=250, n_basins=3):
    points = np.vstack([xs, ys])
    data = points.T

    vx = np.gradient(xs)
    vy = np.gradient(ys)

    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()

    kde = gaussian_kde(points)

    X, Y = np.mgrid[xmin:xmax:complex(n_grid), ymin:ymax:complex(n_grid)]
    positions = np.vstack([X.ravel(), Y.ravel()])
    Z = np.reshape(kde(positions).T, X.shape)

    dZdx, dZdy = np.gradient(Z)

    mag = np.sqrt(dZdx**2 + dZdy**2) + 1e-8
    Fx = dZdx / mag
    Fy = dZdy / mag

    def sample_grid(field, x, y):
        xi = np.clip(
            ((x - xmin) / (xmax - xmin) * (field.shape[0] - 1)).astype(int),
            0,
            field.shape[0] - 1,
        )
        yi = np.clip(
            ((y - ymin) / (ymax - ymin) * (field.shape[1] - 1)).astype(int),
            0,
            field.shape[1] - 1,
        )
        return field[xi, yi]

    Fx_t = sample_grid(Fx, xs, ys)
    Fy_t = sample_grid(Fy, xs, ys)
    rho_t = sample_grid(Z, xs, ys)

    vel_mag = np.sqrt(vx**2 + vy**2) + 1e-8
    field_mag = np.sqrt(Fx_t**2 + Fy_t**2) + 1e-8

    coherence = (vx * Fx_t + vy * Fy_t) / (vel_mag * field_mag)

    # Basin segmentation
    kmeans = KMeans(n_clusters=n_basins, random_state=42, n_init=10)
    labels = kmeans.fit_predict(data)
    centers = kmeans.cluster_centers_

    # Grid basin labels
    grid_points = np.vstack([X.ravel(), Y.ravel()]).T
    grid_labels = kmeans.predict(grid_points).reshape(X.shape)

    # Transition probability proxy
    transition_field = 1.0 / (Z + 1e-6)
    transition_field = (transition_field - transition_field.min()) / (
        transition_field.max() - transition_field.min() + 1e-8
    )

    # Gate candidates:
    # low density + low coherence + basin switching
    label_change = np.zeros_like(labels, dtype=bool)
    label_change[1:] = labels[1:] != labels[:-1]

    low_density = rho_t < np.percentile(rho_t, 25)
    low_coherence = coherence < np.percentile(coherence, 25)

    gate_mask = (low_density & low_coherence) | label_change
    gate_indices = np.where(gate_mask)[0]
    gate_indices = gate_indices[::120]

    # Transition matrix
    transition_matrix = np.zeros((n_basins, n_basins))

    for a, b in zip(labels[:-1], labels[1:]):
        transition_matrix[a, b] += 1

    row_sums = transition_matrix.sum(axis=1, keepdims=True) + 1e-8
    transition_matrix = transition_matrix / row_sums

    # Navigation path proxy:
    # observed path segment crossing multiple regime regions
    path_start = int(len(xs) * 0.25)
    path_end = int(len(xs) * 0.48)

    return {
        "xs": xs,
        "ys": ys,
        "X": X,
        "Y": Y,
        "Z": Z,
        "Fx": Fx,
        "Fy": Fy,
        "coherence": coherence,
        "labels": labels,
        "centers": centers,
        "grid_labels": grid_labels,
        "transition_field": transition_field,
        "gate_x": xs[gate_indices],
        "gate_y": ys[gate_indices],
        "path_x": xs[path_start:path_end],
        "path_y": ys[path_start:path_end],
        "transition_matrix": transition_matrix,
        "extent": [xmin, xmax, ymin, ymax],
    }


# ============================================================
# 3. SIMULATE SYSTEMS
# ============================================================

lorenz_x, lorenz_y, lorenz_z = simulate_system(
    lorenz_step,
    initial_state=(0.1, 0.0, 0.0),
    dt=0.01,
    steps=17000,
    burn=1200,
)

halv_x, halv_y, halv_z = simulate_system(
    halvorsen_step,
    initial_state=(0.1, 0.0, 0.0),
    dt=0.005,
    steps=22000,
    burn=2000,
)

lorenz_struct = extract_nexah_structure(lorenz_x, lorenz_y, n_grid=250, n_basins=3)
halv_struct = extract_nexah_structure(halv_x, halv_y, n_grid=250, n_basins=3)


# ============================================================
# 4. PLOT HELPERS
# ============================================================

def plot_system_row(axes, data, title):
    xs = data["xs"]
    ys = data["ys"]
    X = data["X"]
    Y = data["Y"]
    Z = data["Z"]
    Fx = data["Fx"]
    Fy = data["Fy"]
    labels = data["labels"]
    centers = data["centers"]
    grid_labels = data["grid_labels"]
    transition_field = data["transition_field"]
    coherence = data["coherence"]
    extent = data["extent"]

    # Panel 1 — Raw dynamics
    axes[0].plot(xs, ys, lw=0.35, alpha=0.75)
    axes[0].set_title(f"{title}\nRaw Dynamics")
    axes[0].set_xticks([])
    axes[0].set_yticks([])

    # Panel 2 — Density + flow
    axes[1].imshow(np.rot90(Z), extent=extent, aspect="auto")
    axes[1].quiver(
        X[::18, ::18],
        Y[::18, ::18],
        Fx[::18, ::18],
        Fy[::18, ::18],
        scale=35,
        alpha=0.55,
        width=0.002,
    )
    axes[1].set_title("Field\nDensity + Flow")
    axes[1].set_xticks([])
    axes[1].set_yticks([])

    # Panel 3 — Basins + gates
    axes[2].imshow(
        np.rot90(grid_labels),
        extent=extent,
        aspect="auto",
        alpha=0.35,
    )
    axes[2].contour(X, Y, Z, levels=8, linewidths=0.6, alpha=0.7)
    axes[2].scatter(
        centers[:, 0],
        centers[:, 1],
        s=80,
        marker="x",
        linewidths=2,
        label="Basin centers",
    )
    axes[2].scatter(
        data["gate_x"],
        data["gate_y"],
        s=12,
        c="black",
        alpha=0.8,
        label="Gate candidates",
    )
    axes[2].set_title("Regime Geometry\nBasins + Gates")
    axes[2].set_xticks([])
    axes[2].set_yticks([])
    axes[2].legend(fontsize=7, loc="upper right")

    # Panel 4 — Navigation structure
    axes[3].imshow(np.rot90(transition_field), extent=extent, aspect="auto", alpha=0.8)
    axes[3].scatter(xs, ys, c=coherence, s=0.8, cmap="coolwarm", alpha=0.55)
    axes[3].plot(
        data["path_x"],
        data["path_y"],
        color="black",
        lw=2.0,
        label="Observed path",
    )
    axes[3].scatter(
        data["gate_x"],
        data["gate_y"],
        s=14,
        c="black",
        alpha=0.8,
    )
    axes[3].set_title("Transition Field\nCoherence + Path")
    axes[3].set_xticks([])
    axes[3].set_yticks([])
    axes[3].legend(fontsize=7, loc="upper right")


# ============================================================
# 5. CREATE FIGURE
# ============================================================

fig, axes = plt.subplots(2, 4, figsize=(22, 10))

plot_system_row(axes[0], lorenz_struct, "Lorenz")
plot_system_row(axes[1], halv_struct, "Halvorsen")

fig.suptitle(
    "NEXAH — Cross-System Structure Extraction\n"
    "Dynamics → Field → Basins/Gates → Navigable Transition Structure",
    fontsize=16,
)

plt.tight_layout(rect=[0, 0, 1, 0.93])


# ============================================================
# 6. SAVE
# ============================================================

out = "NEXAH_DEMONSTRATOR/visuals/nexah_hero_cross_system_structure_v4.png"

plt.savefig(
    out,
    dpi=300,
    bbox_inches="tight",
)

print(f"Saved visual to: {out}")

plt.show()
