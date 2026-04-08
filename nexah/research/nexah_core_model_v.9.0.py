# nexah_core_model_v.9.0.py

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# NEXAH v9.0
# Switch Layer + State Machine on Dual-Strand Grey Channel
# ------------------------------------------------------------
# Idea:
# - build a full field with blue / green / red / grey
# - identify a grey channel around an elastic axis
# - split grey into lower / upper strand
# - define a switch-layer state machine
# - track transitions between contracting and expanding regimes
# ============================================================


# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------
steps = 22000

# left / right seeds
left_center = np.array([-9.0, -8.5])
right_center = np.array([9.5, 8.0])

# global affine / elastic axis
axis_slope = 0.53
axis_intercept = -0.2

# lobe geometry
left_a = 7.5
left_b = 10.5
right_a = 8.0
right_b = 11.5

# green middle field
mid_x_min, mid_x_max = -4.5, 5.5
mid_y_min, mid_y_max = -10.0, 10.0

# grey channel parameters
grey_dist_main = 1.75
grey_dist_soft = 2.85

# dual-strand separation around axis
strand_offset = 1.45

# 3x3 and 2x2 grid anchors
grid3_x = np.array([-2.2, 0.0, 2.2])
grid3_y = np.array([-2.4, 0.0, 2.4])

grid2_x = np.array([-1.1, 1.1])
grid2_y = np.array([-1.0, 1.0])

# switch layer thresholds
switch_window_halfwidth = 1.15
coherence_window = 120

# rendering / sampling
thin_alpha = 0.25
dot_size = 2


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def ellipse_spiral(cx, cy, a, b, turns=40, points_per_turn=85,
                   radial_shrink=0.985, phase=0.0):
    xs, ys = [], []
    r = 1.0
    total = turns * points_per_turn
    for i in range(total):
        t = 2 * np.pi * i / points_per_turn + phase
        x = cx + (a * r) * np.cos(t)
        y = cy + (b * r) * np.sin(t)
        xs.append(x)
        ys.append(y)
        r *= radial_shrink
    return np.array(xs), np.array(ys)


def line_distance_and_projection(x, y, m, b):
    """
    Distance and orthogonal projection to y = m x + b
    """
    # line in implicit form: m x - y + b = 0
    denom = np.sqrt(m * m + 1.0)
    signed_dist = (m * x - y + b) / denom
    dist = np.abs(signed_dist)

    # orthogonal projection
    x_proj = (x + m * (y - b)) / (1.0 + m * m)
    y_proj = m * x_proj + b
    return dist, signed_dist, x_proj, y_proj


def axis_y(x, m, b):
    return m * x + b


def build_middle_field():
    xs, ys = [], []
    x_vals = np.linspace(mid_x_min, mid_x_max, 90)
    y_vals = np.linspace(mid_y_min, mid_y_max, 45)
    for x in x_vals:
        for y in y_vals:
            xs.append(x)
            ys.append(y)
    return np.array(xs), np.array(ys)


def classify_main_regions(x, y):
    """
    Main color partition:
    blue  = left contracting lobe
    green = middle region
    red   = right expanding lobe
    """
    if x < -4.5:
        return "blue"
    elif x > 5.5:
        return "red"
    else:
        return "green"


def build_full_field():
    # left spiral
    xb, yb = ellipse_spiral(
        left_center[0], left_center[1], left_a, left_b,
        turns=52, points_per_turn=80, radial_shrink=0.991, phase=0.2
    )

    # right spiral
    xr, yr = ellipse_spiral(
        right_center[0], right_center[1], right_a, right_b,
        turns=52, points_per_turn=82, radial_shrink=0.9915, phase=0.55
    )

    # middle cloud
    xg, yg = build_middle_field()

    # combine
    x = np.concatenate([xb, xg, xr])
    y = np.concatenate([yb, yg, yr])

    colors = np.array([classify_main_regions(xx, yy) for xx, yy in zip(x, y)], dtype=object)
    return x, y, colors


