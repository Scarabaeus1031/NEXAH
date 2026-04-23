# nexah_core_model_v.8.9.py
# NEXAH v8.9 — Dual-Strand Grey Channel + Phase Feedback
#
# Idea:
# - keep the RGB field split
# - detect a grey transition channel
# - split that channel into upper / lower strands
# - add phase feedback around the channel axis
# - show dual-strand navigation structure
#
# Output:
#   1) full field with dual grey strands
#   2) strand-separated grey channel
#   3) angle / phase diagnostics
#   4) phase feedback + strand signal
#   5) dual-strand offset overlay
#
# Run:
#   python nexah/research/nexah_core_model_v.8.9.py

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PARAMETERS
# ============================================================
N = 22000
DT = 0.005

# Lorenz-style core
SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0

# projection weights
Z_SHIFT = 24.0
Y_MIX = 0.38
X_MIX = 0.16

# field split thresholds
LEFT_THRESHOLD = -4.8
RIGHT_THRESHOLD = 5.6

# grey channel extraction
GREY_DIST_MAX = 2.4
GREY_PHASE_BOOST = 0.70
GREY_STRAND_SEP = 1.15

# elastic / guiding axis
AXIS_M = 0.58
AXIS_B = -0.15

# dual-strand geometry
STRAND_CURVE_GAIN = 0.12
STRAND_PHASE_GAIN = 0.70
STRAND_OFFSET_SCALE = 1.05

# 3x3 / 2x2 anchor logic around the middle field
GRID3_X = np.array([-2.4, 0.0, 2.4])
GRID3_Y = np.array([-2.4, 0.0, 2.4])

GRID2_X = np.array([-1.0, 1.0])
GRID2_Y = np.array([-1.0, 1.0])

# phase feedback
PHASE_WINDOW = 31
PHASE_LOCK_SCALE = 0.65

# plotting
DOT_SIZE = 4
GREY_SIZE = 7
STRAND_SIZE = 10

# ============================================================
# HELPERS
# ============================================================
def smooth_1d(arr, k):
    k = max(3, int(k))
    if k % 2 == 0:
        k += 1
    kernel = np.ones(k, dtype=float)
    kernel /= kernel.sum()
    return np.convolve(arr, kernel, mode="same")


def axis_y(x):
    return AXIS_M * x + AXIS_B


def axis_distance(x, y):
    # distance from point to line y = m x + b
    return np.abs(AXIS_M * x - y + AXIS_B) / np.sqrt(AXIS_M ** 2 + 1.0)


def project_xyz_to_plane(x, y, z):
    """
    Build the familiar NEXAH field plane.
    """
    xp = x + X_MIX * z
    yp = y - Y_MIX * (z - Z_SHIFT)
    return xp, yp


def wrap_angle_deg(theta_deg):
    return np.mod(theta_deg, 360.0)


def circular_diff_deg(theta_deg):
    """
    wrapped angular velocity in degrees
    """
    rad = np.deg2rad(theta_deg)
    d = np.diff(np.unwrap(rad), prepend=rad[0])
    return np.rad2deg(d)


def moving_phase_coherence(theta_deg, window=31):
    """
    coherence in [0,1] using local circular resultant length
    """
    window = max(5, int(window))
    if window % 2 == 0:
        window += 1
    half = window // 2

    th = np.deg2rad(theta_deg)
    c = np.cos(th)
    s = np.sin(th)

    coh = np.zeros_like(theta_deg, dtype=float)
    for i in range(len(theta_deg)):
        a = max(0, i - half)
        b = min(len(theta_deg), i + half + 1)
        cc = c[a:b].mean()
        ss = s[a:b].mean()
        coh[i] = np.sqrt(cc * cc + ss * ss)
    return coh


def nearest_grid_points(xs, ys, gx, gy):
    pts = np.array([(x, y) for x in gx for y in gy], dtype=float)
    out_idx = np.empty(len(xs), dtype=int)
    out_dist = np.empty(len(xs), dtype=float)

    for i, (x, y) in enumerate(zip(xs, ys)):
        d2 = np.sum((pts - np.array([x, y])) ** 2, axis=1)
        j = int(np.argmin(d2))
        out_idx[i] = j
        out_dist[i] = np.sqrt(d2[j])
    return pts, out_idx, out_dist


# ============================================================
# SIMULATION
# ============================================================
def simulate_lorenz(n=N, dt=DT):
    x = np.empty(n, dtype=float)
    y = np.empty(n, dtype=float)
    z = np.empty(n, dtype=float)

    x[0], y[0], z[0] = 0.15, 1.0, 1.05

    for i in range(1, n):
        dx = SIGMA * (y[i - 1] - x[i - 1])
        dy = x[i - 1] * (RHO - z[i - 1]) - y[i - 1]
        dz = x[i - 1] * y[i - 1] - BETA * z[i - 1]

        x[i] = x[i - 1] + dt * dx
        y[i] = y[i - 1] + dt * dy
        z[i] = z[i - 1] + dt * dz

    return x, y, z


