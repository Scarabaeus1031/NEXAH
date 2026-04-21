import numpy as np
from sympy import primerange
import matplotlib.pyplot as plt

# -------------------------
# Build Transition Matrix
# -------------------------

def compute_transition(seq, mod):
    matrix = np.zeros((mod, mod))

    for i in range(len(seq) - 1):
        matrix[seq[i], seq[i+1]] += 1

    # row normalize
    row_sums = matrix.sum(axis=1, keepdims=True)
    matrix = np.divide(matrix, row_sums, where=row_sums != 0)
    matrix[np.isnan(matrix)] = 0

    return matrix


# -------------------------
# Loop Metrics
# -------------------------

def loop_probability(P, loop):
    """Product of transition probabilities along loop"""
    prob = 1.0
    for i in range(len(loop) - 1):
        prob *= P[loop[i], loop[i+1]]
    return prob


def return_probability(P, start, steps=10):
    """Probability of returning to start after n steps"""
    Pn = np.linalg.matrix_power(P, steps)
    return Pn[start, start]


def persistence_score(P, loop):
    """
    Measures how much probability mass stays within loop nodes
    """
    nodes = set(loop)
    score = 0.0

    for i in nodes:
        for j in nodes:
            score += P[i, j]

    return score / len(nodes)


# -------------------------
# Prime Sequence
# -------------------------

mod = 7
primes = list(primerange(3, 20000))
seq = [p % mod for p in primes]

P = compute_transition(seq, mod)

# -------------------------
# Define Top Loops (from your data)
# -------------------------

loops = [
    [4, 5, 4],
    [2, 3, 2],
    [1, 2, 1],
    [5, 6, 5],
    [1, 5, 4, 1],
    [4, 6, 5, 4],
    [3, 5, 4, 3]
]

print("=" * 70)
print("LOOP STABILITY ANALYSIS (mod 7)")
print("=" * 70)

results = []

for loop in loops:
    lp = loop_probability(P, loop)
    rp = return_probability(P, loop[0], steps=len(loop))
    ps = persistence_score(P, loop)

    results.append((loop, lp, rp, ps))

    print(f"\nLoop: {loop}")
    print(f"  Loop probability:     {lp:.6f}")
    print(f"  Return probability:   {rp:.6f}")
    print(f"  Persistence score:    {ps:.6f}")

# -------------------------
# Visualization
# -------------------------

labels = [str(r[0]) for r in results]
loop_probs = [r[1] for r in results]
return_probs = [r[2] for r in results]
persist_scores = [r[3] for r in results]

x = np.arange(len(labels))

plt.figure(figsize=(12,6))

plt.plot(x, loop_probs, marker='o', label="Loop probability")
plt.plot(x, return_probs, marker='o', label="Return probability")
plt.plot(x, persist_scores, marker='o', label="Persistence score")

plt.xticks(x, labels, rotation=45)
plt.title("Loop Stability Metrics (mod 7)")
plt.ylabel("Score")
plt.legend()
plt.grid()

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
