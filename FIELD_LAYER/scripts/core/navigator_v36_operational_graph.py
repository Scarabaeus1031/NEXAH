# navigator_v36_operational_graph.py

import os
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

np.random.seed(42)

# ============================================================
# 1. CLUSTERS
# ============================================================

clusters = {
    "C0": np.array([10.0, 25.0]),
    "C1": np.array([12.0, 24.0]),
    "C2": np.array([13.5, 26.0]),
    "C3": np.array([11.0, 28.5]),
}

cluster_colors = {
    "C0": "#1f77b4",
    "C1": "#ff7f0e",
    "C2": "#2ca02c",
    "C3": "#d62728",
}

cluster_order = ["C0", "C1", "C2", "C3"]

# ============================================================
# 2. FIELD
# ============================================================

def gaussian(x, y, center, depth, sigma=1.2):
    return depth * np.exp(-((x - center[0]) ** 2 + (y - center[1]) ** 2) / (2 * sigma ** 2))

def scalar_field(x, y):
    val = 0.0
    val += gaussian(x, y, clusters["C2"], 3.0)
    val += gaussian(x, y, clusters["C1"], 2.0)
    val += gaussian(x, y, clusters["C0"], 1.5)
    val += gaussian(x, y, clusters["C3"], -2.0)
    return val

def grad_scalar_field(x, y, eps=1e-3):
    dx = (scalar_field(x + eps, y) - scalar_field(x - eps, y)) / (2 * eps)
    dy = (scalar_field(x, y + eps) - scalar_field(x, y - eps)) / (2 * eps)
    return np.array([dx, dy])

def simulate_noise_stability(x, y, steps=20, noise=0.15, trials=5):
    p = np.array([x, y], dtype=float)
    success = 0

    for _ in range(trials):
        p_sim = p.copy()
        for _ in range(steps):
            v = grad_scalar_field(p_sim[0], p_sim[1])
            v = v / (np.linalg.norm(v) + 1e-9)
            p_sim += 0.2 * v
            p_sim += noise * np.random.randn(2)

        if np.linalg.norm(p_sim - clusters["C2"]) < 1.5:
            success += 1

    return success / trials

def control_cost(x, y):
    d = np.linalg.norm(np.array([x, y]) - clusters["C2"])
    barrier = np.exp(-((x - 11) ** 2 + (y - 29) ** 2) / 2.5)
    return d + 8 * barrier

# ============================================================
# 3. GRID + PHASE MAP
# ============================================================

def build_phase_map(nx=80, ny=80):
    xs = np.linspace(6, 17, nx)
    ys = np.linspace(22, 31, ny)
    X, Y = np.meshgrid(xs, ys)

    cost = np.zeros_like(X)
    robust = np.zeros_like(X)

    print("Computing V36 fields...")

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            cost[i, j] = control_cost(X[i, j], Y[i, j])
            robust[i, j] = simulate_noise_stability(X[i, j], Y[i, j])

    cost_norm = (cost - cost.min()) / (cost.max() - cost.min() + 1e-9)

    phase = np.zeros_like(X, dtype=int)

    # 0 = optimal
    # 1 = robust but expensive
    # 2 = fragile but cheap
    # 3 = bad / irrelevant
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            c = cost_norm[i, j]
            r = robust[i, j]

            if r > 0.7 and c < 0.4:
                phase[i, j] = 0
            elif r > 0.7:
                phase[i, j] = 1
            elif c < 0.4:
                phase[i, j] = 2
            else:
                phase[i, j] = 3

    return xs, ys, X, Y, cost_norm, robust, phase

# ============================================================
# 4. OPERATIONAL NODE EXTRACTION
# ============================================================

def local_minima_mask(arr):
    mask = np.ones_like(arr, dtype=bool)
    rows, cols = arr.shape
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            block = arr[i-1:i+2, j-1:j+2]
            if arr[i, j] > np.min(block):
                mask[i, j] = False
    mask[0, :] = False
    mask[-1, :] = False
    mask[:, 0] = False
    mask[:, -1] = False
    return mask

def extract_operational_nodes(xs, ys, cost_norm, robust, phase, max_nodes=12):
    # only search in operational areas: phase 0 and 1
    candidate_mask = (phase == 0) | (phase == 1)
    minima = local_minima_mask(cost_norm)
    mask = candidate_mask & minima

    pts = []
    ny, nx = cost_norm.shape
    for i in range(ny):
        for j in range(nx):
            if mask[i, j]:
                pts.append((xs[j], ys[i], cost_norm[i, j], robust[i, j]))

    # sort: prefer low cost and high robustness
    pts.sort(key=lambda p: (p[2], -p[3]))

    selected = []
    min_dist = 0.8
    for x, y, c, r in pts:
        keep = True
        for sx, sy, _, _ in selected:
            if np.hypot(x - sx, y - sy) < min_dist:
                keep = False
                break
        if keep:
            selected.append((x, y, c, r))
        if len(selected) >= max_nodes:
            break

    # always include core clusters if missing
    anchors = [
        (clusters["C0"][0], clusters["C0"][1], control_cost(*clusters["C0"]), simulate_noise_stability(*clusters["C0"])),
        (clusters["C1"][0], clusters["C1"][1], control_cost(*clusters["C1"]), simulate_noise_stability(*clusters["C1"])),
        (clusters["C2"][0], clusters["C2"][1], control_cost(*clusters["C2"]), simulate_noise_stability(*clusters["C2"])),
        (clusters["C3"][0], clusters["C3"][1], control_cost(*clusters["C3"]), simulate_noise_stability(*clusters["C3"])),
    ]

    for ax, ay, ac, ar in anchors:
        keep = True
        for sx, sy, _, _ in selected:
            if np.hypot(ax - sx, ay - sy) < 0.4:
                keep = False
                break
        if keep:
            selected.append((ax, ay, ac, ar))

    return selected

