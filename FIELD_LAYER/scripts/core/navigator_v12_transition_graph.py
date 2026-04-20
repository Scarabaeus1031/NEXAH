import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter
from scipy.spatial.distance import cdist

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# 1. LORENZ
# =========================

def generate_lorenz(n_steps=5000, dt=0.01):
    sigma = 10.0
    rho = 28.0
    beta = 8.0 / 3.0

    X = np.zeros((n_steps, 3), dtype=float)
    x, y, z = 1.0, 1.0, 1.0

    for i in range(n_steps):
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z

        x += dx * dt
        y += dy * dt
        z += dz * dt

        X[i] = [x, y, z]

    return X


# =========================
# 2. PCA PROJECTION
# =========================

def compute_basis(X):
    pca = PCA(n_components=3)
    pca.fit(X)
    return pca.components_


def project(X, e1, e2):
    alpha = X @ e1
    beta = X @ e2
    return alpha, beta


# =========================
# 3. DENSITY FIELD
# =========================

def density_field(alpha, beta, bins=220, sigma=2.0):
    H, xedges, yedges = np.histogram2d(alpha, beta, bins=bins)
    H = gaussian_filter(H, sigma=sigma)
    return H, xedges, yedges


# =========================
# 4. NODE DETECTION
# =========================

def extract_nodes(H, threshold_quantile=0.992, min_dist=6):
    """
    Find local high-density node centers by threshold + greedy spacing.
    """
    thresh = np.quantile(H, threshold_quantile)
    coords = np.argwhere(H > thresh)

    if len(coords) == 0:
        return np.empty((0, 2), dtype=int)

    # sort by density descending
    values = np.array([H[c[0], c[1]] for c in coords])
    order = np.argsort(values)[::-1]
    coords = coords[order]

    nodes = []
    for c in coords:
        if len(nodes) == 0:
            nodes.append(c)
            continue

        d = cdist([c], np.array(nodes))
        if np.min(d) > min_dist:
            nodes.append(c)

    return np.array(nodes, dtype=int)


def grid_to_plot_coords(nodes, xedges, yedges):
    xs = 0.5 * (xedges[:-1] + xedges[1:])
    ys = 0.5 * (yedges[:-1] + yedges[1:])
    pts = np.array([[xs[i], ys[j]] for i, j in nodes], dtype=float)
    return pts


# =========================
# 5. TRAJECTORY WINDOWS
# =========================

def sample_trajectories(alpha, beta, num_samples=40, length=220):
    """
    Overlapping trajectory windows from across the later system evolution.
    """
    start_min = max(0, len(alpha) - 2500)
    start_max = len(alpha) - length - 1

    if start_max <= start_min:
        starts = np.array([0], dtype=int)
    else:
        starts = np.linspace(start_min, start_max, num_samples).astype(int)

    trajs = []
    for s in starts:
        traj = np.stack([alpha[s:s+length], beta[s:s+length]], axis=1)
        trajs.append(traj)

    return trajs, starts


# =========================
# 6. NODE ASSIGNMENT
# =========================

def assign_node(point, node_points, radius=3.2):
    """
    Assign point to nearest node if within radius, else None.
    """
    if len(node_points) == 0:
        return None

    d = cdist([point], node_points)[0]
    idx = np.argmin(d)

    if d[idx] <= radius:
        return int(idx)
    return None


def compress_sequence(seq):
    """
    Remove consecutive duplicates and Nones.
    Example: [None,1,1,1,None,2,2,3] -> [1,2,3]
    """
    out = []
    prev = None
    for s in seq:
        if s is None:
            continue
        if s != prev:
            out.append(s)
            prev = s
    return out


# =========================
# 7. GRAPH CONSTRUCTION
# =========================

def build_transition_graph(trajs, node_points, radius=3.2):
    """
    Build weighted directed edges from node visitation sequences.
    """
    edge_weights = {}
    trajectory_sequences = []

    for traj in trajs:
        seq = [assign_node(p, node_points, radius=radius) for p in traj]
        seq = compress_sequence(seq)
        trajectory_sequences.append(seq)

        for a, b in zip(seq[:-1], seq[1:]):
            if a == b:
                continue
            edge_weights[(a, b)] = edge_weights.get((a, b), 0) + 1

    return edge_weights, trajectory_sequences