def grey_channel_mask(x, y, m, b):
    dist, signed_dist, x_proj, y_proj = line_distance_and_projection(x, y, m, b)

    # stronger channel in central bridge, softer in outer range
    central = (x > -6.5) & (x < 15.5)
    mask_main = (dist < grey_dist_main) & central
    mask_soft = (dist < grey_dist_soft) & (~central) & (x > -18.5) & (x < 20.5)

    mask = mask_main | mask_soft
    return mask, dist, signed_dist, x_proj, y_proj


def split_dual_strands(x, y, signed_dist):
    """
    Split grey channel into upper / lower strands around the axis.
    """
    upper = signed_dist < 0.0
    lower = signed_dist >= 0.0
    return upper, lower


def build_3x3_grid():
    pts = []
    for gx in grid3_x:
        for gy in grid3_y:
            pts.append((gx, gy))
    return np.array(pts)


def build_2x2_core():
    pts = []
    for gx in grid2_x:
        for gy in grid2_y:
            pts.append((gx, gy))
    return np.array(pts)


def nearest_point_indices(px, py, xs, ys):
    ids = []
    for x0, y0 in zip(px, py):
        d2 = (xs - x0) ** 2 + (ys - y0) ** 2
        ids.append(np.argmin(d2))
    return np.array(ids, dtype=int)


def compute_theta(x, y, x0=0.0, y0=0.0):
    th = np.degrees(np.arctan2(y - y0, x - x0))
    th = np.mod(th, 360.0)
    return th


def angular_velocity(theta_deg):
    th = np.radians(theta_deg)
    unwrapped = np.unwrap(th)
    dth = np.diff(unwrapped)
    dth_deg = np.degrees(dth)
    dth_deg = np.concatenate([[0.0], dth_deg])
    return dth_deg


def rolling_mean(x, w):
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    for i in range(len(x)):
        a = max(0, i - w + 1)
        out[i] = np.mean(x[a:i + 1])
    return out


def normalize_01(x):
    x = np.asarray(x, dtype=float)
    mn = np.min(x)
    mx = np.max(x)
    if mx - mn < 1e-12:
        return np.zeros_like(x)
    return (x - mn) / (mx - mn)


def switch_state_machine(score, coherence, signed_offset):
    """
    Four symbolic states on the dual grey channel.
    """
    if coherence > 0.90 and signed_offset > 0.55:
        return "upper_lock"
    elif coherence > 0.90 and signed_offset < -0.55:
        return "lower_lock"
    elif score > 0.55:
        return "switch"
    else:
        return "drift"


# ------------------------------------------------------------
# BUILD FIELD
# ------------------------------------------------------------
x, y, base_colors = build_full_field()

grey_mask, grey_dist, grey_signed_dist, x_proj, y_proj = grey_channel_mask(
    x, y, axis_slope, axis_intercept
)

full_colors = base_colors.copy()
full_colors[grey_mask] = "grey"

grey_upper_mask = grey_mask & (grey_signed_dist < 0.0)
grey_lower_mask = grey_mask & (grey_signed_dist >= 0.0)

# build synthetic upper / lower strands
x_upper = x_proj[grey_upper_mask]
y_upper = y_proj[grey_upper_mask] + strand_offset / np.sqrt(1.0 + axis_slope * axis_slope)

x_lower = x_proj[grey_lower_mask]
y_lower = y_proj[grey_lower_mask] - strand_offset / np.sqrt(1.0 + axis_slope * axis_slope)

# 3x3 and 2x2 grids
grid3 = build_3x3_grid()
grid2 = build_2x2_core()

grid3_ids = nearest_point_indices(grid3[:, 0], grid3[:, 1], x, y)
grid2_ids = nearest_point_indices(grid2[:, 0], grid2[:, 1], x, y)

# ------------------------------------------------------------
# ANGULAR ANALYSIS ON GREY CHANNEL
# ------------------------------------------------------------
xg = x[grey_mask]
yg = y[grey_mask]

theta_full = compute_theta(x, y)
theta_grey = compute_theta(xg, yg)

dtheta_grey = angular_velocity(theta_grey)

# coherence and score
coherence = 1.0 - normalize_01(np.abs(dtheta_grey))
grey_score = 1.0 - normalize_01(grey_dist[grey_mask])

coherence_smoothed = rolling_mean(coherence, coherence_window)
grey_score_smoothed = rolling_mean(grey_score, coherence_window)

