import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import os

# =========================
# PARAMETERS
# =========================
MOD = 7
N_PRIMES = 3000
MIN_WEIGHT = 0.08   # show only stronger transitions
NODE_SIZE = 120
FIGSIZE = (7, 7)

# =========================
# PRIME GENERATOR
# =========================
def generate_primes(n: int):
    primes = []
    num = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > num:
                break
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        num += 1
    return primes

# =========================
# EMBEDDING
# =========================
def embed_circle(mod: int):
    angles = [2 * np.pi * i / mod for i in range(mod)]
    return np.array([[np.cos(a), np.sin(a)] for a in angles])

# =========================
# BUILD TRANSITIONS
# =========================
def build_transition_weights(mod: int, n_primes: int):
    primes = generate_primes(n_primes)
    residues = [p % mod for p in primes]

    transitions = list(zip(residues[:-1], residues[1:]))
    counts = Counter(transitions)

    max_count = max(counts.values()) if counts else 1
    weights = {edge: c / max_count for edge, c in counts.items()}

    node_counts = Counter(residues)
    max_node = max(node_counts.values()) if node_counts else 1
    node_weights = {node: node_counts.get(node, 0) / max_node for node in range(mod)}

    return weights, node_weights

# =========================
# DRAW GRAPH
# =========================
def draw_transition_graph(mod: int, n_primes: int, min_weight: float):
    coords = embed_circle(mod)
    weights, node_weights = build_transition_weights(mod, n_primes)

    fig, ax = plt.subplots(figsize=FIGSIZE)

    # soft circle guide
    theta = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(theta), np.sin(theta), alpha=0.15, linewidth=1.5)

    # edges
    for (a, b), w in weights.items():
        if w < min_weight:
            continue

        x1, y1 = coords[a]
        x2, y2 = coords[b]

        ax.plot(
            [x1, x2],
            [y1, y2],
            linewidth=1 + 5 * w,
            alpha=0.15 + 0.75 * w
        )

    # nodes
    xs = coords[:, 0]
    ys = coords[:, 1]

    sizes = [NODE_SIZE * (0.6 + 1.8 * node_weights[i]) for i in range(mod)]
    ax.scatter(xs, ys, s=sizes, zorder=5)

    # labels
    for i, (x, y) in enumerate(coords):
        ax.text(
            x * 1.10,
            y * 1.10,
            str(i),
            ha="center",
            va="center",
            fontsize=11
        )

    ax.set_title("mod7 Transition Graph — Clean")
    ax.set_aspect("equal")
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.axis("off")

    return fig

# =========================
# MAIN
# =========================
def main():
    fig = draw_transition_graph(MOD, N_PRIMES, MIN_WEIGHT)

    os.makedirs("output/plots", exist_ok=True)
    output_path = "output/plots/mod7_transition_graph_clean.png"
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    print(f"[OK] Saved to {output_path}")

    if os.environ.get("AUTO_SAVE") == "1":
        plt.close(fig)
    else:
        plt.show()

if __name__ == "__main__":
    main()