# =========================
# 8. VISUALIZATION
# =========================

def plot_transition_graph(H, xedges, yedges, node_points, edge_weights, trajs):
    fig = plt.figure(figsize=(14, 10))

    ax = fig.add_subplot(111)
    ax.imshow(
        H.T,
        origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto",
        cmap="viridis"
    )

    # trajectories (light)
    for traj in trajs:
        ax.plot(traj[:, 0], traj[:, 1], color="white", alpha=0.10, linewidth=1.2)

    # edges
    max_w = max(edge_weights.values()) if len(edge_weights) > 0 else 1
    for (a, b), w in edge_weights.items():
        p1 = node_points[a]
        p2 = node_points[b]

        linewidth = 1.5 + 4.0 * (w / max_w)
        alpha = 0.35 + 0.55 * (w / max_w)

        ax.annotate(
            "",
            xy=(p2[0], p2[1]),
            xytext=(p1[0], p1[1]),
            arrowprops=dict(
                arrowstyle="->",
                color="white",
                lw=linewidth,
                alpha=alpha,
                shrinkA=14,
                shrinkB=14
            ),
            zorder=4
        )

        mx = 0.5 * (p1[0] + p2[0])
        my = 0.5 * (p1[1] + p2[1])
        ax.text(
            mx, my, str(w),
            color="white",
            fontsize=9,
            ha="center",
            va="center",
            bbox=dict(facecolor="black", alpha=0.35, edgecolor="none", pad=1.5)
        )

    # nodes
    for i, p in enumerate(node_points):
        ax.scatter(p[0], p[1], s=260, c="yellow", edgecolor="black", zorder=5)
        ax.text(
            p[0], p[1], f"N{i}",
            color="black",
            fontsize=10,
            ha="center",
            va="center",
            zorder=6
        )

    ax.set_title("V12 Transition Graph Engine")
    ax.set_xlabel("α")
    ax.set_ylabel("β")

    out = os.path.join(OUTPUT_DIR, "v12_transition_graph.png")
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")


def plot_adjacency_matrix(n_nodes, edge_weights):
    M = np.zeros((n_nodes, n_nodes), dtype=int)
    for (a, b), w in edge_weights.items():
        M[a, b] = w

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    im = ax.imshow(M, cmap="magma")

    for i in range(n_nodes):
        for j in range(n_nodes):
            if M[i, j] > 0:
                ax.text(j, i, str(M[i, j]), color="white", ha="center", va="center", fontsize=9)

    ax.set_title("V12 Transition Adjacency Matrix")
    ax.set_xlabel("to node")
    ax.set_ylabel("from node")
    fig.colorbar(im, ax=ax)

    out = os.path.join(OUTPUT_DIR, "v12_transition_matrix.png")
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")


# =========================
# 9. MAIN
# =========================

if __name__ == "__main__":
    print("Running V12 Transition Graph Engine...")

    X = generate_lorenz()

    e1, e2, _ = compute_basis(X)
    alpha, beta = project(X, e1, e2)

    H, xedges, yedges = density_field(alpha, beta, bins=220, sigma=2.0)

    nodes_grid = extract_nodes(H, threshold_quantile=0.992, min_dist=6)
    node_points = grid_to_plot_coords(nodes_grid, xedges, yedges)

    print(f"Detected nodes: {len(node_points)}")

    trajs, starts = sample_trajectories(alpha, beta, num_samples=40, length=220)

    edge_weights, sequences = build_transition_graph(
        trajs,
        node_points,
        radius=3.2
    )

    # print sequences for debugging
    nonempty = [seq for seq in sequences if len(seq) > 0]
    print(f"Non-empty node sequences: {len(nonempty)}")

    if len(edge_weights) == 0:
        print("Edges: []")
    else:
        print("Edges:")
        for (a, b), w in sorted(edge_weights.items(), key=lambda x: (-x[1], x[0][0], x[0][1])):
            print(f"  N{a} -> N{b}: {w}")

    plot_transition_graph(H, xedges, yedges, node_points, edge_weights, trajs)
    plot_adjacency_matrix(len(node_points), edge_weights)
