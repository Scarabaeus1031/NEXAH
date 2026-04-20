import os
import numpy as np
import matplotlib.pyplot as plt

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

# Known converged points from previous versions
reference_points = {
    "V26.1": np.array([13.49285164, 26.01624951]),
    "V38":   np.array([13.46106669, 26.11600472]),
}

# ============================================================
# 2. FIELD
# ============================================================

def gaussian(x, y, center, strength, sigma=1.2):
    return strength * np.exp(-((x - center[0])**2 + (y - center[1])**2) / (2 * sigma**2))

def scalar_field(x, y):
    return (
        gaussian(x, y, clusters["C0"], 1.5)
        + gaussian(x, y, clusters["C1"], 2.0)
        + gaussian(x, y, clusters["C2"], 3.0)
        - gaussian(x, y, clusters["C3"], 2.0)
    )

def grad_field(x, y, eps=1e-3):
    dx = (scalar_field(x + eps, y) - scalar_field(x - eps, y)) / (2 * eps)
    dy = (scalar_field(x, y + eps) - scalar_field(x, y - eps)) / (2 * eps)
    return np.array([dx, dy])

def rotational_field(x, y):
    p = np.array([x, y], dtype=float)
    v = np.zeros(2, dtype=float)

    r2 = p - clusters["C2"]
    d2 = np.linalg.norm(r2) + 1e-9
    v += 0.60 * np.array([r2[1], -r2[0]]) * np.exp(-(d2**2) / (2 * 1.6**2))

    r3 = p - clusters["C3"]
    d3 = np.linalg.norm(r3) + 1e-9
    v += 0.55 * np.array([-r3[1], r3[0]]) * np.exp(-(d3**2) / (2 * 1.3**2))

    return v

def combined_field(x, y):
    return grad_field(x, y) + rotational_field(x, y)

def capture_hook_field(x, y, target, hook_radius=1.6, hook_strength=1.15):
    p = np.array([x, y], dtype=float)
    r = p - target
    d = np.linalg.norm(r) + 1e-9

    inward = -r / d
    tangential = np.array([r[1], -r[0]]) / d

    gate = np.exp(-(d**2) / (2 * hook_radius**2))
    tang_weight = hook_strength * gate
    in_weight = 0.9 * hook_strength * gate * (1.2 + 0.8 * np.exp(-d))

    return tang_weight * tangential + in_weight * inward

# ============================================================
# 3. NAVIGATION / CAPTURE DYNAMICS
# ============================================================

def follow_capture(start, target, steps=260, step_size=0.06, noise=0.0):
    x = np.array(start, dtype=float)
    traj = [x.copy()]

    for _ in range(steps):
        v = combined_field(x[0], x[1])
        bias = 0.35 * (target - x)
        hook = capture_hook_field(x[0], x[1], target)

        direction = v + bias + hook
        direction = direction / (np.linalg.norm(direction) + 1e-9)

        x = x + step_size * direction + noise * np.random.randn(2)
        traj.append(x.copy())

    return np.array(traj)

# ============================================================
# 4. FIXPOINT EXTRACTION
# ============================================================

def estimate_fixpoint(num_seeds=80):
    """
    Start seeds in a box around C2 and estimate the mean final point
    after long capture dynamics.
    """
    c2 = clusters["C2"]
    finals = []

    for _ in range(num_seeds):
        seed = c2 + np.array([
            np.random.uniform(-0.9, 0.9),
            np.random.uniform(-0.9, 0.9)
        ])
        traj = follow_capture(seed, c2, steps=260, step_size=0.06, noise=0.0)
        finals.append(traj[-1])

    finals = np.array(finals)
    fixpoint = np.mean(finals, axis=0)
    spread = np.mean(np.linalg.norm(finals - fixpoint, axis=1))
    return fixpoint, finals, spread

# ============================================================
# 5. LOCAL STABILITY TEST
# ============================================================

def ring_seeds(center, radius, n=36):
    pts = []
    for k in range(n):
        theta = 2 * np.pi * k / n
        pts.append(center + radius * np.array([np.cos(theta), np.sin(theta)]))
    return np.array(pts)

def stability_fraction(center, fixpoint, radius, n=36, tol=0.16, noise=0.0):
    seeds = ring_seeds(center, radius, n=n)
    finals = []
    ok = []

    for s in seeds:
        traj = follow_capture(s, clusters["C2"], steps=260, step_size=0.06, noise=noise)
        end = traj[-1]
        finals.append(end)
        ok.append(np.linalg.norm(end - fixpoint) <= tol)

    return np.mean(ok), seeds, np.array(finals), np.array(ok)

def scan_basin_radius(center, fixpoint, radii, n=36, tol=0.16):
    fracs = []
    for r in radii:
        frac, _, _, _ = stability_fraction(center, fixpoint, r, n=n, tol=tol, noise=0.0)
        fracs.append(frac)
    return np.array(fracs)

# ============================================================
# 6. RUN ANALYSIS
# ============================================================

fixpoint, finals_cloud, spread = estimate_fixpoint(num_seeds=100)

radii = np.linspace(0.05, 1.20, 18)
fractions = scan_basin_radius(clusters["C2"], fixpoint, radii, n=40, tol=0.16)

# stability radius: largest radius with >= 90% return
stable_idx = np.where(fractions >= 0.90)[0]
if len(stable_idx) > 0:
    stable_radius = radii[stable_idx[-1]]
else:
    stable_radius = 0.0

