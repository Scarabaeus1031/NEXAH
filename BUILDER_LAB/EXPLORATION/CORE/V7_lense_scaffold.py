# ============================================================
# NEXAH — VISUAL 07: THE LENS (Scaffold)
# Multi-Perspective Coherence Mapping
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# ------------------------------------------------------------
# 1. SYNTHETIC DATA (replace later with real NEXAH outputs)
# ------------------------------------------------------------

np.random.seed(42)

# parametric structure (figure-8 / aperture-like)
t = np.linspace(0, 2*np.pi, 2000)

alpha = 20 * np.sin(t)
beta  = 15 * np.sin(t) * np.cos(t)

# density proxy (add noise cloud)
noise = np.random.normal(scale=2.5, size=(len(t), 2))
density_points = np.stack([alpha, beta], axis=1) + noise

# ridge (downsampled clean structure)
ridge_idx = np.linspace(0, len(t)-1, 120).astype(int)
ridge_alpha = alpha[ridge_idx]
ridge_beta  = beta[ridge_idx]

# aperture ring (smoothed / idealized)
aperture_alpha = alpha
aperture_beta  = beta

# gates (discrete samples along ring)
gate_idx = np.linspace(0, len(t)-1, 16).astype(int)
gate_alpha = alpha[gate_idx]
gate_beta  = beta[gate_idx]

# ghost snake (minimal path)
ghost_alpha = alpha[::50]
ghost_beta  = beta[::50]

# ------------------------------------------------------------
# TIME / COHERENCE (Panel 3)
# ------------------------------------------------------------

time = np.linspace(0, 100, 1000)

signal = np.sin(0.1 * time) * np.exp(0.02 * time)
signal += 0.3 * np.random.randn(len(time))

# simple coherence proxy (rolling correlation)
window = 40
C = np.zeros_like(time)

for i in range(window, len(time)):
    seg = signal[i-window:i]
    if len(seg) > 2:
        C[i] = np.corrcoef(seg[:-1], seg[1:])[0, 1]
    else:
        C[i] = 0

# gate detection (near zero coherence)
threshold = 0.1
gate_times = time[np.abs(C) < threshold]

# ------------------------------------------------------------
# 2. FIGURE LAYOUT
# ------------------------------------------------------------

fig = plt.figure(figsize=(16, 6))
gs = GridSpec(2, 3, height_ratios=[1, 1])

# ============================================================
# PANEL 1 — TOP VIEW (α-β)
# ============================================================

ax1 = fig.add_subplot(gs[:, 0])

# density
ax1.scatter(density_points[:,0], density_points[:,1],
            s=2, alpha=0.2)

# ridge
ax1.plot(ridge_alpha, ridge_beta, linewidth=1)

# aperture
ax1.plot(aperture_alpha, aperture_beta, linewidth=2)

# gates
ax1.scatter(gate_alpha, gate_beta, s=30)

# ghost
ax1.plot(ghost_alpha, ghost_beta, linewidth=1.5)

ax1.set_title("Top View (α-β)")
ax1.set_xlabel("α")
ax1.set_ylabel("β")
ax1.grid(True, alpha=0.3)

# ============================================================
# PANEL 2 — FROG VIEW (β vs synthetic γ)
# ============================================================

ax2 = fig.add_subplot(gs[:, 1], projection='3d')

gamma = np.sin(2*t) * 10  # synthetic third dimension

# density
ax2.scatter(density_points[:,0],
            density_points[:,1],
            np.random.normal(scale=2, size=len(density_points)),
            s=2, alpha=0.2)

# ridge
ax2.plot(ridge_alpha, ridge_beta,
         np.sin(2*t[ridge_idx])*10,
         linewidth=1)

# aperture
ax2.plot(aperture_alpha, aperture_beta,
         gamma,
         linewidth=2)

# gates
ax2.scatter(gate_alpha, gate_beta,
            np.sin(2*t[gate_idx])*10,
            s=30)

# ghost
ax2.plot(ghost_alpha, ghost_beta,
         np.sin(2*t[::50])*10,
         linewidth=1.5)

ax2.set_title("Frog View (3D Projection)")
ax2.set_xlabel("α")
ax2.set_ylabel("β")
ax2.set_zlabel("γ")

# ============================================================
# PANEL 3 — TIME / COHERENCE
# ============================================================

ax3 = fig.add_subplot(gs[0, 2])
ax4 = fig.add_subplot(gs[1, 2])

# signal
ax3.plot(time, signal, linewidth=1)
ax3.set_title("Signal x(t)")
ax3.set_xlabel("time")
ax3.set_ylabel("x(t)")
ax3.grid(True, alpha=0.3)

# coherence
ax4.plot(time, C, linewidth=1)

# zero line
ax4.axhline(0, linestyle='--')

# gates
for gt in gate_times[::50]:  # reduce clutter
    ax4.axvline(gt, linewidth=0.5)

ax4.set_title("Coherence C(t) + Gates")
ax4.set_xlabel("time")
ax4.set_ylabel("C(t)")
ax4.grid(True, alpha=0.3)

# ------------------------------------------------------------
# GLOBAL TITLE
# ------------------------------------------------------------

plt.suptitle("VISUAL 07 — THE NEXAH LENS\nMulti-Perspective Coherence Mapping",
             fontsize=14)

plt.tight_layout()
plt.show()
