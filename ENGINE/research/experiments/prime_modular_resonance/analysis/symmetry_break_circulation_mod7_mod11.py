import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# ============================================================
# SETTINGS
# ============================================================

N_PRIMES = 3000
MOD_A = 7
MOD_B = 11
WINDOW = 3
GRID_N = 80

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
# BUILD 2D STATE TRAJECTORY
# ============================================================

def build_state_trajectory(primes, mod_a=7, mod_b=11):
    x = primes % mod_a
    y = primes % mod_b
    states = np.column_stack([x, y])
    return states

# ============================================================
# NORMALIZE FOR PLOTTING
# ============================================================

def normalize_states(states, mod_a=7, mod_b=11):
    xs = states[:, 0].astype(float)
    ys = states[:, 1].astype(float)

    # center around zero
    xs = (xs / (mod_a - 1)) * 2 - 1
    ys = (ys / (mod_b - 1)) * 2 - 1

    return xs, ys

# ============================================================
# LOOP AREA / CHARGE
# ============================================================

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

# ============================================================
# FIND LOCAL LOOPS
# ============================================================

def canonical_loop(seq):
    seq = tuple(seq)
    rots = [seq[i:] + seq[:i] for i in range(len(seq))]
    rev = seq[::-1]
    rev_rots = [rev[i:] + rev[:i] for i in range(len(rev))]
    return min(rots + rev_rots)

def detect_loops(states_xy, min_len=3, max_len=8):
    loops = Counter()
    loop_positions = {}
    charges = {}

    n = len(states_xy)

    for L in range(min_len, max_len + 1):
        for i in range(n - L):
            pts = [tuple(states_xy[j]) for j in range(i, i + L)]
            nxt = tuple(states_xy[i + L])

            if nxt == pts[0]:
                cyc = canonical_loop(pts)
                loops[(L, cyc)] += 1
                loop_positions.setdefault((L, cyc), []).append(i)

                q, area = loop_charge(cyc)
                charges[(L, cyc)] = (q, area)

    return loops, loop_positions, charges

# ============================================================
# FLUX FIELD
# ============================================================

def compute_flux_field(x, y, grid_n=80):
    xmin, xmax = -1, 1
    ymin, ymax = -1, 1

    dxs = np.diff(x)
    dys = np.diff(y)

    xs = np.linspace(xmin, xmax, grid_n)
    ys = np.linspace(ymin, ymax, grid_n)
    X, Y = np.meshgrid(xs, ys)

    U = np.zeros_like(X)
    V = np.zeros_like(Y)
    C = np.zeros_like(X)

    for i in range(len(dxs)):
        gx = int((x[i] - xmin) / (xmax - xmin) * (grid_n - 1))
        gy = int((y[i] - ymin) / (ymax - ymin) * (grid_n - 1))
        if 0 <= gx < grid_n and 0 <= gy < grid_n:
            U[gy, gx] += dxs[i]
            V[gy, gx] += dys[i]
            C[gy, gx] += 1

    mask = C > 0
    U[mask] /= C[mask]
    V[mask] /= C[mask]

    return X, Y, U, V

def compute_curl(U, V, dx, dy):
    dV_dx = np.gradient(V, axis=1) / dx
    dU_dy = np.gradient(U, axis=0) / dy
    return dV_dx - dU_dy

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 72)
    print("SYMMETRY BREAK CIRCULATION TEST (mod 7 x mod 11)")
    print("=" * 72)

    primes = primes_upto(N_PRIMES * 30)[:N_PRIMES]
    states = build_state_trajectory(primes, MOD_A, MOD_B)
    x, y = normalize_states(states, MOD_A, MOD_B)

    states_xy = np.column_stack([x, y])

    loops, loop_positions, charges = detect_loops(states_xy, min_len=3, max_len=8)

    print("\nTop loops:")
    for (L, cyc), count in sorted(loops.items(), key=lambda z: z[1], reverse=True)[:15]:
        q, area = charges[(L, cyc)]
        print(f"len={L} | count={count:4d} | charge={q:+d} | area={area:.6f}")

    pos_count = sum(count for key, count in loops.items() if charges[key][0] > 0)
    neg_count = sum(count for key, count in loops.items() if charges[key][0] < 0)
    zero_count = sum(count for key, count in loops.items() if charges[key][0] == 0)

    print("\nCharge summary:")
    print(f"Positive: {pos_count}")
    print(f"Negative: {neg_count}")
    print(f"Zero:     {zero_count}")

    # --------------------------------------------------------
    # Plot 1: trajectory in true 2D modular space
    # --------------------------------------------------------
    plt.figure(figsize=(8, 8))
    plt.plot(x[:1200], y[:1200], alpha=0.4, linewidth=0.8)
    plt.scatter(x[:1200], y[:1200], s=5)
    plt.axhline(0, linewidth=0.5)
    plt.axvline(0, linewidth=0.5)
    plt.title("Prime Trajectory in mod-7 x mod-11 Space")
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Plot 2: flux field
    # --------------------------------------------------------
    X, Y, U, V = compute_flux_field(x, y, grid_n=GRID_N)

    plt.figure(figsize=(8, 8))
    plt.streamplot(X, Y, U, V, density=1.1, linewidth=1)
    plt.axhline(0, linewidth=0.5)
    plt.axvline(0, linewidth=0.5)
    plt.title("Flux Field in mod-7 x mod-11 Space")
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Plot 3: curl
    # --------------------------------------------------------
    dx = (X.max() - X.min()) / X.shape[1]
    dy = (Y.max() - Y.min()) / Y.shape[0]
    curl = compute_curl(U, V, dx, dy)

    plt.figure(figsize=(8, 8))
    plt.imshow(
        curl,
        origin="lower",
        extent=[X.min(), X.max(), Y.min(), Y.max()],
        aspect="equal"
    )
    plt.colorbar(label="curl")
    plt.axhline(0, linewidth=0.5)
    plt.axvline(0, linewidth=0.5)
    plt.title("Circulation Field (mod-7 x mod-11)")
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Plot 4: charge balance
    # --------------------------------------------------------
    plt.figure(figsize=(6, 4))
    plt.bar(["positive", "negative", "zero"], [pos_count, neg_count, zero_count])
    plt.title("Topological Charge Balance")
    plt.ylabel("loop count")
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
