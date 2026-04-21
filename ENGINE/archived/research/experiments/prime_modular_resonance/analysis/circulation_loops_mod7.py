import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from numpy.linalg import eig

# ============================================================
# SETTINGS
# ============================================================

N_PRIMES = 2000
MIN_LOOP_LEN = 3
MAX_LOOP_LEN = 8

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
# TRANSITION + SPECTRAL
# ============================================================

def build_transition_matrix(primes):
    residues = primes % 7
    T = np.zeros((7, 7), dtype=float)

    for i in range(len(residues) - 1):
        a, b = residues[i], residues[i + 1]
        T[a, b] += 1

    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1.0
    T = T / row_sums
    return T, residues

def spectral_projection(T):
    eigvals, eigvecs = eig(T)
    idx = np.argsort(-np.abs(np.imag(eigvals)))
    v1 = eigvecs[:, idx[0]]
    v2 = eigvecs[:, idx[1]]
    coords = np.vstack([np.real(v1), np.real(v2)]).T
    return coords

# ============================================================
# BASIN / NODE DETECTION
# ============================================================

def detect_nodes_from_coords(coords):
    # use the 3 active nonzero cluster centers from prior empirical structure:
    # residues projected into spectral space, then clustered by x+y ordering
    pts = coords[1:]  # skip residue 0 for clustering
    scores = pts[:, 0] + pts[:, 1]
    order = np.argsort(scores)
    groups = np.array_split(order, 3)

    centers = []
    for g in groups:
        cx = np.mean(pts[g, 0])
        cy = np.mean(pts[g, 1])
        centers.append((cx, cy))
    return centers

def assign_basin_labels(residues, coords, centers):
    labels = []
    for r in residues:
        px, py = coords[r]
        dists = [np.hypot(px - cx, py - cy) for (cx, cy) in centers]
        labels.append(int(np.argmin(dists)))
    return np.array(labels, dtype=int)

# ============================================================
# LOOP HELPERS
# ============================================================

def canonical_cycle(seq):
    seq = tuple(seq)
    rots = [seq[i:] + seq[:i] for i in range(len(seq))]
    rev = seq[::-1]
    rev_rots = [rev[i:] + rev[:i] for i in range(len(rev))]
    return min(rots + rev_rots)

def is_closed_loop(seq):
    # closed loop in basin sequence:
    # first and last implied equal by sliding window logic outside
    # require all consecutive nodes distinct enough to be meaningful
    if len(set(seq)) < 2:
        return False
    return True

def extract_loops(labels, min_len=3, max_len=8):
    loop_counter = Counter()
    loop_positions = {}

    n = len(labels)

    for L in range(min_len, max_len + 1):
        for i in range(n - L):
            seq = tuple(labels[i:i+L])
            nxt = labels[i+L]

            # closed loop if it returns to the starting basin
            if nxt == seq[0] and is_closed_loop(seq):
                cyc = canonical_cycle(seq)
                loop_counter[(L, cyc)] += 1
                loop_positions.setdefault((L, cyc), []).append(i)

    return loop_counter, loop_positions

# ============================================================
# LOOP GEOMETRY / CHARGE
# ============================================================

def polygon_area(points):
    x = np.array([p[0] for p in points])
    y = np.array([p[1] for p in points])
    return 0.5 * np.sum(x * np.roll(y, -1) - y * np.roll(x, -1))

