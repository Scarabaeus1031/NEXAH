# ============================================================
# EXPERIMENT 08
# JANUS_MULTI_SCALE_ANALYSIS
# ============================================================
#
# Goal:
# Analyze JANUS behavior across multiple
# temporal smoothing scales.
#
# Focus:
# - scale persistence
# - coherence robustness
# - structure stability
# - transition persistence
#
# Outputs:
# - janus_multiscale_overlay.png
# - janus_scale_variance.png
# - janus_scale_heatmap.png
#
# ============================================================

# file:
# scripts/janus_multiscale_analysis.py

import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import solve_ivp
from scipy.ndimage import gaussian_filter1d

plt.style.use("ggplot")

# ============================================================
# LORENZ
# ============================================================

sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0


def lorenz(t, state):

    x, y, z = state

    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    return [dx, dy, dz]


# ============================================================
# SIMULATION
# ============================================================

dt = 0.01
T = 120

t_eval = np.arange(0, T, dt)

sol = solve_ivp(
    lorenz,
    [0, T],
    [1, 1, 1],
    t_eval=t_eval,
)

x = sol.y[0]
y = sol.y[1]

# ============================================================
# JANUS
# ============================================================

dx = np.gradient(x)
dy = np.gradient(y)

theta = np.arctan2(dy, dx)

janus = np.abs(np.cos(theta))

janus = (
    janus - np.min(janus)
) / (
    np.max(janus) - np.min(janus)
)

# ============================================================
# MULTISCALE
# ============================================================

scales = [1, 2, 5, 10, 20, 40]

signals = []

for s in scales:

    smoothed = gaussian_filter1d(
        janus,
        sigma=s
    )

    signals.append(smoothed)

signals = np.array(signals)

# ============================================================
# VARIANCE
# ============================================================

scale_var = np.var(
    signals,
    axis=1
)

# ============================================================
# VISUALIZATION
# ============================================================

# ------------------------------------------------------------
# overlay
# ------------------------------------------------------------

plt.figure(figsize=(14, 7))

for i, s in enumerate(scales):

    plt.plot(
        signals[i],
        label=f"scale={s}",
        alpha=0.8
    )

plt.xlabel("time")
plt.ylabel("JANUS coherence")

plt.title(
    "JANUS Multi-Scale Overlay"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    "outputs/janus_multiscale_overlay.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# scale variance
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    scales,
    scale_var,
    marker="o"
)

plt.xlabel("smoothing scale")
plt.ylabel("variance")

plt.title(
    "JANUS Scale Variance"
)

plt.tight_layout()

plt.savefig(
    "outputs/janus_scale_variance.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# heatmap
# ------------------------------------------------------------

plt.figure(figsize=(14, 6))

plt.imshow(
    signals,
    aspect="auto",
    origin="lower"
)

plt.yticks(
    np.arange(len(scales)),
    scales
)

plt.xlabel("time")
plt.ylabel("scale")

plt.title(
    "JANUS Multi-Scale Heatmap"
)

plt.colorbar(label="coherence")

plt.tight_layout()

plt.savefig(
    "outputs/janus_scale_heatmap.png",
    dpi=300
)

plt.close()

# ============================================================
# RESULTS
# ============================================================

print("\n================================================")
print("JANUS MULTI-SCALE ANALYSIS")
print("================================================")

print(f"samples: {len(janus)}")

print("\nvariance per scale:")

for s, v in zip(scales, scale_var):

    print(
        f"scale={s:>3} "
        f"variance={v:.6f}"
    )

print("\nINTERPRETATION:")
print(
    "persistent structure across scales "
    "indicates coherence robustness"
)

print("\noutputs saved to:")
print("outputs/")
print("================================================")