# choose one representative radius for local map
display_radius = stable_radius if stable_radius > 0 else 0.25
frac_display, seeds_display, finals_display, ok_display = stability_fraction(
    clusters["C2"], fixpoint, display_radius, n=40, tol=0.16, noise=0.0
)

# ============================================================
# 7. BACKGROUND GRID
# ============================================================

xv = np.linspace(6, 17, 220)
yv = np.linspace(22, 31, 220)
X, Y = np.meshgrid(xv, yv)
Z = scalar_field(X, Y)

# ============================================================
# 8. PLOTTING
# ============================================================

fig, axs = plt.subplots(2, 2, figsize=(13, 11))

# Q1 — field + reference points + estimated fixpoint
im1 = axs[0, 0].contourf(X, Y, Z, levels=40, cmap="viridis")
for c, p in clusters.items():
    axs[0, 0].scatter(p[0], p[1], color=cluster_colors[c], s=130, edgecolor="black", zorder=5)
    axs[0, 0].text(p[0] + 0.08, p[1] + 0.08, c)

for label, p in reference_points.items():
    axs[0, 0].scatter(p[0], p[1], s=90, c="white", edgecolor="black", zorder=6)
    axs[0, 0].text(p[0] + 0.06, p[1] - 0.12, label, color="white")

axs[0, 0].scatter(fixpoint[0], fixpoint[1], s=140, c="yellow", edgecolor="black", zorder=7)
axs[0, 0].text(fixpoint[0] + 0.06, fixpoint[1] + 0.06, "x*", color="black")
axs[0, 0].set_title("Q1 — Estimated Fixpoint x*")
axs[0, 0].set_xlabel("α")
axs[0, 0].set_ylabel("β")
fig.colorbar(im1, ax=axs[0, 0], fraction=0.046, pad=0.04)

# Q2 — local seeds / return map
im2 = axs[0, 1].contourf(X, Y, Z, levels=40, cmap="viridis")
axs[0, 1].scatter(fixpoint[0], fixpoint[1], s=130, c="yellow", edgecolor="black", zorder=7)

for s, e, ok in zip(seeds_display, finals_display, ok_display):
    axs[0, 1].plot([s[0], e[0]], [s[1], e[1]], color="white", alpha=0.45, lw=0.8)
    axs[0, 1].scatter(s[0], s[1], s=28, c="cyan", edgecolor="black", zorder=6)
    axs[0, 1].scatter(e[0], e[1], s=22, c=("lime" if ok else "red"), edgecolor="black", zorder=7)

circle = plt.Circle((clusters["C2"][0], clusters["C2"][1]), display_radius, fill=False, color="white", lw=1.4, alpha=0.7)
axs[0, 1].add_patch(circle)

axs[0, 1].set_xlim(12.2, 14.6)
axs[0, 1].set_ylim(25.0, 27.0)
axs[0, 1].set_title(f"Q2 — Local Return Test (r={display_radius:.2f}, frac={frac_display:.2f})")
axs[0, 1].set_xlabel("α")
axs[0, 1].set_ylabel("β")
fig.colorbar(im2, ax=axs[0, 1], fraction=0.046, pad=0.04)

# Q3 — basin radius scan
axs[1, 0].plot(radii, fractions, color="cyan", lw=2.5)
axs[1, 0].axhline(0.90, color="gray", ls="--", lw=1.2)
axs[1, 0].axvline(stable_radius, color="yellow", ls="--", lw=1.4)
axs[1, 0].scatter([stable_radius], [0.90 if stable_radius > 0 else fractions[0]], c="yellow", s=70, edgecolor="black")
axs[1, 0].set_ylim(-0.02, 1.02)
axs[1, 0].set_title("Q3 — Stability Basin Radius Scan")
axs[1, 0].set_xlabel("seed radius around C2")
axs[1, 0].set_ylabel("fraction returning to x*")

# Q4 — end-point cloud
im4 = axs[1, 1].contourf(X, Y, Z, levels=40, cmap="viridis")
axs[1, 1].scatter(finals_cloud[:, 0], finals_cloud[:, 1], s=28, c="cyan", edgecolor="black", alpha=0.75)
axs[1, 1].scatter(fixpoint[0], fixpoint[1], s=140, c="yellow", edgecolor="black", zorder=7)
axs[1, 1].scatter(reference_points["V26.1"][0], reference_points["V26.1"][1], s=80, c="white", edgecolor="black")
axs[1, 1].scatter(reference_points["V38"][0], reference_points["V38"][1], s=80, c="orange", edgecolor="black")
axs[1, 1].set_xlim(12.8, 13.9)
axs[1, 1].set_ylim(25.8, 26.3)
axs[1, 1].set_title(f"Q4 — Endpoint Cloud (spread={spread:.4f})")
axs[1, 1].set_xlabel("α")
axs[1, 1].set_ylabel("β")
fig.colorbar(im4, ax=axs[1, 1], fraction=0.046, pad=0.04)

plt.tight_layout()

out_path = os.path.join(OUTPUT_DIR, "v39_fixpoint_extraction.png")
plt.savefig(out_path, dpi=180, bbox_inches="tight")
plt.close()

print("Saved:", out_path)
print(f"Estimated fixpoint x* = ({fixpoint[0]:.6f}, {fixpoint[1]:.6f})")
print(f"Endpoint cloud spread = {spread:.6f}")
print(f"Stable basin radius (>=90% return) = {stable_radius:.4f}")
print("Reference point deltas:")
for label, p in reference_points.items():
    d = np.linalg.norm(fixpoint - p)
    print(f"  {label}: distance to x* = {d:.6f}")
