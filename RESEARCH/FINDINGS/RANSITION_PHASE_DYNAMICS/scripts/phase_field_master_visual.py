import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# ============================================================
# CONFIG
# ============================================================

OUTPUT_PATH = "RESEARCH/FINDINGS/TRANSITION_PHASE_DYNAMICS/figures/master"
import os
os.makedirs(OUTPUT_PATH, exist_ok=True)

T = 20000
DT = 0.01

# ============================================================
# SYSTEMS
# ============================================================

def lorenz():
    sigma, rho, beta = 10, 28, 8/3
    x = np.zeros((T, 3))
    x[0] = [1, 1, 1]

    for i in range(T-1):
        dx = sigma*(x[i,1]-x[i,0])
        dy = x[i,0]*(rho-x[i,2]) - x[i,1]
        dz = x[i,0]*x[i,1] - beta*x[i,2]
        x[i+1] = x[i] + DT*np.array([dx,dy,dz])

    return x

def rossler():
    a, b, c = 0.2, 0.2, 5.7
    x = np.zeros((T, 3))
    x[0] = [1, 1, 1]

    for i in range(T-1):
        dx = -x[i,1] - x[i,2]
        dy = x[i,0] + a*x[i,1]
        dz = b + x[i,2]*(x[i,0] - c)
        x[i+1] = x[i] + DT*np.array([dx,dy,dz])

    return x

def halvorsen():
    a = 1.4
    x = np.zeros((T, 3))
    x[0] = [1, 1, 1]

    for i in range(T-1):
        dx = -a*x[i,0] - 4*x[i,1] - 4*x[i,2] - x[i,1]**2
        dy = -a*x[i,1] - 4*x[i,2] - 4*x[i,0] - x[i,2]**2
        dz = -a*x[i,2] - 4*x[i,0] - 4*x[i,1] - x[i,0]**2

        step = DT*np.array([dx,dy,dz])

        if np.any(np.isnan(step)) or np.linalg.norm(step) > 50:
            x[i+1] = x[i]
        else:
            x[i+1] = x[i] + step

    return x

# ============================================================
# PHASE + ANALYSIS
# ============================================================

def compute_phase(x):
    theta = np.arctan2(x[:,1], x[:,0])
    theta_unwrapped = np.unwrap(theta)
    dtheta = np.diff(theta_unwrapped)
    return theta_unwrapped, dtheta

def density_field(x, bins=200):
    H, xedges, yedges = np.histogram2d(
        x[:,0], x[:,1], bins=bins
    )
    H = gaussian_filter(H, sigma=2)
    return H, xedges, yedges

# ============================================================
# PLOT FUNCTION
# ============================================================

def plot_system(ax_row, data, name):

    x = data

    # ---- trajectory
    ax = ax_row[0]
    ax.plot(x[:,0], x[:,1], lw=0.5)
    ax.set_title(f"{name} — Trajectory")
    ax.set_xticks([]); ax.set_yticks([])

    # ---- density
    ax = ax_row[1]
    H, xe, ye = density_field(x)
    ax.imshow(H.T, origin='lower', aspect='auto')
    ax.set_title("Field / Density")
    ax.set_xticks([]); ax.set_yticks([])

    # ---- phase
    theta, dtheta = compute_phase(x)

    ax = ax_row[2]
    ax.plot(theta, lw=1)
    ax.set_title("Phase θ(t)")
    ax.set_xticks([])

    # plateau shading
    grad = np.abs(np.gradient(theta))
    mask = grad < np.percentile(grad, 25)

    for i in range(len(mask)):
        if mask[i]:
            ax.axvspan(i, i+1, color='red', alpha=0.05)

    # ---- distribution
    ax = ax_row[3]
    ax.hist(dtheta, bins=100)
    ax.set_title("Δθ Distribution")

# ============================================================
# MAIN
# ============================================================

fig, axes = plt.subplots(3, 4, figsize=(18, 12))

systems = [
    ("Lorenz", lorenz()),
    ("Rössler", rossler()),
    ("Halvorsen", halvorsen())
]

for i, (name, data) in enumerate(systems):
    plot_system(axes[i], data, name)

plt.tight_layout()
plt.savefig(f"{OUTPUT_PATH}/phase_field_master_visual.png", dpi=200)
print(f"[OK] saved → {OUTPUT_PATH}/phase_field_master_visual.png")
