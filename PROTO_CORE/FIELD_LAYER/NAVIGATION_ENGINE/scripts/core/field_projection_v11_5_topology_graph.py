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

    X = np.zeros((n_steps, 3))
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

def density_field(alpha, beta, bins=200):
    H, xedges, yedges = np.histogram2d(alpha, beta, bins=bins)
    H = gaussian_filter(H, sigma=2)
    return H, xedges, yedges


# =========================
# 4. NODE DETECTION (ATTRACTORS)
# =========================

def extract_nodes(H, threshold_quantile=0.995):
    thresh = np.quantile(H, threshold_quantile)
    mask = H > thresh

    coords = np.argwhere(mask)

    # cluster nodes by simple merging (distance)
    nodes = []
    for c in coords:
        if len(nodes) == 0:
            nodes.append(c)
            continue

        d = cdist([c], nodes)
        if np.min(d) > 5:
            nodes.append(c)

    return np.array(nodes)


# =========================
# 5. TRAJECTORY EXTRACTION
# =========================

def sample_trajectories(alpha, beta, num_samples=20, length=100):
    idxs = np.linspace(0, len(alpha)-length-1, num_samples).astype(int)

    trajs = []
    for i in idxs:
        traj = np.stack([alpha[i:i+length], beta[i:i+length]], axis=1)
        trajs.append(traj)

    return trajs


# =========================
# 6. GRAPH CONSTRUCTION
# =========================

def assign_node(point, nodes):
    if len(nodes) == 0:
        return None

    d = cdist([point], nodes)
    return np.argmin(d)


def build_graph(trajs, nodes):
    edges = []

    for traj in trajs:
        start = assign_node(traj[0], nodes)
        end = assign_node(traj[-1], nodes)

        if start is not None and end is not None and start != end:
            edges.append((start, end))

    return edges


# =========================
# 7. VISUALIZATION
# =========================

def plot_topology(H, xedges, yedges, nodes, edges, trajs):
    plt.figure(figsize=(10, 8))

    plt.imshow(
        H.T,
        origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        aspect="auto"
    )

    # Nodes
    for i, n in enumerate(nodes):
        x = xedges[n[0]]
        y = yedges[n[1]]
        plt.scatter(x, y, s=200, c="yellow", edgecolor="black", zorder=5)
        plt.text(x, y, f"N{i}", color="black")

    # Edges
    for e in edges:
        n1 = nodes[e[0]]
        n2 = nodes[e[1]]

        x1, y1 = xedges[n1[0]], yedges[n1[1]]
        x2, y2 = xedges[n2[0]], yedges[n2[1]]

        plt.plot([x1, x2], [y1, y2], "w--", linewidth=2)

    # Trajectories
    for traj in trajs:
        plt.plot(traj[:, 0], traj[:, 1], color="white", alpha=0.3)

    plt.title("V11.5 Topology Graph Layer")
    plt.xlabel("α")
    plt.ylabel("β")

    path = os.path.join(OUTPUT_DIR, "v11_5_topology_graph.png")
    plt.savefig(path, dpi=150)
    plt.close()

    print(f"Saved: {path}")


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    print("Running V11.5 Topology Graph...")

    X = generate_lorenz()

    e1, e2, _ = compute_basis(X)
    alpha, beta = project(X, e1, e2)

    H, xedges, yedges = density_field(alpha, beta)

    nodes = extract_nodes(H)
    print(f"Detected nodes: {len(nodes)}")

    trajs = sample_trajectories(alpha, beta)

    edges = build_graph(trajs, nodes)
    print(f"Edges: {edges}")

    plot_topology(H, xedges, yedges, nodes, edges, trajs)
