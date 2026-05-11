import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import os

# ============================================================
# PARAMETERS
# ============================================================

N = 32000
DT = 0.0125

MODULUS = 23

WINDOW = 8

np.random.seed(7)

# ============================================================
# JANUS ROPE FIELD
# ============================================================

t = np.arange(N) * DT

# layered frequencies
f1 = 2.0
f2 = 3.0
f3 = 5.0
f4 = 7.0

# coupled rope field
x = (
    0.45*np.sin(f1*t)
    + 0.28*np.sin(f2*t + 0.6)
    + 0.15*np.sin(f3*t + 1.4)
)

y = (
    0.52*np.cos(f2*t)
    + 0.25*np.cos(f3*t + 0.3)
    + 0.14*np.sin(f4*t + 1.1)
)

# ============================================================
# OFFSET POLE
# ============================================================

pole = np.array([1.0, 0.0])

dx = x - pole[0]
dy = y - pole[1]

angles = np.degrees(np.arctan2(dy, dx)) % 360

# ============================================================
# RESIDUE STATES
# ============================================================

states = np.floor(
    (angles / 360.0) * MODULUS
).astype(int)

states = np.clip(states, 0, MODULUS-1)

# ============================================================
# DRIFT VECTOR RECONSTRUCTION
# ============================================================

# average local motion per residue state

drift_vectors = defaultdict(list)

for i in range(N - WINDOW):

    s = states[i]

    px = x[i]
    py = y[i]

    qx = x[i + WINDOW]
    qy = y[i + WINDOW]

    vx = qx - px
    vy = qy - py

    drift_vectors[s].append((vx, vy))

# average vectors

mean_vectors = {}

for s in range(MODULUS):

    arr = np.array(drift_vectors[s])

    if len(arr) > 0:
        mean_vectors[s] = arr.mean(axis=0)
    else:
        mean_vectors[s] = np.array([0, 0])

# ============================================================
# RESIDUE CENTERS
# ============================================================

centers = {}

for s in range(MODULUS):

    mask = states == s

    if np.sum(mask) > 0:
        centers[s] = (
            x[mask].mean(),
            y[mask].mean()
        )
    else:
        centers[s] = (0, 0)

# ============================================================
# DRIFT STRENGTH
# ============================================================

strength = np.zeros(MODULUS)

for s in range(MODULUS):

    vx, vy = mean_vectors[s]

    strength[s] = np.sqrt(vx**2 + vy**2)

# ============================================================
# OUTPUT FOLDER CREATION
# ============================================================
output_dir = "outputs/EXP_08"
os.makedirs(output_dir, exist_ok=True)

# ============================================================
# VISUAL 1
# LOCAL DRIFT VECTOR FIELD
# ============================================================

fig, ax = plt.subplots(figsize=(10,10))

ax.scatter(x, y, s=1, alpha=0.05, color='gray')

for s in range(MODULUS):

    cx, cy = centers[s]
    vx, vy = mean_vectors[s]

    ax.arrow(
        cx, cy,
        vx*8,
        vy*8,
        color=plt.cm.plasma(strength[s]/strength.max()),
        width=0.003,
        head_width=0.03,
        alpha=0.95
    )

    ax.text(cx, cy, str(s), fontsize=8)

ax.scatter(
    pole[0],
    pole[1],
    marker='x',
    s=400,
    linewidths=4,
    color='tab:blue'
)

ax.set_title(
    "EXP_08 — Local Drift Vector Field",
    fontsize=22
)

ax.set_aspect('equal')

plt.tight_layout()
phase_locking_filepath = f"{output_dir}/exp08_phase_locking.png"
plt.savefig(phase_locking_filepath, dpi=300)

# ============================================================
# VISUAL 2
# PHASE DRIFT SYNC
# ============================================================

fig, ax = plt.subplots(figsize=(10,10))

ax.scatter(x, y, s=3, alpha=0.1, color='gray')

for s in range(MODULUS):

    cx, cy = centers[s]
    vx, vy = mean_vectors[s]

    ax.arrow(
        cx, cy,
        vx*10,
        vy*10,
        color=plt.cm.viridis(strength[s]/strength.max()),
        width=0.005,
        head_width=0.05,
        alpha=0.75
    )

