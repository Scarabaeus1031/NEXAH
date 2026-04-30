# loop_detection_mod7.py

import numpy as np
from collections import Counter, defaultdict
from sympy import primerange
import matplotlib.pyplot as plt

# -------------------------
# CONFIG
# -------------------------
N = 20000
MOD = 7
MAX_LOOP_LEN = 6       # check loop lengths 2..6
TOP_K = 15             # how many top loops to print per length
MIN_COUNT = 3          # only keep loops seen at least this often

# -------------------------
# PRIME SEQUENCE
# -------------------------
primes = np.array(list(primerange(3, N)))
seq = [int(p % MOD) for p in primes]

# -------------------------
# HELPERS
# -------------------------
def canonical_cycle(cycle):
    """
    Put a cycle into a canonical form so rotations count as the same loop.
    Example:
        (1,3,5) == (3,5,1) == (5,1,3)
    We choose the lexicographically smallest rotation.
    """
    cycle = tuple(cycle)
    rotations = [cycle[i:] + cycle[:i] for i in range(len(cycle))]
    return min(rotations)


def extract_loops_from_window(window, loop_len):
    """
    Detect repeated exact loop patterns in consecutive windows.
    A loop is counted if the first and last state match after wrapping:
        a,b,c  ~ loop candidate
    Here we use the transition cycle:
        (a,b,c) means a->b->c->a
    """
    loops = []

    if len(window) < loop_len:
        return loops

    for i in range(len(window) - loop_len + 1):
        chunk = tuple(window[i:i + loop_len])

        # reject trivial constant chunks
        if len(set(chunk)) < 2:
            continue

        loops.append(canonical_cycle(chunk))

    return loops


def transition_matrix(seq, mod):
    M = np.zeros((mod, mod), dtype=int)
    for i in range(len(seq) - 1):
        M[seq[i], seq[i + 1]] += 1
    return M


def loop_transition_score(loop, M):
    """
    Score a loop by summing transition counts along the cycle.
    Example for (1,3,5): score = M[1,3] + M[3,5] + M[5,1]
    """
    total = 0
    L = len(loop)
    for i in range(L):
        a = loop[i]
        b = loop[(i + 1) % L]
        total += M[a, b]
    return total


# -------------------------
# GLOBAL TRANSITION MATRIX
# -------------------------
M = transition_matrix(seq, MOD)

# -------------------------
# DETECT LOOPS
# -------------------------
loop_results = {}
all_loops_by_length = defaultdict(list)

for loop_len in range(2, MAX_LOOP_LEN + 1):
    loops = extract_loops_from_window(seq, loop_len)
    counts = Counter(loops)

    # keep only loops seen often enough
    filtered = []
    for loop, count in counts.items():
        if count >= MIN_COUNT:
            score = loop_transition_score(loop, M)
            filtered.append((loop, count, score))

    # sort by occurrence, then by score
    filtered.sort(key=lambda x: (x[1], x[2]), reverse=True)

    loop_results[loop_len] = filtered
    all_loops_by_length[loop_len] = filtered

# -------------------------
# PRINT RESULTS
# -------------------------
print("=" * 100)
print("LOOP DETECTION IN PRIME MOD-7 FLOW")
print("=" * 100)

for loop_len in range(2, MAX_LOOP_LEN + 1):
    print(f"\n--- Loop length {loop_len} ---")
    results = loop_results[loop_len][:TOP_K]

    if not results:
        print("No loops found.")
        continue

    for loop, count, score in results:
        loop_str = " → ".join(map(str, loop)) + f" → {loop[0]}"
        print(f"{loop_str:<30} | count={count:<5} | transition_score={score}")

# -------------------------
# PLOT 1: top loop counts by length
# -------------------------
lengths = []
top_counts = []

for loop_len in range(2, MAX_LOOP_LEN + 1):
    results = loop_results[loop_len]
    if results:
        lengths.append(loop_len)
        top_counts.append(results[0][1])

plt.figure(figsize=(8, 5))
plt.bar(lengths, top_counts)
plt.xlabel("Loop length")
plt.ylabel("Top loop count")
plt.title("Most Frequent Loop by Length (mod 7)")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()

# -------------------------
# PLOT 2: top loops of a chosen length
# -------------------------
CHOSEN_LEN = 3
chosen = loop_results.get(CHOSEN_LEN, [])[:TOP_K]

if chosen:
    labels = ["-".join(map(str, loop)) for loop, _, _ in chosen]
    counts = [count for _, count, _ in chosen]

    plt.figure(figsize=(10, 5))
    plt.bar(range(len(labels)), counts)
    plt.xticks(range(len(labels)), labels, rotation=45, ha="right")
    plt.ylabel("Count")
    plt.title(f"Top {CHOSEN_LEN}-Loops in Prime mod-7 Flow")
    plt.tight_layout()
    plt.show()

# -------------------------
# PLOT 3: graph of strongest loop transitions
# -------------------------
try:
    import networkx as nx

    G = nx.DiGraph()

    # use top loops across all lengths
    top_global = []
    for loop_len in range(2, MAX_LOOP_LEN + 1):
        top_global.extend(loop_results[loop_len][:5])

    # add weighted edges from loops
    edge_weights = defaultdict(float)
    for loop, count, score in top_global:
        L = len(loop)
        for i in range(L):
            a = loop[i]
            b = loop[(i + 1) % L]
            edge_weights[(a, b)] += count

    for (a, b), w in edge_weights.items():
        G.add_edge(a, b, weight=w)

    pos = nx.circular_layout(G)
    weights = [G[u][v]["weight"] / 5 for u, v in G.edges()]

    plt.figure(figsize=(7, 7))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=1000,
        width=weights,
        arrows=True
    )
    plt.title("Loop Graph from Prime mod-7 Flow")
    plt.tight_layout()
    plt.show()

except ImportError:
    print("\nnetworkx not installed; skipping graph plot.")
    print("Install with: pip install networkx")


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
