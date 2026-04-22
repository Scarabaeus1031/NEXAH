import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, maximum_filter, minimum_filter
from scipy.spatial.distance import cdist

# ============================================================
# NEXAH — V3 Field Structure Detector
# Purpose:
#   Detect attractors, source-like maxima, and candidate saddle/gate zones
#   from a scalar field / potential-like landscape and overlay them with flow.
#
# Expected inputs:
#   X, Y : meshgrid
#   Z    : scalar field (same shape as X,Y)
#   U, V : vector field (same shape)
#
# Notes:
#   - If your current V2 script already has X,Y,U,V and a scalar background,
#     replace the synthetic demo block below with your real arrays.
#   - This is a practical detector, not a perfect Morse-theory classifier.
# ============================================================


# ------------------------------------------------------------
# DEMO FIELD (replace with your real X, Y, Z, U, V)
# ------------------------------------------------------------
x = np.linspace(6, 17, 260)
y = np.linspace(22, 31, 260)
X, Y = np.meshgrid(x, y)

def gauss(X, Y, x0, y0, sx, sy, amp):
    return amp * np.exp(-(((X - x0) ** 2) / (2 * sx ** 2) + ((Y - y0) ** 2) / (2 * sy ** 2)))

# Scalar field:
# lower values -> attractor-like minima
# higher values -> source-like maxima
Z = (
    -1.8 * gauss(X, Y, 10.0, 25.0, 1.3, 1.1, 1.0)
    -2.4 * gauss(X, Y, 13.5, 26.0, 1.1, 1.0, 1.0)
    +2.2 * gauss(X, Y, 11.2, 28.6, 1.0, 1.0, 1.0)
    -0.8 * gauss(X, Y, 12.0, 24.0, 0.8, 0.9, 1.0)
)

dx = x[1] - x[0]
dy = y[1] - y[0]

# Gradient-driven flow:
dZ_dy, dZ_dx = np.gradient(Z, dy, dx)
U = -dZ_dx
V = -dZ_dy


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def merge_close_points(points_xy, values, min_dist=0.35):
    """
    Merge nearby detections by keeping the strongest candidate.
    For minima: pass values = -Z_at_point (so larger = deeper minimum)
    For maxima: pass values = +Z_at_point
    """
    if len(points_xy) == 0:
        return np.empty((0, 2)), np.array([])

    points_xy = np.asarray(points_xy, dtype=float)
    values = np.asarray(values, dtype=float)

    order = np.argsort(values)[::-1]
    pts = points_xy[order]
    vals = values[order]

    keep_pts = []
    keep_vals = []

    for i, p in enumerate(pts):
        if len(keep_pts) == 0:
            keep_pts.append(p)
            keep_vals.append(vals[i])
            continue

        d = cdist([p], np.array(keep_pts))[0]
        if np.all(d > min_dist):
            keep_pts.append(p)
            keep_vals.append(vals[i])

    return np.array(keep_pts), np.array(keep_vals)


def extract_local_extrema(Zs, X, Y, mode="min", neighborhood=9, threshold_quantile=0.2):
    """
    Find local minima or maxima from smoothed scalar field Zs.
    """
    if mode == "min":
        filt = minimum_filter(Zs, size=neighborhood)
        mask = (Zs == filt)
        thr = np.quantile(Zs, threshold_quantile)
        mask &= (Zs <= thr)
        raw_vals = Zs[mask]
        points = np.column_stack([X[mask], Y[mask]])
        scores = -raw_vals  # deeper minima = larger score
    else:
        filt = maximum_filter(Zs, size=neighborhood)
        mask = (Zs == filt)
        thr = np.quantile(Zs, 1 - threshold_quantile)
        mask &= (Zs >= thr)
        raw_vals = Zs[mask]
        points = np.column_stack([X[mask], Y[mask]])
        scores = raw_vals

    return points, raw_vals, scores


def sample_field_at_points(X, Y, A, px, py):
    """
    Bilinear-ish nearest sample for convenience.
    """
    ix = np.argmin(np.abs(X[0, :] - px))
    iy = np.argmin(np.abs(Y[:, 0] - py))
    return A[iy, ix]


