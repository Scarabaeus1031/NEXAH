# ============================================================
# EXPERIMENT 07
# JANUS_PHASE_SYNCHRONIZATION
# ============================================================
#
# Goal:
# Analyze phase synchronization between:
#
# - JANUS coherence
# - curvature
#
# Focus:
# - Hilbert phase extraction
# - phase locking
# - synchronization structure
# - phase drift
#
# Outputs:
# - janus_phase_difference.png
# - janus_phase_locking.png
# - janus_phase_space.png
#
# ============================================================

# file:
# scripts/janus_phase_synchronization.py

import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import solve_ivp
from scipy.signal import hilbert

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
z = sol.y[2]

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
# CURVATURE
# ============================================================

ddx = np.gradient(dx)
ddy = np.gradient(dy)

curvature = np.abs(
    dx * ddy - dy * ddx
) / (
    dx**2 + dy**2
) ** 1.5

curvature = np.log10(curvature + 1e-12)

curvature = (
    curvature - np.min(curvature)
) / (
    np.max(curvature) - np.min(curvature)
)

# ============================================================
# PHASE EXTRACTION
# ============================================================

analytic_janus = hilbert(janus)
analytic_curv = hilbert(curvature)

phase_janus = np.unwrap(
    np.angle(analytic_janus)
)

phase_curv = np.unwrap(
    np.angle(analytic_curv)
)

phase_diff = phase_janus - phase_curv

phase_lock = np.abs(
    np.mean(
        np.exp(1j * phase_diff)
    )
)

# ============================================================
# VISUALIZATION
# ============================================================

# ------------------------------------------------------------
# phase difference
# ------------------------------------------------------------

plt.figure(figsize=(14, 6))

plt.plot(phase_diff)

plt.xlabel("time")
plt.ylabel("phase difference")

plt.title(
    "JANUS vs Curvature — Phase Difference"
)

plt.tight_layout()

plt.savefig(
    "outputs/janus_phase_difference.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# phase locking histogram
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

plt.hist(
    np.mod(phase_diff, 2*np.pi),
    bins=60
)

plt.xlabel("phase difference")
plt.ylabel("count")

plt.title(
    f"Phase Locking Distribution\n"
    f"locking = {phase_lock:.4f}"
)

plt.tight_layout()

plt.savefig(
    "outputs/janus_phase_locking.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# phase space
# ------------------------------------------------------------

plt.figure(figsize=(8, 8))

plt.scatter(
    np.cos(phase_janus),
    np.cos(phase_curv),
    s=2,
    alpha=0.4
)

plt.xlabel("JANUS phase")
plt.ylabel("curvature phase")

plt.title(
    "JANUS vs Curvature — Phase Space"
)

plt.tight_layout()

plt.savefig(
    "outputs/janus_phase_space.png",
    dpi=300
)

plt.close()

# ============================================================
# RESULTS
# ============================================================

print("\n================================================")
print("JANUS PHASE SYNCHRONIZATION")
print("================================================")

print(f"samples: {len(janus)}")
print(f"phase locking value: {phase_lock:.6f}")

print("\nINTERPRETATION:")

if phase_lock > 0.7:
    print("strong phase synchronization")

elif phase_lock > 0.4:
    print("moderate phase synchronization")

else:
    print("weak phase synchronization")

print("\noutputs saved to:")
print("outputs/")
print("================================================")