# ============================================================
# 5. GRAPH BUILDING
# ============================================================

def segment_score(p1, p2, cost_norm, robust, xs, ys, samples=18):
    x1, y1 = p1
    x2, y2 = p2

    vals_cost = []
    vals_rob = []

    for k in range(samples):
        t = k / (samples - 1)
        x = (1 - t) * x1 + t * x2
        y = (1 - t) * y1 + t * y2

        ix = np.argmin(np.abs(xs - x))
        iy = np.argmin(np.abs(ys - y))

        vals_cost.append(cost_norm[iy, ix])
        vals_rob.append(robust[iy, ix])

    mean_cost = float(np.mean(vals_cost))
    mean_rob = float(np.mean(vals_rob))
    dist = float(np.hypot(x2 - x1, y2 - y1))

    # lower is better
    score = dist * (1.0 + 1.4 * mean_cost) / (0.25 + mean_rob)
    return score, mean_cost, mean_rob, dist

def build_operational_graph(nodes, cost_norm, robust, xs, ys):
    G = nx.Graph()

    for i, (x, y, c, r) in enumerate(nodes):
        G.add_node(i, pos=(x, y), cost=c, robust=r)

    # candidate edges
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            p1 = (nodes[i][0], nodes[i][1])
            p2 = (nodes[j][0], nodes[j][1])

            score, mean_cost, mean_rob, dist = segment_score(
                p1, p2, cost_norm, robust, xs, ys
            )

            # operational acceptance rule
            if mean_rob > 0.45 and mean_cost < 0.75 and dist < 5.0:
                G.add_edge(
                    i, j,
                    weight=score,
                    mean_cost=mean_cost,
                    mean_rob=mean_rob,
                    dist=dist
                )

    return G

# ============================================================
# 6. PLOTTING
# ============================================================

def plot_v36():
    xs, ys, X, Y, cost_norm, robust, phase = build_phase_map()

    nodes = extract_operational_nodes(xs, ys, cost_norm, robust, phase, max_nodes=10)
    G = build_operational_graph(nodes, cost_norm, robust, xs, ys)

    fig, axs = plt.subplots(2, 2, figsize=(13, 11))

    # Q1 — phase map
    cmap = plt.get_cmap("Set1", 4)
    axs[0, 0].imshow(
        phase,
        extent=[xs.min(), xs.max(), ys.min(), ys.max()],
        origin="lower",
        cmap=cmap,
        alpha=0.85,
        aspect="auto"
    )
    axs[0, 0].set_title("Q1 — Operational Phase Map")

    # Q2 — extracted nodes
    axs[0, 1].contourf(X, Y, scalar_field(X, Y), levels=30)
    for i, (x, y, c, r) in enumerate(nodes):
        axs[0, 1].scatter(x, y, s=90, c="cyan", edgecolor="black")
        axs[0, 1].text(x + 0.08, y + 0.08, f"N{i}", color="white")
    axs[0, 1].set_title("Q2 — Operational Nodes")

    # Q3 — graph in field
    axs[1, 0].contourf(X, Y, scalar_field(X, Y), levels=30)
    pos = {i: (nodes[i][0], nodes[i][1]) for i in G.nodes}

    for u, v, data in G.edges(data=True):
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        axs[1, 0].plot([x1, x2], [y1, y2], color="white", lw=1.6, alpha=0.9)

    for i, (x, y, c, r) in enumerate(nodes):
        axs[1, 0].scatter(x, y, s=100, c="cyan", edgecolor="black")
        axs[1, 0].text(x + 0.08, y + 0.08, f"N{i}", color="white")

    axs[1, 0].set_title("Q3 — Operational Graph in Field")

    # Q4 — abstract graph
    ax = axs[1, 1]
    spring_pos = nx.spring_layout(G, seed=42, weight="weight")
    nx.draw_networkx_edges(G, spring_pos, ax=ax, edge_color="gray", width=1.8)
    nx.draw_networkx_nodes(G, spring_pos, ax=ax, node_color="cyan", edgecolors="black", node_size=700)
    nx.draw_networkx_labels(G, spring_pos, ax=ax, font_size=10)

    edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, spring_pos, edge_labels=edge_labels, ax=ax, font_size=8)

    ax.set_title("Q4 — Abstract Operational Graph")
    ax.axis("off")

    # cluster markers on first three
    for ax in [axs[0, 0], axs[0, 1], axs[1, 0]]:
        for c, posc in clusters.items():
            ax.scatter(posc[0], posc[1], color=cluster_colors[c], s=90, edgecolor="black")
            ax.text(posc[0] + 0.12, posc[1] + 0.12, c)

        ax.set_xlim(6, 17)
        ax.set_ylim(22, 31)
        ax.set_xlabel("α")
        ax.set_ylabel("β")

    plt.tight_layout()

    outfile = os.path.join(OUTPUT_DIR, "v36_operational_graph.png")
    plt.savefig(outfile, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved: {outfile}")
    print("\nOperational nodes:")
    for i, (x, y, c, r) in enumerate(nodes):
        print(f"  N{i}: ({x:.2f}, {y:.2f}) | cost={c:.3f} | robust={r:.3f}")

    print("\nOperational edges:")
    for u, v, d in G.edges(data=True):
        print(
            f"  N{u} -- N{v} | weight={d['weight']:.3f} | "
            f"mean_cost={d['mean_cost']:.3f} | mean_rob={d['mean_rob']:.3f}"
        )

if __name__ == "__main__":
    plot_v36()
