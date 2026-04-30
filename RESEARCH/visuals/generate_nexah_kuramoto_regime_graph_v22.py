# NEXAH v22 — Kuramoto Regime Graph
#
# Priority:
# Kuramoto → NEXAH Field → Basins → Gates → Regime Transition Graph
#
# Output:
# RESEARCH/visuals/nexah_kuramoto_regime_graph_v22.png

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from sklearn.cluster import KMeans
import networkx as nx


# ============================================================
# 1. KURAMOTO SIMULATION
# ============================================================

def simulate_kuramoto(n_agents=64, steps=4500, dt=0.04, K=2.05, seed=7):
    rng = np.random.default_rng(seed)

    theta = rng.uniform(0, 2 * np.pi, n_agents)
    omega = rng.normal(0.0, 0.65, n_agents)

    theta_history = np.zeros((steps, n_agents))
    r_history = np.zeros(steps)
    psi_history = np.zeros(steps)

    for t in range(steps):
        order = np.mean(np.exp(1j * theta))
        r = np.abs(order)
        psi = np.angle(order)

        theta_history[t] = theta
        r_history[t] = r
        psi_history[t] = psi

        theta_dot = omega + K * r * np.sin(psi - theta)
        theta = np.mod(theta + dt * theta_dot, 2 * np.pi)

    return theta_history, r_history, np.unwrap(psi_history)


# ============================================================
# 2. FIELD HELPERS
# ============================================================

def density_field(x, y, grid_n=250):
    x = np.asarray(x)
    y = np.asarray(y)

    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]

    x = x + np.random.normal(0, 1e-7, len(x))
    y = y + np.random.normal(0, 1e-7, len(y))

    kde = gaussian_kde(np.vstack([x, y]))

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()

    if xmax - xmin < 1e-8:
        xmin -= 1e-3
        xmax += 1e-3
    if ymax - ymin < 1e-8:
        ymin -= 1e-3
        ymax += 1e-3

    X, Y = np.mgrid[xmin:xmax:complex(grid_n), ymin:ymax:complex(grid_n)]
    Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)

    return X, Y, Z, [xmin, xmax, ymin, ymax], x, y


def navigation_field(Z):
    dZdx, dZdy = np.gradient(Z)
    mag = np.sqrt(dZdx**2 + dZdy**2) + 1e-9
    return dZdx / mag, dZdy / mag


def detect_gates(Z, percentile=15):
    return Z < np.percentile(Z, percentile)


def grid_to_points(mask, extent, shape, max_points=800):
    gx, gy = np.where(mask)

    gx = np.interp(gx, [0, shape[0]], [extent[0], extent[1]])
    gy = np.interp(gy, [0, shape[1]], [extent[2], extent[3]])

    if len(gx) > max_points:
        idx = np.linspace(0, len(gx) - 1, max_points).astype(int)
        gx = gx[idx]
        gy = gy[idx]

    return gx, gy


# ============================================================
# 3. REGIME GRAPH
# ============================================================

def compute_regimes(x, y, k=4):
    data = np.vstack([x, y]).T
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = km.fit_predict(data)
    centers = km.cluster_centers_
    return labels, centers, km


def transition_matrix(labels, k):
    M = np.zeros((k, k))

    for a, b in zip(labels[:-1], labels[1:]):
        M[int(a), int(b)] += 1

    row_sums = M.sum(axis=1, keepdims=True) + 1e-12
    P = M / row_sums

    return P


def make_graph(P, threshold=0.03):
    G = nx.DiGraph()

    k = P.shape[0]

    for i in range(k):
        G.add_node(i)

    for i in range(k):
        for j in range(k):
            if P[i, j] > threshold:
                G.add_edge(i, j, weight=float(P[i, j]))

    return G


def grid_regime_labels(X, Y, kmeans):
    pts = np.vstack([X.ravel(), Y.ravel()]).T
    labels = kmeans.predict(pts).reshape(X.shape)
    return labels


# ============================================================
# 4. RUN
# ============================================================

theta_hist, r_hist, psi_hist = simulate_kuramoto()

r = r_hist
dr = np.gradient(r)
dr = np.convolve(dr, np.ones(5) / 5, mode="same")

# NEXAH synchronization slice
x_slice = r
y_slice = dr

X, Y, Z, extent, x, y = density_field(x_slice, y_slice)

Fx, Fy = navigation_field(Z)

gate_mask = detect_gates(Z)
gx, gy = grid_to_points(gate_mask, extent, Z.shape)

labels, centers, kmeans = compute_regimes(x, y, k=4)
P = transition_matrix(labels, k=4)
G = make_graph(P, threshold=0.03)

grid_labels = grid_regime_labels(X, Y, kmeans)

# graph layout based on actual regime centers
pos = {i: centers[i] for i in range(len(centers))}