def loop_charge(cycle, centers):
    pts = [centers[i] for i in cycle]
    area = polygon_area(pts)
    if area > 0:
        return +1
    elif area < 0:
        return -1
    return 0

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 72)
    print("CIRCULATION LOOPS (mod 7)")
    print("=" * 72)

    primes = primes_upto(N_PRIMES * 20)[:N_PRIMES]
    T, residues = build_transition_matrix(primes)
    coords = spectral_projection(T)

    centers = detect_nodes_from_coords(coords)
    labels = assign_basin_labels(residues, coords, centers)

    print("\nDetected basin centers:")
    for i, (cx, cy) in enumerate(centers):
        print(f"Q{i+1}: ({cx:.4f}, {cy:.4f})")

    loop_counter, loop_positions = extract_loops(
        labels,
        min_len=MIN_LOOP_LEN,
        max_len=MAX_LOOP_LEN
    )

    # summarize
    print("\nTop loops by length:")
    summary_by_len = {}
    for (L, cyc), count in loop_counter.items():
        summary_by_len.setdefault(L, []).append((cyc, count))

    for L in range(MIN_LOOP_LEN, MAX_LOOP_LEN + 1):
        print(f"\n--- Loop length {L} ---")
        arr = sorted(summary_by_len.get(L, []), key=lambda z: z[1], reverse=True)[:10]
        if not arr:
            print("No loops found.")
            continue
        for cyc, count in arr:
            charge = loop_charge(cyc, centers)
            print(f"{cyc} | count={count:4d} | charge={charge:+d}")

    # dominant overall
    if len(loop_counter) == 0:
        print("\nNo circulation loops detected.")
        return

    dominant_key = sorted(loop_counter.items(), key=lambda z: z[1], reverse=True)[0][0]
    dom_len, dom_cycle = dominant_key
    dom_count = loop_counter[dominant_key]
    dom_charge = loop_charge(dom_cycle, centers)

    print("\nDominant loop overall:")
    print(f"length={dom_len}, cycle={dom_cycle}, count={dom_count}, charge={dom_charge:+d}")

    # charge stats
    pos_charge = 0
    neg_charge = 0
    zero_charge = 0
    for (L, cyc), count in loop_counter.items():
        q = loop_charge(cyc, centers)
        if q > 0:
            pos_charge += count
        elif q < 0:
            neg_charge += count
        else:
            zero_charge += count

    print("\nCharge summary:")
    print(f"Positive loops: {pos_charge}")
    print(f"Negative loops: {neg_charge}")
    print(f"Zero-area loops: {zero_charge}")

    # ========================================================
    # PLOT 1: dominant loops by length
    # ========================================================

    lengths = []
    top_counts = []
    labels_plot = []

    for L in range(MIN_LOOP_LEN, MAX_LOOP_LEN + 1):
        arr = sorted(summary_by_len.get(L, []), key=lambda z: z[1], reverse=True)
        if arr:
            cyc, count = arr[0]
            lengths.append(L)
            top_counts.append(count)
            labels_plot.append(str(cyc))

    plt.figure(figsize=(10, 5))
    plt.bar(lengths, top_counts)
    plt.title("Most Frequent Circulation Loop by Length")
    plt.xlabel("Loop length")
    plt.ylabel("Top loop count")
    plt.xticks(lengths)
    plt.tight_layout()
    plt.show()

    # ========================================================
    # PLOT 2: dominant loop geometry
    # ========================================================

    plt.figure(figsize=(8, 8))

    # all residue projections
    plt.scatter(coords[:, 0], coords[:, 1], s=80, zorder=2)
    for i, (px, py) in enumerate(coords):
        plt.text(px + 0.015, py + 0.015, str(i), fontsize=11)

    # basin centers
    for i, (cx, cy) in enumerate(centers):
        plt.scatter(cx, cy, s=220, color="yellow", edgecolor="black", zorder=4)
        plt.text(cx + 0.02, cy + 0.02, f"Q{i+1}", fontsize=12, weight="bold")

    cyc = list(dom_cycle) + [dom_cycle[0]]
    xs = [centers[i][0] for i in cyc]
    ys = [centers[i][1] for i in cyc]

    plt.plot(xs, ys, color="red", linewidth=3, zorder=5)
    for i in range(len(xs) - 1):
        dx = xs[i+1] - xs[i]
        dy = ys[i+1] - ys[i]
        plt.arrow(
            xs[i], ys[i],
            0.82 * dx, 0.82 * dy,
            head_width=0.02,
            head_length=0.03,
            fc="red", ec="red",
            length_includes_head=True,
            zorder=6
        )

    plt.axhline(0, linewidth=0.5)
    plt.axvline(0, linewidth=0.5)
    plt.title(f"Dominant Circulation Loop: {dom_cycle} | charge={dom_charge:+d}")
    plt.tight_layout()
    plt.show()

    # ========================================================
    # PLOT 3: charge balance
    # ========================================================

    plt.figure(figsize=(6, 4))
    plt.bar(["positive", "negative", "zero"], [pos_charge, neg_charge, zero_charge])
    plt.title("Topological Charge Balance of Loops")
    plt.ylabel("Total loop count")
    plt.tight_layout()
    plt.show()


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