# ------------------------------------------------------------
# SMOOTHING + DIAGNOSTICS
# ------------------------------------------------------------
Zs = gaussian_filter(Z, sigma=2.0)

dZs_dy, dZs_dx = np.gradient(Zs, dy, dx)
speed = np.sqrt(U**2 + V**2)

dU_dy, dU_dx = np.gradient(U, dy, dx)
dV_dy, dV_dx = np.gradient(V, dy, dx)

div = dU_dx + dV_dy
curl = dV_dx - dU_dy

# Hessian-ish terms from scalar field
dxx = np.gradient(dZs_dx, dx, axis=1)
dyy = np.gradient(dZs_dy, dy, axis=0)
dxy = np.gradient(dZs_dx, dy, axis=0)

detH = dxx * dyy - dxy**2
traceH = dxx + dyy

# Candidate "decision regions":
# low speed + negative determinant of Hessian can indicate saddle-like structure
speed_s = gaussian_filter(speed, sigma=2.0)
saddle_score = gaussian_filter((-detH), sigma=2.0) / (speed_s + 1e-6)


# ------------------------------------------------------------
# DETECT ATTRACTORS / MAXIMA
# ------------------------------------------------------------
min_pts, min_vals_raw, min_scores = extract_local_extrema(
    Zs, X, Y, mode="min", neighborhood=11, threshold_quantile=0.22
)
max_pts, max_vals_raw, max_scores = extract_local_extrema(
    Zs, X, Y, mode="max", neighborhood=11, threshold_quantile=0.22
)

min_pts, min_scores = merge_close_points(min_pts, min_scores, min_dist=0.60)
max_pts, max_scores = merge_close_points(max_pts, max_scores, min_dist=0.60)

# ------------------------------------------------------------
# DETECT CANDIDATE SADDLES / GATES
# ------------------------------------------------------------
# local maxima of saddle_score, but only where speed is relatively low
ss = gaussian_filter(saddle_score, sigma=1.5)
ss_max = maximum_filter(ss, size=13)

saddle_mask = (ss == ss_max)
saddle_mask &= (speed_s <= np.quantile(speed_s, 0.35))
saddle_mask &= (ss >= np.quantile(ss, 0.975))

saddle_pts = np.column_stack([X[saddle_mask], Y[saddle_mask]])
saddle_vals = ss[saddle_mask]

saddle_pts, saddle_vals = merge_close_points(saddle_pts, saddle_vals, min_dist=0.70)

# ------------------------------------------------------------
# OPTIONAL: choose top few detections only
# ------------------------------------------------------------
n_min_keep = min(4, len(min_pts))
n_max_keep = min(4, len(max_pts))
n_saddle_keep = min(6, len(saddle_pts))

min_pts = min_pts[:n_min_keep]
max_pts = max_pts[:n_max_keep]
saddle_pts = saddle_pts[:n_saddle_keep]

# ------------------------------------------------------------
# VISUALIZATION
# ------------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(15, 12))

# Q1 — Scalar field + attractors / maxima
ax = axs[0, 0]
cf = ax.contourf(X, Y, Zs, levels=40, cmap="viridis")
ax.streamplot(X, Y, U, V, color="white", density=1.4, linewidth=0.8)
if len(min_pts):
    ax.scatter(min_pts[:, 0], min_pts[:, 1], s=160, c="lime", edgecolors="black", linewidths=1.5, label="Attractors")
if len(max_pts):
    ax.scatter(max_pts[:, 0], max_pts[:, 1], s=160, c="red", edgecolors="black", linewidths=1.5, label="Source-like maxima")
for i, p in enumerate(min_pts):
    ax.text(p[0] + 0.12, p[1] + 0.10, f"A{i}", color="white", fontsize=10, weight="bold")
for i, p in enumerate(max_pts):
    ax.text(p[0] + 0.12, p[1] + 0.10, f"M{i}", color="white", fontsize=10, weight="bold")
ax.set_title("Q1 — Field + Detected Attractors / Maxima")
ax.set_xlabel("α")
ax.set_ylabel("β")
ax.legend(loc="upper right")
fig.colorbar(cf, ax=ax)