# signed axis offset inside grey channel
signed_offset = grey_signed_dist[grey_mask]

# state machine along grey channel
states = np.array([
    switch_state_machine(s, c, d)
    for s, c, d in zip(grey_score_smoothed, coherence_smoothed, signed_offset)
], dtype=object)

# ------------------------------------------------------------
# PLOTTING
# ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 9))

mask_blue = full_colors == "blue"
mask_green = full_colors == "green"
mask_red = full_colors == "red"
mask_grey = full_colors == "grey"

ax.scatter(x[mask_blue], y[mask_blue], s=dot_size, c="dodgerblue", alpha=0.90, label="blue")
ax.scatter(x[mask_green], y[mask_green], s=dot_size, c="orange", alpha=0.90, label="green")
ax.scatter(x[mask_red], y[mask_red], s=dot_size, c="limegreen", alpha=0.90, label="red")
ax.scatter(x[mask_grey], y[mask_grey], s=dot_size + 1, c="black", alpha=0.85, label="grey")

# elastic axis
x_line = np.linspace(np.min(x) - 1.5, np.max(x) + 1.5, 400)
y_line = axis_y(x_line, axis_slope, axis_intercept)
ax.plot(x_line, y_line, color="#c68600", lw=2.2, label="elastic axis")

# 3x3 grid
ax.scatter(grid3[:, 0], grid3[:, 1], s=85, facecolors="none",
           edgecolors="magenta", linewidths=1.6, label="3x3 grid")

# 2x2 core
ax.scatter(grid2[:, 0], grid2[:, 1], s=105, c="#36d9e8", edgecolors="#36d9e8", label="2x2 core")

ax.set_title("NEXAH v9.0 — Switch Layer on Dual-Strand Grey Channel")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.grid(True, alpha=0.35)
ax.legend(loc="upper left")
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# DUAL STRANDS
# ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 9))

ax.scatter(x, y, s=2, c="#7fbfff", alpha=0.08)
ax.scatter(xg[grey_signed_dist[grey_mask] < 0.0], yg[grey_signed_dist[grey_mask] < 0.0],
           s=10, c="gray", alpha=0.55, label="grey upper (raw)")
ax.scatter(xg[grey_signed_dist[grey_mask] >= 0.0], yg[grey_signed_dist[grey_mask] >= 0.0],
           s=10, c="gray", alpha=0.55, label="grey lower (raw)")

ax.scatter(x_upper, y_upper, s=12, c="#35d9f2", alpha=0.95, label="upper strand")
ax.scatter(x_lower, y_lower, s=12, c="#f04df0", alpha=0.95, label="lower strand")
ax.plot(x_line, y_line, color="#c68600", lw=2.0, label="axis")

ax.set_title("Dual Grey Strands")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.grid(True, alpha=0.35)
ax.legend(loc="upper left")
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# ANGULAR DIAGNOSTICS
# ------------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

axs[0, 0].hist(theta_full, bins=150, color="#4c84b6")
for v in [52, 54, 56, 137, 184, 276]:
    axs[0, 0].axvline(v, ls="--", lw=1.5, color="#2878c8")
axs[0, 0].set_title("Angular Distribution (Full Field)")
axs[0, 0].set_xlabel("Degrees")
axs[0, 0].set_ylabel("Count")

axs[0, 1].hist(theta_grey, bins=120, color="#4c84b6")
for v in [52, 54, 56, 137, 184, 276]:
    axs[0, 1].axvline(v, ls="--", lw=1.5, color="#2878c8")
axs[0, 1].set_title("Angular Distribution (Grey Channel)")
axs[0, 1].set_xlabel("Degrees")
axs[0, 1].set_ylabel("Count")

axs[1, 0].plot(dtheta_grey, lw=1.0)
axs[1, 0].set_title("Angular Velocity dθ")
axs[1, 0].set_xlabel("time step")
axs[1, 0].set_ylabel("deg / step")

