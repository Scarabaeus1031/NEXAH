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
    thresh = np.quantile(H, threshold_quantile)
    coords = np.argwhere(H > thresh)

    if len(coords) == 0:
        return np.empty((0, 2), dtype=int)

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
    return np.array([[xs[i], ys[j]] for i, j in nodes], dtype=float)


# =========================
# 5. TRAJECTORY WINDOWS
# =========================

def sample_trajectories(alpha, beta, num_samples=40, length=220):
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
    if len(node_points) == 0:
        return None

    d = cdist([point], node_points)[0]
    idx = np.argmin(d)

    if d[idx] <= radius:
        return int(idx)
    return None


def compress_sequence(seq):
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


def build_adjacency_dict(n_nodes, edge_weights):
    adj = {i: [] for i in range(n_nodes)}
    for (a, b), w in edge_weights.items():
        adj[a].append((b, w))
    return adj


# =========================
# 8. CYCLE DETECTION
# =========================

def canonical_cycle(cycle):
    """
    Remove duplicate last element and normalize rotation.
    Example: [3,4,6,9,3] -> canonical tuple.
    """
    cyc = cycle[:-1]
    n = len(cyc)
    rotations = [tuple(cyc[i:] + cyc[:i]) for i in range(n)]
    return min(rotations)


def find_cycles(adj, max_len=8):
    found = set()

    def dfs(start, current, path, visited):
        for nxt, _ in adj[current]:
            if nxt == start and len(path) >= 2:
                cyc = canonical_cycle(path + [start])
                if len(cyc) <= max_len:
                    found.add(cyc)
            elif nxt not in visited and len(path) < max_len:
                dfs(start, nxt, path + [nxt], visited | {nxt})

    for node in adj.keys():
        dfs(node, node, [node], {node})

    return sorted(found, key=len)


def cycle_weight(cycle, edge_weights):
    """
    Sum weights along closed cycle.
    """
    total = 0
    for a, b in zip(cycle, cycle[1:] + cycle[:1]):
        total += edge_weights.get((a, b), 0)
    return total


# =========================
# 9. VISUALIZATION
# =========================

def plot_cycle_graph(H, xedges, yedges, node_points, edge_weights, cycles, top_k=3):
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111)

    ax.imshow(
        H.T,
        origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto",
        cmap="viridis"
    )

    # all edges, faint
    max_w = max(edge_weights.values()) if edge_weights else 1
    for (a, b), w in edge_weights.items():
        p1 = node_points[a]
        p2 = node_points[b]

        ax.annotate(
            "",
            xy=(p2[0], p2[1]),
            xytext=(p1[0], p1[1]),
            arrowprops=dict(
                arrowstyle="->",
                color="white",
                lw=1.0 + 2.0 * (w / max_w),
                alpha=0.20,
                shrinkA=14,
                shrinkB=14
            ),
            zorder=3
        )

    # nodes
    for i, p in enumerate(node_points):
        ax.scatter(p[0], p[1], s=260, c="yellow", edgecolor="black", zorder=5)
        ax.text(p[0], p[1], f"N{i}", color="black", fontsize=10, ha="center", va="center", zorder=6)

    # top cycles
    weighted_cycles = [(cyc, cycle_weight(list(cyc), edge_weights)) for cyc in cycles]
    weighted_cycles.sort(key=lambda x: x[1], reverse=True)

    colors = ["cyan", "orange", "magenta"]
    legend_lines = []

    for k, (cyc, w) in enumerate(weighted_cycles[:top_k]):
        color = colors[k % len(colors)]
        pts = np.array([node_points[i] for i in cyc] + [node_points[cyc[0]]])

        ax.plot(pts[:, 0], pts[:, 1], color=color, linewidth=3.2, alpha=0.95, zorder=7)
        legend_lines.append(f"{color}: cycle {list(cyc)} | weight={w}")

    text = "\n".join(legend_lines) if legend_lines else "no cycles found"
    ax.text(
        0.02, 0.98, text,
        transform=ax.transAxes,
        ha="left", va="top",
        fontsize=10,
        color="white",
        bbox=dict(facecolor="black", alpha=0.45, edgecolor="white")
    )

    ax.set_title("V12.1 Cycle Detection + Dominant Loops")
    ax.set_xlabel("α")
    ax.set_ylabel("β")

    out = os.path.join(OUTPUT_DIR, "v12_1_cycle_detection.png")
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")


def plot_cycle_weights(cycles, edge_weights):
    weighted_cycles = [(list(cyc), cycle_weight(list(cyc), edge_weights)) for cyc in cycles]
    weighted_cycles.sort(key=lambda x: x[1], reverse=True)

    labels = [str(c[0]) for c in weighted_cycles[:10]]
    weights = [c[1] for c in weighted_cycles[:10]]

    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)

    if len(weights) > 0:
        ax.bar(range(len(weights)), weights)
        ax.set_xticks(range(len(weights)))
        ax.set_xticklabels(labels, rotation=45, ha="right")
    else:
        ax.text(0.5, 0.5, "No cycles found", ha="center", va="center", transform=ax.transAxes)

    ax.set_title("V12.1 Dominant Cycle Weights")
    ax.set_ylabel("cycle weight")

    out = os.path.join(OUTPUT_DIR, "v12_1_cycle_weights.png")
    plt.savefig(out, dpi=180, bbox_inches="tight")
    plt.close()

    print(f"Saved: {out}")


# =========================
# 10. MAIN
# =========================

if __name__ == "__main__":
    print("Running V12.1 Cycle Detection...")

    X = generate_lorenz()

    e1, e2, _ = compute_basis(X)
    alpha, beta = project(X, e1, e2)

    H, xedges, yedges = density_field(alpha, beta, bins=220, sigma=2.0)

    nodes_grid = extract_nodes(H, threshold_quantile=0.992, min_dist=6)
    node_points = grid_to_plot_coords(nodes_grid, xedges, yedges)
    print(f"Detected nodes: {len(node_points)}")

    trajs, starts = sample_trajectories(alpha, beta, num_samples=40, length=220)

    edge_weights, sequences = build_transition_graph(trajs, node_points, radius=3.2)
    adj = build_adjacency_dict(len(node_points), edge_weights)

    cycles = find_cycles(adj, max_len=8)

    print(f"Detected cycles: {len(cycles)}")
    if len(cycles) > 0:
        print("Top cycles by weight:")
        weighted = [(list(c), cycle_weight(list(c), edge_weights)) for c in cycles]
        weighted.sort(key=lambda x: x[1], reverse=True)
        for cyc, w in weighted[:10]:
            print(f"  cycle={cyc} | weight={w}")
    else:
        print("No cycles found.")

    plot_cycle_graph(H, xedges, yedges, node_points, edge_weights, cycles, top_k=3)
    plot_cycle_weights(cycles, edge_weights)
