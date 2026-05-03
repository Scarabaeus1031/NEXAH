import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# =========================
# PARAMETERS
# =========================
MODS = [7, 11, 13, 17]
N_PRIMES = 3000
MIN_WEIGHT = 0.08

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
    angles = np.array([2 * np.pi * i / mod for i in range(mod)])
    return np.column_stack((np.cos(angles), np.sin(angles)))

# =========================
# BUILD TRANSITIONS
# =========================
def build_transition_data(mod: int, primes):
    residues = [p % mod for p in primes]
    pairs = list(zip(residues[:-1], residues[1:]))

    counts = Counter(pairs)
    max_count = max(counts.values()) if counts else 1

    edges = []
    for (a, b), c in counts.items():
        w = c / max_count
        if w >= MIN_WEIGHT:
            edges.append((a, b, w))
    return edges

# =========================
# PLOT SINGLE MOD
# =========================
def plot_mod(ax, mod, primes):
    coords = embed_circle(mod)
    edges = build_transition_data(mod, primes)

    # edges
    for a, b, w in edges:
        x1, y1 = coords[a]
        x2, y2 = coords[b]
        ax.plot(
            [x1, x2],
            [y1, y2],
            linewidth=2 * w,
            alpha=0.7
        )

    # nodes
    ax.scatter(coords[:,0], coords[:,1], s=80)

    # labels
    for i, (x, y) in enumerate(coords):
        ax.text(x * 1.1, y * 1.1, str(i),
                ha='center', va='center', fontsize=9)

    ax.set_title(f"mod {mod}", fontsize=12)
    ax.set_aspect('equal')
    ax.axis('off')

# =========================
# MAIN FIGURE
# =========================
def main():
    primes = generate_primes(N_PRIMES)

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    axes = axes.flatten()

    for i, mod in enumerate(MODS):
        plot_mod(axes[i], mod, primes)

    plt.suptitle(
        "Figure 1 — Prime Modular Transition Regimes",
        fontsize=16
    )

    plt.tight_layout()
    plt.savefig("output/plots/figure_1_mod_comparison.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    main()
