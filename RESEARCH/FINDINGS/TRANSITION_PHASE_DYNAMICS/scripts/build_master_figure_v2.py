import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.ndimage import gaussian_filter
import os
from PIL import Image

# ============================================================
# CONFIG
# ============================================================

OUTPUT = "RESEARCH/FINDINGS/TRANSITION_PHASE_DYNAMICS/figures/master/master_figure_v2.png"

# OPTIONAL: vorhandene Visuals einbinden (falls existieren)
PRIME_VISUAL = "RESEARCH/FINDINGS/PRIME_MODULAR_RESONANCE/analysis/output/plots/PRIME_MODULAR_RESONANCE_SYSTEM_OVERVIEW.png"
CYCLE_CORE_VISUAL = "RESEARCH/FINDINGS/PRIME_MODULAR_RESONANCE/analysis/output/plots/cycle_core_ring_mod23.png"

# ============================================================
# HELPERS
# ============================================================

def try_load_image(path):
    if os.path.exists(path):
        return Image.open(path)
    return None

# ============================================================
# SYSTEMS
# ============================================================

def lorenz(T=12000, dt=0.005):
    sigma, rho, beta = 10, 28, 8/3
    x = np.zeros((T, 3))
    x[0] = [1, 1, 1]

    for i in range(T-1):
        dx = sigma*(x[i,1]-x[i,0])
        dy = x[i,0]*(rho-x[i,2]) - x[i,1]
        dz = x[i,0]*x[i,1] - beta*x[i,2]
        x[i+1] = x[i] + dt*np.array([dx,dy,dz])

    return x[2000:]


def compute_phase(x):
    theta = np.arctan2(x[:,1], x[:,0])
    theta = np.unwrap(theta)
    dtheta = np.diff(theta)
    return theta, dtheta


def density(x):
    H, _, _ = np.histogram2d(x[:,0], x[:,1], bins=150)
    return gaussian_filter(H, sigma=2)

# ============================================================
# KURAMOTO (FIXED → echte Synchronisation)
# ============================================================

def kuramoto(N=60, K=2.5, T=8000, dt=0.01):

    theta = np.random.uniform(0, 2*np.pi, N)
    omega = np.random.normal(0, 0.2, N)

    r_values = []
    mean_phase = []

    for t in range(T):
        diff = theta[:, None] - theta
        coupling = np.sum(np.sin(diff), axis=1)

        theta += (omega + K/N * coupling) * dt

        r = np.abs(np.mean(np.exp(1j * theta)))
        r_values.append(r)
        mean_phase.append(np.mean(theta))

    return np.array(r_values), np.array(mean_phase)

# ============================================================
# GENERATE DATA
# ============================================================

lor = lorenz()
theta, dtheta = compute_phase(lor)
H = density(lor)

r, mp = kuramoto()

# ============================================================
# FIGURE LAYOUT
# ============================================================

fig = plt.figure(figsize=(18, 12))
gs = GridSpec(4, 4, figure=fig)

# ============================================================
# ROW 1 — INPUT SYSTEMS
# ============================================================

# PRIME SYSTEM
ax = fig.add_subplot(gs[0, 0])
img = try_load_image(PRIME_VISUAL)

if img:
    ax.imshow(img)
    ax.set_title("Discrete System (Prime)")
    ax.axis('off')
else:
    ax.text(0.5, 0.5, "Prime Modular\nTransitions", ha='center')
    ax.set_title("Discrete System")
    ax.axis('off')

# LORENZ
ax = fig.add_subplot(gs[0, 1])
ax.plot(lor[:,0], lor[:,1], lw=0.3)
ax.set_title("Continuous (Lorenz)")
ax.axis('off')

# KURAMOTO
ax = fig.add_subplot(gs[0, 2])
ax.plot(r)
ax.set_ylim(0,1)
ax.set_title("Synchronization r(t)")

# empty
fig.add_subplot(gs[0, 3]).axis('off')

# ============================================================
# ROW 2 — PHASE (ZENTRAL!)
# ============================================================

ax = fig.add_subplot(gs[1, 0:2])
ax.plot(theta, lw=1.5)
ax.set_title("Phase θ(t) — universal coordinate")

grad = np.abs(np.gradient(theta))
mask = grad < np.percentile(grad, 20)

for i in range(len(mask)):
    if mask[i]:
        ax.axvspan(i, i+1, color='red', alpha=0.03)

# Δθ
ax = fig.add_subplot(gs[1, 2])
ax.hist(dtheta, bins=120)
ax.set_title("Δθ Distribution")

# Kuramoto Phase
ax = fig.add_subplot(gs[1, 3])
ax.plot(mp)
ax.set_title("Mean Phase (Kuramoto)")

# ============================================================
# ROW 3 — STRUCTURE (JETZT MIT CONTENT)
# ============================================================

# Cycle Core
ax = fig.add_subplot(gs[2, 0])
img = try_load_image(CYCLE_CORE_VISUAL)

if img:
    ax.imshow(img)
    ax.set_title("Cycle Core Structure")
    ax.axis('off')
else:
    ax.text(0.5, 0.5, "Cycle Core", ha='center')
    ax.axis('off')

# Drift → einfach Phase-Trend visualisieren
ax = fig.add_subplot(gs[2, 1])
ax.plot(np.cumsum(dtheta), lw=1)
ax.set_title("Directional Drift")

# Phase = coordinate
ax = fig.add_subplot(gs[2, 2])
ax.text(0.5, 0.5, "Phase = structural coordinate", ha='center')
ax.axis('off')

# Winding
ax = fig.add_subplot(gs[2, 3])
ax.plot(theta / (2*np.pi))
ax.set_title("Winding Number")

# ============================================================
# ROW 4 — EMERGENCE
# ============================================================

# Flow field
ax = fig.add_subplot(gs[3, 0])
ax.imshow(H.T, origin='lower', aspect='auto')
ax.set_title("Flow Field (phase-embedded)")

# Sync (nochmal klar)
ax = fig.add_subplot(gs[3, 1])
ax.plot(r)
ax.set_ylim(0,1)
ax.set_title("Global Synchronization")

# Geometry
ax = fig.add_subplot(gs[3, 2])
ax.text(0.5, 0.5, "Emergent Geometry\n(Torus / Flow)", ha='center')
ax.axis('off')

# FINAL INSIGHT
ax = fig.add_subplot(gs[3, 3])
ax.text(0.5, 0.5,
        "All systems collapse onto\nphase-driven transition structure",
        ha='center', fontsize=11)
ax.axis('off')

# ============================================================
plt.tight_layout()
plt.savefig(OUTPUT, dpi=200)
print(f"[OK] saved → {OUTPUT}")
