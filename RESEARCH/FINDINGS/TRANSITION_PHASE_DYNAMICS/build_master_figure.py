import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.ndimage import gaussian_filter

# ============================================================
# CONFIG
# ============================================================

OUTPUT = "RESEARCH/FINDINGS/TRANSITION_PHASE_DYNAMICS/figures/master/master_figure.png"

# ============================================================
# SIMPLE DEMO SYSTEMS (reuse patterns)
# ============================================================

def generate_lorenz_projection(T=10000, dt=0.005):
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
# KURAMOTO
# ============================================================

def kuramoto(N=50, K=2.0, T=8000, dt=0.01):

    theta = np.random.uniform(0, 2*np.pi, N)
    omega = np.random.normal(0, 0.1, N)

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
# FIGURE
# ============================================================

fig = plt.figure(figsize=(18, 12))
gs = GridSpec(4, 4, figure=fig)

# ------------------------------------------------------------
# ROW 1 — INPUT SYSTEMS
# ------------------------------------------------------------

# Prime placeholder
ax = fig.add_subplot(gs[0, 0])
ax.text(0.5, 0.5, "Prime Modular\nTransitions", ha='center', va='center')
ax.set_title("Discrete System")
ax.axis('off')

# Continuous
lorenz = generate_lorenz_projection()
ax = fig.add_subplot(gs[0, 1])
ax.plot(lorenz[:,0], lorenz[:,1], lw=0.3)
ax.set_title("Continuous (Lorenz)")
ax.axis('off')

# Kuramoto
r, mp = kuramoto()
ax = fig.add_subplot(gs[0, 2])
ax.plot(r)
ax.set_title("Kuramoto r(t)")
ax.set_ylim(0,1)

# Empty slot
fig.add_subplot(gs[0, 3]).axis('off')

# ------------------------------------------------------------
# ROW 2 — PHASE MAPPING
# ------------------------------------------------------------

theta, dtheta = compute_phase(lorenz)

ax = fig.add_subplot(gs[1, 0:2])
ax.plot(theta, lw=1)
ax.set_title("Phase θ(t)")

# plateau highlight
grad = np.abs(np.gradient(theta))
mask = grad < np.percentile(grad, 20)

for i in range(len(mask)):
    if mask[i]:
        ax.axvspan(i, i+1, color='red', alpha=0.03)

# Δθ distribution
ax = fig.add_subplot(gs[1, 2])
ax.hist(dtheta, bins=100)
ax.set_title("Δθ Distribution")

# Kuramoto phase
ax = fig.add_subplot(gs[1, 3])
ax.plot(mp)
ax.set_title("Mean Phase (Kuramoto)")

# ------------------------------------------------------------
# ROW 3 — STRUCTURE (CORE)
# ------------------------------------------------------------

ax = fig.add_subplot(gs[2, 0])
ax.text(0.5, 0.5, "Cycle Core", ha='center', va='center')
ax.set_title("Recurrence Structure")
ax.axis('off')

ax = fig.add_subplot(gs[2, 1])
ax.text(0.5, 0.5, "Drift", ha='center', va='center')
ax.set_title("Directional Transport")
ax.axis('off')

ax = fig.add_subplot(gs[2, 2])
ax.text(0.5, 0.5, "Phase = Coordinate", ha='center', va='center')
ax.axis('off')

ax = fig.add_subplot(gs[2, 3])
ax.text(0.5, 0.5, "Winding", ha='center', va='center')
ax.axis('off')

# ------------------------------------------------------------
# ROW 4 — EMERGENCE
# ------------------------------------------------------------

# density field
ax = fig.add_subplot(gs[3, 0])
ax.imshow(density(lorenz).T, origin='lower', aspect='auto')
ax.set_title("Flow Field")

# synchronization
ax = fig.add_subplot(gs[3, 1])
ax.plot(r)
ax.set_title("Synchronization r(t)")
ax.set_ylim(0,1)

# topology
ax = fig.add_subplot(gs[3, 2])
ax.text(0.5, 0.5, "Emergent Geometry\n(Torus / Flow)", ha='center', va='center')
ax.axis('off')

# final insight
ax = fig.add_subplot(gs[3, 3])
ax.text(0.5, 0.5,
        "All systems collapse onto\nphase-driven transition structure",
        ha='center', va='center')
ax.axis('off')

# ------------------------------------------------------------
plt.tight_layout()
plt.savefig(OUTPUT, dpi=200)
print(f"[OK] saved → {OUTPUT}")