# Q2 — Curl / Divergence map
ax = axs[0, 1]
cf = ax.contourf(X, Y, curl, levels=40, cmap="coolwarm")
cs = ax.contour(X, Y, div, levels=10, colors="black", linewidths=0.8, alpha=0.7)
ax.clabel(cs, inline=True, fontsize=7)
if len(saddle_pts):
    ax.scatter(saddle_pts[:, 0], saddle_pts[:, 1], s=140, c="white", marker="X", edgecolors="black", linewidths=1.2, label="Gate / Saddle candidate")
for i, p in enumerate(saddle_pts):
    ax.text(p[0] + 0.10, p[1] + 0.10, f"G{i}", color="white", fontsize=10, weight="bold")
ax.set_title("Q2 — Curl / Divergence + Gate Candidates")
ax.set_xlabel("α")
ax.set_ylabel("β")
ax.legend(loc="upper right")
fig.colorbar(cf, ax=ax)

# Q3 — Saddle score / decision zones
ax = axs[1, 0]
cf = ax.contourf(X, Y, ss, levels=40, cmap="magma")
# highlight top boundary-like zones
thr = np.quantile(ss, 0.97)
boundary_mask = np.where(ss >= thr, 1.0, 0.0)
ax.contour(X, Y, boundary_mask, levels=[0.5], colors="cyan", linewidths=2.0)
if len(saddle_pts):
    ax.scatter(saddle_pts[:, 0], saddle_pts[:, 1], s=120, c="white", marker="X", edgecolors="black", linewidths=1.2)
ax.set_title("Q3 — Decision Regions / Boundary Score")
ax.set_xlabel("α")
ax.set_ylabel("β")
fig.colorbar(cf, ax=ax)

# Q4 — Readable geometry overlay
ax = axs[1, 1]
cf = ax.contourf(X, Y, Zs, levels=40, cmap="cividis")
ax.streamplot(X, Y, U, V, color="white", density=1.45, linewidth=0.8)

# attractors
if len(min_pts):
    ax.scatter(min_pts[:, 0], min_pts[:, 1], s=180, c="lime", edgecolors="black", linewidths=1.6)
# maxima
if len(max_pts):
    ax.scatter(max_pts[:, 0], max_pts[:, 1], s=180, c="red", edgecolors="black", linewidths=1.6)
# saddles
if len(saddle_pts):
    ax.scatter(saddle_pts[:, 0], saddle_pts[:, 1], s=160, c="white", marker="X", edgecolors="black", linewidths=1.2)

# labels
for i, p in enumerate(min_pts):
    ax.text(p[0] + 0.12, p[1] + 0.10, f"ATTRACTOR A{i}", color="white", fontsize=9, weight="bold")
for i, p in enumerate(max_pts):
    ax.text(p[0] + 0.12, p[1] + 0.10, f"SOURCE M{i}", color="white", fontsize=9, weight="bold")
for i, p in enumerate(saddle_pts):
    ax.text(p[0] + 0.12, p[1] + 0.10, f"FLOW GATE G{i}", color="white", fontsize=9, weight="bold")

ax.set_title("Q4 — NEXAH V3 Readable Structure Map")
ax.set_xlabel("α")
ax.set_ylabel("β")
fig.colorbar(cf, ax=ax)

plt.tight_layout()


# ------------------------------------------------------------
# PRINT SUMMARY
# ------------------------------------------------------------
print("\n--- NEXAH V3 STRUCTURE SUMMARY ---")
print(f"Detected attractors: {len(min_pts)}")
for i, p in enumerate(min_pts):
    print(f"  A{i}: ({p[0]:.3f}, {p[1]:.3f})")

print(f"Detected source-like maxima: {len(max_pts)}")
for i, p in enumerate(max_pts):
    print(f"  M{i}: ({p[0]:.3f}, {p[1]:.3f})")

print(f"Detected gate/saddle candidates: {len(saddle_pts)}")
for i, p in enumerate(saddle_pts):
    print(f"  G{i}: ({p[0]:.3f}, {p[1]:.3f})")