# ============================================================
# FIELD CLASSIFICATION
# ============================================================
def classify_rgb_field(xp, yp):
    labels = np.empty(len(xp), dtype=object)

    for i, (x, y) in enumerate(zip(xp, yp)):
        if x < LEFT_THRESHOLD:
            labels[i] = "blue"
        elif x > RIGHT_THRESHOLD:
            labels[i] = "red"
        else:
            labels[i] = "green"

    return labels


def detect_grey_channel(xp, yp, theta_deg):
    """
    Grey channel = near axis + phase-support
    """
    d_axis = axis_distance(xp, yp)

    # phase preference around the bridge:
    # favor angles near ~45° or ~225° modulo 180
    phi = wrap_angle_deg(theta_deg)
    phase_term = np.minimum(
        np.abs(phi - 45.0),
        np.minimum(np.abs(phi - 225.0), np.abs(phi - 405.0)),
    )
    phase_term = np.minimum(phase_term, 180.0 - np.minimum(phase_term, 180.0))
    phase_score = np.exp(-(phase_term ** 2) / (2.0 * (28.0 ** 2)))

    grey_score = np.exp(-(d_axis ** 2) / (2.0 * (GREY_DIST_MAX ** 2))) * (
        1.0 + GREY_PHASE_BOOST * phase_score
    )

    grey_mask = grey_score > 0.60
    return grey_mask, grey_score, d_axis, phase_score


def split_dual_grey_strands(xg, yg, theta_g, coherence_g):
    """
    Split grey channel into upper / lower strands relative to axis,
    with slight curvature and phase feedback.
    """
    y_axis = axis_y(xg)
    residual = yg - y_axis

    # local trend / curvature from smoothed residual
    res_s = smooth_1d(residual, 41)
    curv = np.gradient(np.gradient(res_s))

    # phase term
    phase_term = np.sin(np.deg2rad(theta_g)) * STRAND_PHASE_GAIN

    # coherence term: strong coherence tightens the split
    coh_term = (coherence_g - np.mean(coherence_g)) * PHASE_LOCK_SCALE

    signed_score = residual + STRAND_CURVE_GAIN * curv + phase_term - coh_term

    upper_mask = signed_score >= 0.0
    lower_mask = ~upper_mask

    # offset points for visualization
    # move along normal to the axis
    nx = -AXIS_M / np.sqrt(AXIS_M ** 2 + 1.0)
    ny = 1.0 / np.sqrt(AXIS_M ** 2 + 1.0)

    base_offset = STRAND_OFFSET_SCALE * (
        0.35 + 0.65 * (1.0 - np.clip(coherence_g, 0.0, 1.0))
    )

    xu = xg.copy()
    yu = yg.copy()
    xl = xg.copy()
    yl = yg.copy()

    xu[upper_mask] += nx * base_offset[upper_mask] * GREY_STRAND_SEP
    yu[upper_mask] += ny * base_offset[upper_mask] * GREY_STRAND_SEP

    xl[lower_mask] -= nx * base_offset[lower_mask] * GREY_STRAND_SEP
    yl[lower_mask] -= ny * base_offset[lower_mask] * GREY_STRAND_SEP

    return upper_mask, lower_mask, xu, yu, xl, yl, signed_score


