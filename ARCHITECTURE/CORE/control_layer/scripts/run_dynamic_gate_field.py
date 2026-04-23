import os

import numpy as np

import matplotlib.pyplot as plt

print("⚡ NEXAH Dynamic Gate Field")

# --------------------------------------------------

# Output Path

# --------------------------------------------------

BASE_DIR = os.path.dirname(__file__)

OUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../outputs/demo"))

os.makedirs(OUT_DIR, exist_ok=True)

# --------------------------------------------------

# 1. Field Definition

# --------------------------------------------------

def flow_field(x, y):

    dx = y - x * (x**2 + y**2)

    dy = -x - y * (x**2 + y**2)

    return np.array([dx, dy])

def boundary_field(x, y):

    return np.exp(x**2 + y**2)

def target_field(x, y, tx, ty):

    return np.array([tx - x, ty - y])

def unit(v):

    n = np.linalg.norm(v)

    if n < 1e-12:

        return np.zeros_like(v)

    return v / n

# --------------------------------------------------

# 2. Gate Score

# --------------------------------------------------

def gate_score(x, y, target):

    flow = flow_field(x, y)

    tvec = target_field(x, y, target[0], target[1])

    flow_n = unit(flow)

    target_n = unit(tvec)

    alignment = np.dot(flow_n, target_n)

    b = boundary_field(x, y)

    return alignment * np.exp(-0.3 * b)

# --------------------------------------------------

# 3. Candidate Gates

# --------------------------------------------------

def find_candidate_gates(target, top_percent=99.2):

    xs = np.linspace(-2, 2, 180)

    ys = np.linspace(-2, 2, 180)

    X, Y = np.meshgrid(xs, ys)

    S = np.zeros_like(X)

    for i in range(X.shape[0]):

        for j in range(X.shape[1]):

            S[i, j] = gate_score(X[i, j], Y[i, j], target)

    threshold = np.percentile(S, top_percent)

    mask = S >= threshold

    candidates = np.column_stack([X[mask], Y[mask], S[mask]])

    return X, Y, S, candidates

def prune_gates(candidates, min_dist=0.18, max_keep=8):

    if len(candidates) == 0:

        return np.empty((0, 3))

    order = np.argsort(-candidates[:, 2])

    candidates = candidates[order]

    chosen = []

    for c in candidates:

        pt = c[:2]

        if all(np.linalg.norm(pt - np.array(ch[:2])) > min_dist for ch in chosen):

            chosen.append(c)

        if len(chosen) >= max_keep:

            break

    return np.array(chosen)

# --------------------------------------------------

# 4. Dynamic Target

# --------------------------------------------------

def moving_target(t):

    # small oscillation around a base target

    tx = 1.3 + 0.25 * np.cos(0.7 * t)

    ty = 0.35 + 0.25 * np.sin(1.1 * t)

    return np.array([tx, ty])

# --------------------------------------------------

# 5. Generate Dynamic Gate Tracks

# --------------------------------------------------

times = np.linspace(0, 12, 18)

gate_tracks = []

target_positions = []

for tt in times:

    target = moving_target(tt)

    target_positions.append(target)

    X, Y, S, raw_candidates = find_candidate_gates(target, top_percent=99.2)

    gates = prune_gates(raw_candidates, min_dist=0.16, max_keep=6)

    gate_tracks.append(gates)

target_positions = np.array(target_positions)

# --------------------------------------------------

# 6. Background Field

# --------------------------------------------------

x = np.linspace(-2, 2, 120)

y = np.linspace(-2, 2, 120)

Xf, Yf = np.meshgrid(x, y)

U = np.zeros_like(Xf)

V = np.zeros_like(Yf)

for i in range(Xf.shape[0]):

    for j in range(Xf.shape[1]):

        vec = flow_field(Xf[i, j], Yf[i, j])

        U[i, j] = vec[0]

        V[i, j] = vec[1]

# final score field for last target

last_target = target_positions[-1]

Sf = np.zeros_like(Xf)

for i in range(Xf.shape[0]):

    for j in range(Xf.shape[1]):

        Sf[i, j] = gate_score(Xf[i, j], Yf[i, j], last_target)

# --------------------------------------------------

# 7. Plot

# --------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# --- left: dynamic gates over time

ax = axes[0]

ax.contourf(Xf, Yf, Sf, levels=30, alpha=0.55)

ax.streamplot(Xf, Yf, U, V, color="black", density=1)

# plot target path

ax.plot(target_positions[:, 0], target_positions[:, 1],

        color="blue", linewidth=2, label="target path")

ax.scatter(target_positions[:, 0], target_positions[:, 1],

           color="blue", s=18)

# plot gates per time slice

for k, gates in enumerate(gate_tracks):

    if len(gates) == 0:

        continue

    alpha = 0.2 + 0.8 * (k + 1) / len(gate_tracks)

    ax.scatter(gates[:, 0], gates[:, 1],

               color="magenta", s=40, alpha=alpha)

ax.set_title("Dynamic Gate Field")

ax.set_xlabel("x")

ax.set_ylabel("y")

ax.legend()

# --- right: gate centroids over time

ax2 = axes[1]

ax2.plot(target_positions[:, 0], target_positions[:, 1],

         color="blue", linewidth=2, label="target path")

ax2.scatter(target_positions[:, 0], target_positions[:, 1],

            color="blue", s=18)

centroids = []

for gates in gate_tracks:

    if len(gates) > 0:

        centroids.append(np.mean(gates[:, :2], axis=0))

    else:

        centroids.append([np.nan, np.nan])

centroids = np.array(centroids)

ax2.plot(centroids[:, 0], centroids[:, 1],

         color="red", linewidth=2, label="gate centroid path")

ax2.scatter(centroids[:, 0], centroids[:, 1],

            color="red", s=22)

for i, c in enumerate(centroids):

    if not np.isnan(c[0]):

        ax2.text(c[0], c[1], str(i), fontsize=8)

ax2.set_title("Gate Drift vs Target Drift")

ax2.set_xlabel("x")

ax2.set_ylabel("y")

ax2.legend()

ax2.set_aspect("equal", adjustable="box")

plt.tight_layout()

out_path = os.path.join(OUT_DIR, "nexah_dynamic_gate_field.png")

plt.savefig(out_path, dpi=200)

print(f"✔ Saved → {out_path}")

print("""

🧠 Interpretation:

Magenta points = gate candidates over time

Blue path      = moving target

Red path       = gate-centroid drift

→ gates are not fixed

→ target drift reshapes entry regions

→ control must adapt to moving transition structures

""")