ax.set_title(
    "EXP_08 — Phase Drift Synchronization",
    fontsize=22
)

ax.set_aspect('equal')

plt.tight_layout()
phase_sync_filepath = f"{output_dir}/exp08_phase_drift_sync.png"
plt.savefig(phase_sync_filepath, dpi=300)

# ============================================================
# VISUAL 3
# PHASE DEVIATION HEATMAP
# ============================================================

fig, ax = plt.subplots(figsize=(12,4))

heat = strength.reshape(1,-1)

ax.imshow(
    heat,
    cmap='magma',
    aspect='auto'
)

ax.set_xticks(np.arange(MODULUS))
ax.set_yticks([])

ax.set_title(
    "EXP_08 — Phase Deviation Heatmap",
    fontsize=22
)

plt.tight_layout()
phase_deviation_filepath = f"{output_dir}/exp08_phase_deviation_heatmap.png"
plt.savefig(phase_deviation_filepath, dpi=300)

# ============================================================
# VISUAL 4
# TRANSPORT CORRIDOR OVERLAY
# ============================================================

fig, ax = plt.subplots(figsize=(10,10))

ax.scatter(
    x,
    y,
    c=states,
    cmap='tab20',
    s=3,
    alpha=0.25
)

top_states = np.argsort(strength)[-6:]

for s in top_states:

    mask = states == s

    ax.scatter(
        x[mask],
        y[mask],
        s=8,
        alpha=0.7,
        label=f"state {s}"
    )

ax.scatter(
    pole[0],
    pole[1],
    marker='x',
    s=350,
    linewidths=4,
    color='tab:blue'
)

ax.legend()

ax.set_title(
    "EXP_08 — Transport Corridor Overlay",
    fontsize=22
)

ax.set_aspect('equal')

plt.tight_layout()
transport_corridors_filepath = f"{output_dir}/exp08_transport_corridors.png"
plt.savefig(transport_corridors_filepath, dpi=300)

# ============================================================
# VISUAL 5
# MODULAR VORTEX RECONSTRUCTION
# ============================================================

grid_n = 200

gx = np.linspace(-1.2, 1.2, grid_n)
gy = np.linspace(-1.4, 0.6, grid_n)

GX, GY = np.meshgrid(gx, gy)

VX = np.zeros_like(GX)
VY = np.zeros_like(GY)

for s in range(MODULUS):

    cx, cy = centers[s]
    vx, vy = mean_vectors[s]

    dist2 = (GX - cx)**2 + (GY - cy)**2

    weight = np.exp(-dist2 / 0.05)

    VX += vx * weight
    VY += vy * weight

speed = np.sqrt(VX**2 + VY**2)

speed = gaussian_filter(speed, sigma=1.0)

fig, ax = plt.subplots(figsize=(12,10))

ax.streamplot(
    gx,
    gy,
    VX,
    VY,
    color=speed,
    cmap='plasma',
    density=2.2,
    linewidth=1.5
)

ax.scatter(
    pole[0],
    pole[1],
    marker='x',
    s=450,
    linewidths=5,
    color='cyan'
)

ax.set_title(
    "EXP_08 — Modular Vortex Reconstruction",
    fontsize=24
)

ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.4, 0.6)

ax.set_aspect('equal')

plt.tight_layout()
modular_vortex_filepath = f"{output_dir}/exp08_modular_vortex_reconstruction.png"
plt.savefig(modular_vortex_filepath, dpi=300)

# ============================================================
# SUMMARY
# ============================================================

print("\n===================================")
print("EXP_08 — Phase Locking Analysis")
print("===================================\n")

print(f"Samples: {N}")
print(f"Modulus: {MODULUS}")

print("\nStrongest drift states:")
print("-----------------------------------")

for s in top_states[::-1]:
    print(
        f"state {s}: "
        f"strength={strength[s]:.5f}"
    )

print("\nGenerated visuals:")
print("-----------------------------------")

files = [
    "exp08_phase_locking.png",
    "exp08_phase_drift_sync.png",
    "exp08_phase_deviation_heatmap.png",
    "exp08_transport_corridors.png",
    "exp08_modular_vortex_reconstruction.png"
]

for f in files:
    print(f)

print("\nDONE.\n")