# ============================================================
# 5. PLOT
# ============================================================

fig, axes = plt.subplots(1, 5, figsize=(24, 5))

# ------------------------------------------------------------
# 1. Kuramoto raw
# ------------------------------------------------------------

for i in range(theta_hist.shape[1]):
    axes[0].plot(np.sin(theta_hist[:700, i]), lw=0.25, alpha=0.25)

axes[0].plot(r[:700], color="black", lw=2.2, label="r(t)")
axes[0].set_title("Kuramoto Raw\noscillators + order")
axes[0].axis("off")
axes[0].legend(fontsize=8)

# ------------------------------------------------------------
# 2. NEXAH field
# ------------------------------------------------------------

axes[1].imshow(np.rot90(Z), cmap="viridis", extent=extent, aspect="auto")
axes[1].plot(x, y, color="white", lw=1.0, alpha=0.75)

axes[1].quiver(
    X[::14, ::14],
    Y[::14, ::14],
    Fx[::14, ::14],
    Fy[::14, ::14],
    color="white",
    alpha=0.55,
    scale=35,
    width=0.002,
)

axes[1].set_title("NEXAH Field\nDensity + Flow")
axes[1].axis("off")

# ------------------------------------------------------------
# 3. Basins + gates
# ------------------------------------------------------------

axes[2].imshow(
    np.rot90(grid_labels),
    extent=extent,
    aspect="auto",
    alpha=0.45,
)

axes[2].contour(X, Y, Z, levels=8, linewidths=0.6, alpha=0.75)
axes[2].plot(x, y, color="white", lw=0.75, alpha=0.55)

axes[2].scatter(
    centers[:, 0],
    centers[:, 1],
    color="black",
    marker="x",
    s=90,
    linewidths=2,
    label="regime centers",
)

axes[2].scatter(gx, gy, s=100, c="cyan", alpha=0.13, edgecolors="none")
axes[2].scatter(gx, gy, s=18, c="yellow", alpha=0.85, edgecolors="black", linewidths=0.25)

axes[2].set_title("Regime Geometry\nBasins + Gates")
axes[2].axis("off")
axes[2].legend(fontsize=7, loc="upper right")

# ------------------------------------------------------------
# 4. Regime graph over field
# ------------------------------------------------------------

axes[3].imshow(np.rot90(Z), cmap="inferno", extent=extent, aspect="auto", alpha=0.85)
axes[3].plot(x, y, color="white", lw=0.5, alpha=0.45)

for i, c in enumerate(centers):
    axes[3].scatter(c[0], c[1], color="white", s=90, edgecolors="black", linewidths=0.8)
    axes[3].text(c[0], c[1], f"B{i}", color="black", fontsize=9, ha="center", va="center")

for i, j, data in G.edges(data=True):
    p = data["weight"]
    a = centers[i]
    b = centers[j]

    if i == j:
        continue

    axes[3].annotate(
        "",
        xy=(b[0], b[1]),
        xytext=(a[0], a[1]),
        arrowprops=dict(
            arrowstyle="->",
            lw=1.0 + 5.0 * p,
            color="cyan",
            alpha=0.8,
        ),
    )

axes[3].scatter(gx, gy, s=80, c="cyan", alpha=0.10, edgecolors="none")
axes[3].set_title("Transition Graph\nBasin → Basin")
axes[3].axis("off")

# ------------------------------------------------------------
# 5. Transition matrix
# ------------------------------------------------------------

im = axes[4].imshow(P, vmin=0, vmax=max(0.1, P.max()), cmap="magma")
axes[4].set_title("Transition Matrix\nP(Bᵢ → Bⱼ)")
axes[4].set_xlabel("to")
axes[4].set_ylabel("from")

axes[4].set_xticks(range(P.shape[0]))
axes[4].set_yticks(range(P.shape[0]))

for i in range(P.shape[0]):
    for j in range(P.shape[1]):
        axes[4].text(
            j,
            i,
            f"{P[i, j]:.2f}",
            ha="center",
            va="center",
            color="white" if P[i, j] > P.max() * 0.45 else "black",
            fontsize=8,
        )

fig.colorbar(im, ax=axes[4], fraction=0.046, pad=0.04)

# ------------------------------------------------------------
# Global title
# ------------------------------------------------------------

fig.suptitle(
    "NEXAH v22 — Kuramoto Regime Graph\n"
    "Synchronization → Field → Basins/Gates → Transition Graph",
    fontsize=16,
)

plt.tight_layout(rect=[0, 0, 1, 0.88])

out = "RESEARCH/visuals/nexah_kuramoto_regime_graph_v22.png"

plt.savefig(out, dpi=300, bbox_inches="tight")

print(f"Saved visual to: {out}")

plt.show()
