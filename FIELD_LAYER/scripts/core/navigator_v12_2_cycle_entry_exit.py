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
# 3. DENSITY
# =========================

def density_field(alpha, beta, bins=220):
    H, xedges, yedges = np.histogram2d(alpha, beta, bins=bins)
    H = gaussian_filter(H, sigma=2)
    return H, xedges, yedges


# =========================
# 4. NODES
# =========================

def extract_nodes(H, q=0.992, min_dist=6):
    thresh = np.quantile(H, q)
    coords = np.argwhere(H > thresh)

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

    return np.array(nodes)


def grid_to_coords(nodes, xedges, yedges):
    xs = 0.5 * (xedges[:-1] + xedges[1:])
    ys = 0.5 * (yedges[:-1] + yedges[1:])
    return np.array([[xs[i], ys[j]] for i, j in nodes])


# =========================
# 5. TRAJECTORIES
# =========================

def sample_trajectories(alpha, beta, n=40, length=220):
    starts = np.linspace(len(alpha)-2500, len(alpha)-length-1, n).astype(int)

    trajs = []
    for s in starts:
        traj = np.stack([alpha[s:s+length], beta[s:s+length]], axis=1)
        trajs.append(traj)

    return trajs


# =========================
# 6. NODE ASSIGNMENT
# =========================

def assign_node(p, nodes, r=3.2):
    d = cdist([p], nodes)[0]
    i = np.argmin(d)
    return i if d[i] < r else None


def compress(seq):
    out, prev = [], None
    for s in seq:
        if s is None:
            continue
        if s != prev:
            out.append(s)
            prev = s
    return out


# =========================
# 7. ENTRY / EXIT DETECTION
# =========================

def detect_entry_exit(trajs, nodes):
    entry_points = []
    exit_points = []

    for traj in trajs:
        seq = [assign_node(p, nodes) for p in traj]
        seq = compress(seq)

        # detect transitions
        for i in range(len(seq)-1):
            a, b = seq[i], seq[i+1]
            if a != b:
                entry_points.append((b, traj[0]))  # entering b
                exit_points.append((a, traj[-1]))  # leaving a

    return entry_points, exit_points


# =========================
# 8. VISUALIZATION
# =========================

def plot(H, xedges, yedges, nodes, trajs, entry, exit):
    plt.figure(figsize=(12, 9))

    plt.imshow(
        H.T,
        origin="lower",
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
        cmap="viridis",
        aspect="auto"
    )

    # trajectories
    for t in trajs:
        plt.plot(t[:,0], t[:,1], color="white", alpha=0.1)

    # nodes
    for i, p in enumerate(nodes):
        plt.scatter(p[0], p[1], s=220, c="yellow", edgecolor="black")
        plt.text(p[0], p[1], f"N{i}", ha="center", va="center")

    # entry points
    for node_id, pos in entry:
        plt.scatter(pos[0], pos[1], c="green", s=60, alpha=0.8)

    # exit points
    for node_id, pos in exit:
        plt.scatter(pos[0], pos[1], c="red", s=60, alpha=0.8)

    plt.title("V12.2 Cycle Entry / Exit Points")
    plt.xlabel("α")
    plt.ylabel("β")

    path = os.path.join(OUTPUT_DIR, "v12_2_entry_exit.png")
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()

    print(f"Saved: {path}")


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    print("Running V12.2 Cycle Entry / Exit...")

    X = generate_lorenz()
    e1, e2, _ = compute_basis(X)

    alpha, beta = project(X, e1, e2)
    H, xedges, yedges = density_field(alpha, beta)

    nodes_grid = extract_nodes(H)
    nodes = grid_to_coords(nodes_grid, xedges, yedges)

    print(f"Nodes: {len(nodes)}")

    trajs = sample_trajectories(alpha, beta)

    entry, exit = detect_entry_exit(trajs, nodes)

    print(f"Entry points: {len(entry)}")
    print(f"Exit points: {len(exit)}")

    plot(H, xedges, yedges, nodes, trajs, entry, exit)