# ============================================================
# MAIN
# ============================================================
def main():
    # -----------------------------
    # simulate
    # -----------------------------
    x, y, z = simulate_lorenz()

    # skip transient
    burn = 2000
    x = x[burn:]
    y = y[burn:]
    z = z[burn:]

    # -----------------------------
    # project
    # -----------------------------
    xp, yp = project_xyz_to_plane(x, y, z)

    # center-ish angle around the bridge
    cx = smooth_1d(xp, 51)
    cy = smooth_1d(yp, 51)
    theta = wrap_angle_deg(np.degrees(np.arctan2(yp - cy, xp - cx)))
    dtheta = circular_diff_deg(theta)
    coherence = moving_phase_coherence(theta, window=PHASE_WINDOW)

    # -----------------------------
    # classify field
    # -----------------------------
    rgb = classify_rgb_field(xp, yp)

    grey_mask, grey_score, d_axis, phase_score = detect_grey_channel(xp, yp, theta)

    # remove grey from RGB labels only visually later
    blue_mask = (rgb == "blue") & (~grey_mask)
    green_mask = (rgb == "green") & (~grey_mask)
    red_mask = (rgb == "red") & (~grey_mask)

    xg = xp[grey_mask]
    yg = yp[grey_mask]
    theta_g = theta[grey_mask]
    coh_g = coherence[grey_mask]

    # split dual strands
    upper_mask, lower_mask, xu, yu, xl, yl, strand_signal = split_dual_grey_strands(
        xg, yg, theta_g, coh_g
    )

    # grid anchors
    grid3_pts, _, _ = nearest_grid_points(np.array([0.0]), np.array([0.0]), GRID3_X, GRID3_Y)
    grid3_pts = np.array([(gx, gy) for gx in GRID3_X for gy in GRID3_Y], dtype=float)

    grid2_pts = np.array([(gx, gy) for gx in GRID2_X for gy in GRID2_Y], dtype=float)

    # -----------------------------
    # counts
    # -----------------------------
    counts = {
        "blue": int(np.sum(blue_mask)),
        "green": int(np.sum(green_mask)),
        "red": int(np.sum(red_mask)),
        "grey": int(np.sum(grey_mask)),
        "grey_upper": int(np.sum(upper_mask)),
        "grey_lower": int(np.sum(lower_mask)),
    }

    total = len(xp)

    # ============================================================
    # PLOTS
    # ============================================================

    # ------------------------------------------------------------
    # 1) Main field
    # ------------------------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(12, 9))
    ax1.scatter(xp[blue_mask], yp[blue_mask], s=DOT_SIZE, c="tab:blue", alpha=0.9, label="blue")
    ax1.scatter(xp[green_mask], yp[green_mask], s=DOT_SIZE, c="orange", alpha=0.9, label="green")
    ax1.scatter(xp[red_mask], yp[red_mask], s=DOT_SIZE, c="tab:green", alpha=0.9, label="red")
    ax1.scatter(xg, yg, s=GREY_SIZE, c="black", alpha=0.9, label="grey")

    # elastic axis
    xx = np.linspace(np.min(xp) - 1.0, np.max(xp) + 1.0, 300)
    yy = axis_y(xx)
    ax1.plot(xx, yy, color="#c98c00", lw=2.2, label="elastic axis")

    # 3x3 grid
    ax1.scatter(
        grid3_pts[:, 0],
        grid3_pts[:, 1],
        s=80,
        facecolors="none",
        edgecolors="magenta",
        linewidths=1.5,
        label="3x3 grid",
    )

    # 2x2 core
    ax1.scatter(
        grid2_pts[:, 0],
        grid2_pts[:, 1],
        s=110,
        c="#28d7f7",
        alpha=0.95,
        label="2x2 core",
    )

    ax1.set_title("NEXAH v8.9 — Dual-Strand Grey Channel + Phase Feedback")
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.grid(True, alpha=0.4)
    ax1.legend(loc="upper left")

    # ------------------------------------------------------------
    # 2) Grey strands
    # ------------------------------------------------------------
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    ax2.scatter(xp, yp, s=3, c="#9ec9ef", alpha=0.08)
    ax2.scatter(xg[upper_mask], yg[upper_mask], s=12, c="black", alpha=0.6, label="grey upper (raw)")
    ax2.scatter(xg[lower_mask], yg[lower_mask], s=12, c="dimgray", alpha=0.6, label="grey lower (raw)")
    ax2.scatter(xu[upper_mask], yu[upper_mask], s=18, c="#25e6ff", alpha=0.9, label="upper strand")
    ax2.scatter(xl[lower_mask], yl[lower_mask], s=18, c="#ff38ff", alpha=0.9, label="lower strand")

    for i in range(0, len(xg), max(1, len(xg) // 80)):
        if upper_mask[i]:
            ax2.plot([xg[i], xu[i]], [yg[i], yu[i]], color="#25e6ff", alpha=0.25, lw=0.8)
        else:
            ax2.plot([xg[i], xl[i]], [yg[i], yl[i]], color="#ff38ff", alpha=0.25, lw=0.8)

    ax2.plot(xx, yy, color="#c98c00", lw=2.0, alpha=0.8, label="axis")
    ax2.set_title("Dual Grey Strands")
    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="upper left")

    # ------------------------------------------------------------
    # 3) Angular diagnostics
    # ------------------------------------------------------------
    fig3, axs3 = plt.subplots(2, 2, figsize=(14, 9))

    axs3[0, 0].hist(theta, bins=180, color="steelblue")
    for ang in [52, 56, 139, 221, 319]:
        axs3[0, 0].axvline(ang, color="tab:blue", linestyle="--", alpha=0.8)
    axs3[0, 0].set_title("Angular Distribution (Full Field)")
    axs3[0, 0].set_xlabel("Degrees")
    axs3[0, 0].set_ylabel("Count")

    axs3[0, 1].hist(theta_g, bins=120, color="steelblue")
    for ang in [46, 139, 225, 319]:
        axs3[0, 1].axvline(ang, color="tab:blue", linestyle="--", alpha=0.8)
    axs3[0, 1].set_title("Angular Distribution (Grey Channel)")
    axs3[0, 1].set_xlabel("Degrees")
    axs3[0, 1].set_ylabel("Count")

    axs3[1, 0].plot(dtheta, lw=1.0)
    axs3[1, 0].set_title("Angular Velocity dθ")
    axs3[1, 0].set_xlabel("time step")
    axs3[1, 0].set_ylabel("deg / step")

    axs3[1, 1].plot(theta, lw=1.0)
    axs3[1, 1].set_title("θ over time")
    axs3[1, 1].set_xlabel("time step")
    axs3[1, 1].set_ylabel("deg")

    plt.tight_layout()

    # ------------------------------------------------------------
    # 4) Phase feedback / strand signal
    # ------------------------------------------------------------
    fig4, axs4 = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    axs4[0].plot(coherence, color="#d88f00", lw=1.2)
    axs4[0].set_title("Phase Coherence")
    axs4[0].set_ylabel("coherence")
    axs4[0].grid(True, alpha=0.25)

    axs4[1].plot(strand_signal, color="purple", lw=1.0)
    axs4[1].axhline(0.0, color="black", lw=1.0, alpha=0.5)
    axs4[1].set_title("Dual-Strand Signal")
    axs4[1].set_xlabel("grey-channel index")
    axs4[1].set_ylabel("signed strand score")
    axs4[1].grid(True, alpha=0.25)

    plt.tight_layout()

    # ------------------------------------------------------------
    # 5) Offset overlay / strap
    # ------------------------------------------------------------
    fig5, ax5 = plt.subplots(figsize=(12, 9))
    ax5.scatter(xp[blue_mask], yp[blue_mask], s=3, c="tab:blue", alpha=0.35)
    ax5.scatter(xp[green_mask], yp[green_mask], s=3, c="orange", alpha=0.35)
    ax5.scatter(xp[red_mask], yp[red_mask], s=3, c="tab:green", alpha=0.35)
    ax5.scatter(xg, yg, s=8, c="black", alpha=0.65)
    ax5.scatter(xu[upper_mask], yu[upper_mask], s=16, c="#25e6ff", alpha=0.85)
    ax5.scatter(xl[lower_mask], yl[lower_mask], s=16, c="#ff38ff", alpha=0.85)

    # span-gurt / restriction + elasticity
    ax5.plot(xx, yy, color="#c0c0c0", lw=1.5, alpha=0.9)
    ax5.plot(xx, yy + 1.4, color="#c98c00", lw=2.0, alpha=0.9)
    ax5.plot(xx, yy - 1.4, color="#c98c00", lw=2.0, alpha=0.9)

    ax5.set_title("NEXAH v8.9 — Span-Gurt / Elastic Dual Lock")
    ax5.set_xlabel("X")
    ax5.set_ylabel("Y")
    ax5.grid(True, alpha=0.35)

    # ------------------------------------------------------------
    # 6) Optional coherence polar
    # ------------------------------------------------------------
    fig6 = plt.figure(figsize=(8, 8))
    ax6 = fig6.add_subplot(111, projection="polar")
    th = np.deg2rad(theta)
    coh_norm = 0.45 + 0.55 * (coherence / (np.max(coherence) + 1e-9))
    ax6.scatter(th[::8], coh_norm[::8], c=coh_norm[::8], s=10, cmap="plasma")
    ax6.set_title("NEXAH Coherence — Polar")

    # ============================================================
    # SUMMARY
    # ============================================================
    print("\n=== NEXAH v8.9 Summary ===")
    for k in ["blue", "green", "red", "grey"]:
        print(f"{k}: {counts[k]} ({counts[k] / total:.3f})")
    print(f"grey upper: {counts['grey_upper']}")
    print(f"grey lower: {counts['grey_lower']}")
    print(f"phase coherence min/max/mean: {coherence.min():.4f} {coherence.max():.4f} {coherence.mean():.4f}")
    print(f"grey score min/max/mean: {grey_score.min():.4f} {grey_score.max():.4f} {grey_score.mean():.4f}")
    print(f"grey axis distance min/max/mean: {d_axis[grey_mask].min():.4f} {d_axis[grey_mask].max():.4f} {d_axis[grey_mask].mean():.4f}")

    plt.show()


if __name__ == "__main__":
    main()