axs[1, 1].plot(theta_grey, lw=1.0)
axs[1, 1].set_title("θ over time")
axs[1, 1].set_xlabel("time step")
axs[1, 1].set_ylabel("deg")

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# PHASE COHERENCE / SWITCH SIGNAL
# ------------------------------------------------------------
signed_strand_signal = np.zeros_like(coherence_smoothed)
signed_strand_signal[grey_signed_dist[grey_mask] < 0.0] = 1.0
signed_strand_signal[grey_signed_dist[grey_mask] >= 0.0] = -1.0
dual_signal = signed_strand_signal * grey_score_smoothed * (0.5 + 0.5 * coherence_smoothed)

fig, axs = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

axs[0].plot(coherence_smoothed, color="#dd8a00", lw=1.3)
axs[0].set_title("Phase Coherence")
axs[0].set_ylabel("coherence")
axs[0].grid(True, alpha=0.30)

axs[1].plot(dual_signal, color="#a000a0", lw=1.0)
axs[1].axhline(0.0, color="k", lw=0.8, alpha=0.6)
axs[1].set_title("Dual-Strand Signal")
axs[1].set_xlabel("grey-channel index")
axs[1].set_ylabel("signed strand score")
axs[1].grid(True, alpha=0.30)

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# ELASTIC OVERLAY / SPAN-GURT
# ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 9))

ax.scatter(x, y, s=2, c="#8fd2ff", alpha=0.12)
ax.scatter(x_upper, y_upper, s=18, c="#35d9f2", alpha=0.90, label="upper strand")
ax.scatter(x_lower, y_lower, s=18, c="#f04df0", alpha=0.90, label="lower strand")

# three elastic guides
y_axis = axis_y(x_line, axis_slope, axis_intercept)
ax.plot(x_line, y_axis, color="#c68600", lw=2.0)
ax.plot(x_line, y_axis + 1.45, color="gray", lw=1.6, alpha=0.65)
ax.plot(x_line, y_axis - 1.45, color="#c68600", lw=2.0, alpha=0.95)

# emphasize right locking area
circle = plt.Circle((12.6, 7.4), 1.15, fill=False, color="gray", lw=2.2)
ax.add_patch(circle)

ax.set_title("NEXAH v9.0 — Span-Gurt / Elastic Dual Lock")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.grid(True, alpha=0.35)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# POLAR COHERENCE VIEW
# ------------------------------------------------------------
fig = plt.figure(figsize=(9, 9))
ax = plt.subplot(111, projection="polar")

th = np.radians(theta_grey)
r = 0.45 + 0.55 * coherence_smoothed
ax.scatter(th, r, c=coherence_smoothed, cmap="plasma", s=10, alpha=0.9)

ax.set_title("NEXAH Coherence — Polar", va="bottom")
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# RETURN MAP (switch section)
# ------------------------------------------------------------
u = normalize_01(theta_grey)
u_n = u[:-1]
u_np1 = u[1:]

fig, ax = plt.subplots(figsize=(11, 8))
ax.scatter(u_n, u_np1, s=18, alpha=0.55)
ax.set_title("Lorenz Return Map (switch section)")
ax.set_xlabel("u_n")
ax.set_ylabel("u_{n+1}")
ax.grid(True, alpha=0.35)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------
unique, counts = np.unique(full_colors, return_counts=True)
summary = dict(zip(unique, counts))
total = len(full_colors)

grey_upper_count = int(np.sum(grey_upper_mask))
grey_lower_count = int(np.sum(grey_lower_mask))

print("\n=== NEXAH v9.0 Summary ===")
for key in ["blue", "green", "red", "grey"]:
    val = summary.get(key, 0)
    print(f"{key}: {val} ({val / total:.3f})")

print(f"grey upper: {grey_upper_count}")
print(f"grey lower: {grey_lower_count}")
print(
    "phase coherence min/max/mean: "
    f"{coherence_smoothed.min():.4f} "
    f"{coherence_smoothed.max():.4f} "
    f"{coherence_smoothed.mean():.4f}"
)
print(
    "grey score min/max/mean: "
    f"{grey_score_smoothed.min():.4f} "
    f"{grey_score_smoothed.max():.4f} "
    f"{grey_score_smoothed.mean():.4f}"
)
print(
    "grey axis distance min/max/mean: "
    f"{grey_dist[grey_mask].min():.4f} "
    f"{grey_dist[grey_mask].max():.4f} "
    f"{grey_dist[grey_mask].mean():.4f}"
)
