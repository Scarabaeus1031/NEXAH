# threshold_impact_on_mod7_flow.py

import numpy as np
from sympy import primerange, isprime
import matplotlib.pyplot as plt

# -------------------------
# CONFIG
# -------------------------
N = 20000
WINDOW = 40          # points before / after threshold
MOD = 7

# threshold families to inspect
MAX_N_2 = 12
MAX_N_3 = 9

# -------------------------
# PRIME SEQUENCE
# -------------------------
primes = np.array(list(primerange(3, N)))
prime_mod = primes % MOD

# -------------------------
# BUILD THRESHOLD SET
# -------------------------
thresholds = []

for n in range(1, MAX_N_2 + 1):
    m = 2**n
    thresholds.append({
        "label": f"2^{n}",
        "m": m,
        "m_plus_1": m + 1,
        "type": "2n",
        "prime_jump": isprime(m + 1),
    })

for n in range(1, MAX_N_3 + 1):
    m = 3**n
    thresholds.append({
        "label": f"3^{n}",
        "m": m,
        "m_plus_1": m + 1,
        "type": "3n",
        "prime_jump": isprime(m + 1),
    })

thresholds = sorted(thresholds, key=lambda x: x["m"])

# -------------------------
# GLOBAL TRANSITION MATRIX
# -------------------------
def build_transition_matrix(seq, mod):
    matrix = np.zeros((mod, mod), dtype=float)
    for i in range(len(seq) - 1):
        matrix[seq[i], seq[i + 1]] += 1

    row_sums = matrix.sum(axis=1, keepdims=True)
    matrix = np.divide(
        matrix,
        row_sums,
        out=np.zeros_like(matrix),
        where=row_sums != 0
    )
    return matrix

global_matrix = build_transition_matrix(prime_mod, MOD)

# -------------------------
# LOCAL WINDOW EXTRACTION
# -------------------------
def get_local_window(primes, center_value, window):
    """
    Find the prime nearest to center_value and return a local index window.
    """
    idx = np.searchsorted(primes, center_value)

    if idx >= len(primes):
        idx = len(primes) - 1
    elif idx > 0:
        # choose closer of idx or idx-1
        if abs(primes[idx] - center_value) >= abs(primes[idx - 1] - center_value):
            idx = idx - 1

    start = max(0, idx - window)
    end = min(len(primes), idx + window + 1)

    return idx, start, end

# -------------------------
# LOCAL IMPACT METRICS
# -------------------------
def matrix_distance(A, B):
    return np.linalg.norm(A - B)

def dominant_edges(matrix, top_k=5):
    edges = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            edges.append((i, j, matrix[i, j]))
    edges.sort(key=lambda x: x[2], reverse=True)
    return edges[:top_k]

results = []

for th in thresholds:
    idx, start, end = get_local_window(primes, th["m"], WINDOW)
    local_seq = prime_mod[start:end]

    if len(local_seq) < 3:
        continue

    local_matrix = build_transition_matrix(local_seq, MOD)
    dist = matrix_distance(local_matrix, global_matrix)
    dom = dominant_edges(local_matrix, top_k=5)

    results.append({
        "label": th["label"],
        "m": th["m"],
        "m_plus_1": th["m_plus_1"],
        "type": th["type"],
        "prime_jump": th["prime_jump"],
        "nearest_prime": int(primes[idx]),
        "distance_to_global": dist,
        "dominant_edges": dom,
        "local_matrix": local_matrix
    })

# -------------------------
# PRINT SUMMARY
# -------------------------
print("=" * 100)
print("THRESHOLD IMPACT ON MOD-7 FLOW")
print("=" * 100)

for r in results:
    print(
        f"{r['label']:>4} | m={r['m']:<6} | m+1={r['m_plus_1']:<6} | "
        f"type={r['type']:<2} | prime_jump={str(r['prime_jump']):<5} | "
        f"nearest_prime={r['nearest_prime']:<6} | "
        f"dist_to_global={r['distance_to_global']:.4f}"
    )
    print("   top edges:", ", ".join([f"{a}->{b}:{w:.3f}" for a, b, w in r["dominant_edges"]]))

# -------------------------
# PLOT 1: distance-to-global
# -------------------------
labels = [r["label"] for r in results]
distances = [r["distance_to_global"] for r in results]
colors = ["tab:blue" if r["type"] == "2n" else "tab:orange" for r in results]
markers = ["o" if r["prime_jump"] else "x" for r in results]

plt.figure(figsize=(12, 5))
for i, r in enumerate(results):
    plt.scatter(i, r["distance_to_global"], color=colors[i], marker=markers[i], s=90)
    plt.text(i, r["distance_to_global"] + 0.01, r["label"], ha="center", fontsize=8)

plt.xticks(range(len(labels)), labels, rotation=45)
plt.ylabel("Distance to global mod-7 flow")
plt.title("Threshold Impact on mod-7 Flow")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# -------------------------
# PLOT 2: compare prime-jump vs non-prime-jump distances
# -------------------------
prime_jump_dist = [r["distance_to_global"] for r in results if r["prime_jump"]]
non_prime_jump_dist = [r["distance_to_global"] for r in results if not r["prime_jump"]]

plt.figure(figsize=(8, 5))
plt.boxplot([prime_jump_dist, non_prime_jump_dist], labels=["prime jump", "non-prime jump"])
plt.ylabel("Distance to global mod-7 flow")
plt.title("Local Flow Deviation Around Thresholds")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# -------------------------
# PLOT 3: heatmaps for strongest deviations
# -------------------------
top_results = sorted(results, key=lambda x: x["distance_to_global"], reverse=True)[:4]

fig, axes = plt.subplots(1, len(top_results), figsize=(4 * len(top_results), 4))
if len(top_results) == 1:
    axes = [axes]

for ax, r in zip(axes, top_results):
    im = ax.imshow(r["local_matrix"], cmap="viridis")
    ax.set_title(f"{r['label']}  (m+1={r['m_plus_1']})")
    ax.set_xlabel("Next state")
    ax.set_ylabel("Current state")

fig.colorbar(im, ax=axes, shrink=0.8)
plt.tight_layout()
plt.show()


# ================= AUTO SAVE HOOK =================
import os
import matplotlib.pyplot as plt

if os.environ.get("AUTO_SAVE") == "1":

    figs = list(map(plt.figure, plt.get_fignums()))

    if not figs:
        print("[WARN] No figures to save.")

    for i, fig in enumerate(figs):
        filename = __file__.split("/")[-1].replace(".py", f"_{i}.png")
        fig.savefig(f"output/plots/{filename}", dpi=150, bbox_inches="tight")

    plt.close("all")

else:
    plt.show()

# =================================================
