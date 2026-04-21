import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# ============================================================
# SETTINGS
# ============================================================

N_PRIMES = 4000
MOD_A = 7
MOD_B = 11

MIN_LEN = 3
MAX_LEN = 10

# ============================================================
# PRIME GENERATOR
# ============================================================

def primes_upto(n):
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(np.sqrt(n)) + 1):
        if sieve[i]:
            sieve[i * i:n + 1:i] = False
    return np.where(sieve)[0]

# ============================================================
# BUILD STATES + EDGES
# ============================================================

def build_states(primes):
    x = primes % MOD_A
    y = primes % MOD_B

    # normalize to [-1,1]
    x = (x / (MOD_A - 1)) * 2 - 1
    y = (y / (MOD_B - 1)) * 2 - 1

    return np.column_stack([x, y])

def build_edges(states):
    edges = []
    for i in range(len(states) - 1):
        a = tuple(states[i])
        b = tuple(states[i + 1])
        edges.append((a, b))
    return edges

# ============================================================
# LOOP DETECTION (EDGE SPACE)
# ============================================================

def canonical_loop(seq):
    seq = tuple(seq)
    rots = [seq[i:] + seq[:i] for i in range(len(seq))]
    rev = seq[::-1]
    rev_rots = [rev[i:] + rev[:i] for i in range(len(rev))]
    return min(rots + rev_rots)

def polygon_area(points):
    x = np.array([p[0] for p in points])
    y = np.array([p[1] for p in points])
    return 0.5 * np.sum(x * np.roll(y, -1) - y * np.roll(x, -1))

def loop_charge(points, eps=1e-9):
    area = polygon_area(points)
    if area > eps:
        return +1, area
    elif area < -eps:
        return -1, area
    return 0, area

def detect_edge_loops(edges):
    loops = Counter()
    charges = {}

    n = len(edges)

    for L in range(MIN_LEN, MAX_LEN + 1):
        for i in range(n - L):

            # extract sequence of edges
            seq = edges[i:i + L]

            # continuity check
            valid = True
            for j in range(len(seq) - 1):
                if seq[j][1] != seq[j + 1][0]:
                    valid = False
                    break

            if not valid:
                continue

            # closed loop check
            if seq[-1][1] != seq[0][0]:
                continue

            # extract polygon points
            pts = [seq[k][0] for k in range(len(seq))]

            cyc = canonical_loop(pts)
            loops[(L, cyc)] += 1

            q, area = loop_charge(cyc)
            charges[(L, cyc)] = (q, area)

    return loops, charges

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 72)
    print("EDGE FLOW CIRCULATION (mod 7 x mod 11)")
    print("=" * 72)

    primes = primes_upto(N_PRIMES * 30)[:N_PRIMES]

    states = build_states(primes)
    edges = build_edges(states)

    loops, charges = detect_edge_loops(edges)

    if len(loops) == 0:
        print("\nNo loops detected.")
        return

    print("\nTop loops:\n")

    sorted_loops = sorted(loops.items(), key=lambda z: z[1], reverse=True)

    for (L, cyc), count in sorted_loops[:20]:
        q, area = charges[(L, cyc)]
        print(f"len={L} | count={count:4d} | charge={q:+d} | area={area:.6f}")

    pos = sum(count for k, count in loops.items() if charges[k][0] > 0)
    neg = sum(count for k, count in loops.items() if charges[k][0] < 0)
    zero = sum(count for k, count in loops.items() if charges[k][0] == 0)

    print("\nCharge summary:")
    print(f"Positive: {pos}")
    print(f"Negative: {neg}")
    print(f"Zero:     {zero}")

    # --------------------------------------------------------
    # Plot: dominant loop
    # --------------------------------------------------------
    best = sorted_loops[0][0]
    pts = np.array(best[1])

    plt.figure(figsize=(6, 6))
    plt.plot(*zip(*(list(pts) + [pts[0]])), marker='o')
    plt.axhline(0, linewidth=0.5)
    plt.axvline(0, linewidth=0.5)
    plt.title(f"Dominant Loop (len={best[0]})")
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.tight_layout()
    plt.show()

# ============================================================

if __name__ == "__main__":
    main()


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
