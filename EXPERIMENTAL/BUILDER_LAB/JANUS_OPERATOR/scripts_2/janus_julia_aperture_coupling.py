# ============================================================
# EXP-22 — JANUS ⇄ JULIA APERTURE COUPLING
# ============================================================
#
# Goal:
# Connect JANUS aperture peaks with local Julia geometries.
#
# Pipeline:
#
# Lorenz Dynamics
# → JANUS Aperture Score
# → Gate Candidates
# → c-plane Mapping
# → Julia Generation
# → Geometry Overlay
#
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.ndimage import gaussian_gradient_magnitude
from mpl_toolkits.mplot3d import Axes3D

# ============================================================
# OUTPUT DIRECTORY
# ============================================================

OUTPUT_DIR = "EXPERIMENTAL/BUILDER_LAB/JANUS_OPERATOR/outputs/"

# ============================================================
# LORENZ SYSTEM
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

t0 = 0
t1 = 120
samples = 12000

t_eval = np.linspace(t0, t1, samples)

initial_state = [0.1, 1.0, 1.05]

sol = solve_ivp(
    lorenz,
    (t0, t1),
    initial_state,
    t_eval=t_eval
)

x = sol.y[0]
y = sol.y[1]
z = sol.y[2]

# ============================================================
# JANUS APERTURE SCORE
# ============================================================

vx = np.gradient(x)
vy = np.gradient(y)
vz = np.gradient(z)

speed = np.sqrt(vx**2 + vy**2 + vz**2)

ax = np.gradient(vx)
ay = np.gradient(vy)
az = np.gradient(vz)

accel = np.sqrt(ax**2 + ay**2 + az**2)

# normalized aperture score

eps = 1e-8

aperture = accel / (speed + eps)

# smooth

from scipy.ndimage import gaussian_filter1d

aperture_smooth = gaussian_filter1d(aperture, sigma=6)

# ============================================================
# GATE DETECTION
# ============================================================

threshold = np.percentile(aperture_smooth, 99.5)

gate_mask = aperture_smooth >= threshold

gate_indices = np.where(gate_mask)[0]

# ============================================================
# MAP TO JULIA PARAMETER SPACE
# ============================================================

# normalize Lorenz coordinates

xn = (x - np.min(x)) / (np.max(x) - np.min(x))
yn = (y - np.min(y)) / (np.max(y) - np.min(y))

# map into Mandelbrot neighborhood

c_real = -1.2 + xn * 1.6
c_imag = -0.8 + yn * 1.6

# ============================================================
# JULIA GENERATOR
# ============================================================

def julia_set(c, N=400, bound=2, max_iter=80):

    xmin, xmax = -1.5, 1.5
    ymin, ymax = -1.5, 1.5

    X = np.linspace(xmin, xmax, N)
    Y = np.linspace(ymin, ymax, N)

    Z = X[:, None] + 1j * Y[None, :]

    output = np.zeros(Z.shape)

    mask = np.ones(Z.shape, dtype=bool)

    for i in range(max_iter):

        Z[mask] = Z[mask]**2 + c

        escaped = np.abs(Z) > bound

        output[escaped & mask] = i

        mask &= ~escaped

    output[output == 0] = max_iter

    return output

# ============================================================
# SELECT TOP GATES
# ============================================================

top_gates = gate_indices[:6]

# ============================================================
# PLOT 1 — LORENZ APERTURE GATES
# ============================================================

fig = plt.figure(figsize=(10, 8))

ax3d = fig.add_subplot(111, projection='3d')

ax3d.plot(
    x,
    y,
    z,
    color='lightgray',
    alpha=0.15,
    linewidth=0.5
)

sc = ax3d.scatter(
    x[top_gates],
    y[top_gates],
    z[top_gates],
    c=aperture_smooth[top_gates],
    cmap='plasma',
    s=50
)

ax3d.set_title("EXP-22 — JANUS Aperture Gate Mapping")

plt.colorbar(sc, label="Aperture Score")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR + "exp22_lorenz_aperture_gates.png",
    dpi=300
)

plt.close()

# ============================================================
# PLOT 2 — JULIA SYSTEMS
# ============================================================

fig, axes = plt.subplots(2, 3, figsize=(12, 8))

axes = axes.flatten()

for idx, gate in enumerate(top_gates):

    c = c_real[gate] + 1j * c_imag[gate]

    J = julia_set(c)

    ax = axes[idx]

    ax.imshow(
        J.T,
        cmap='magma',
        origin='lower',
        extent=[-1.5, 1.5, -1.5, 1.5]
    )

    ax.set_title(
        f"c={c.real:.2f}+{c.imag:.2f}i"
    )

    ax.set_xticks([])
    ax.set_yticks([])

plt.suptitle("EXP-22 — Local Julia Geometries")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR + "exp22_julia_gate_geometries.png",
    dpi=300
)

plt.close()

# ============================================================
# PLOT 3 — APERTURE TIMESERIES
# ============================================================

plt.figure(figsize=(12, 4))

plt.plot(
    aperture_smooth,
    color='darkorange',
    linewidth=1
)

plt.axhline(
    threshold,
    color='red',
    linestyle='--',
    label='gate threshold'
)

plt.scatter(
    gate_indices,
    aperture_smooth[gate_indices],
    color='black',
    s=10
)

plt.title("EXP-22 — Aperture Gate Timeseries")

plt.xlabel("Time")
plt.ylabel("Aperture")

plt.legend()

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR + "exp22_aperture_timeseries.png",
    dpi=300
)

plt.close()

# ============================================================
# PLOT 4 — PARAMETER SPACE MAP
# ============================================================

plt.figure(figsize=(8, 8))

plt.scatter(
    c_real,
    c_imag,
    c=aperture_smooth,
    cmap='viridis',
    s=1,
    alpha=0.5
)

plt.scatter(
    c_real[top_gates],
    c_imag[top_gates],
    color='red',
    s=80,
    edgecolors='white'
)

plt.title("EXP-22 — Lorenz → Julia Parameter Mapping")

plt.xlabel("Re(c)")
plt.ylabel("Im(c)")

plt.colorbar(label="Aperture Score")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR + "exp22_parameter_mapping.png",
    dpi=300
)

plt.close()

# ============================================================
# PLOT 5 — GEOMETRY COMPARISON
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# left = Lorenz gates

axes[0].scatter(
    x,
    z,
    c=aperture_smooth,
    cmap='plasma',
    s=0.5
)

axes[0].scatter(
    x[top_gates],
    z[top_gates],
    color='cyan',
    s=40
)

axes[0].set_title("Lorenz Gate Geometry")

# right = parameter space

axes[1].scatter(
    c_real,
    c_imag,
    c=aperture_smooth,
    cmap='magma',
    s=1
)

axes[1].scatter(
    c_real[top_gates],
    c_imag[top_gates],
    color='cyan',
    s=50
)

axes[1].set_title("Mapped Julia Gate Space")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR + "exp22_geometry_comparison.png",
    dpi=300
)

plt.close()

# ============================================================
# SUMMARY
# ============================================================

print("\n======================================")
print("EXP-22 — JANUS ⇄ JULIA COUPLING")
print("======================================\n")

print(f"samples: {samples}")
print(f"gate candidates: {len(gate_indices)}")

print("\nthreshold:")
print(f"{threshold:.6f}")

print("\noutputs generated:\n")

print("exp22_lorenz_aperture_gates.png")
print("exp22_julia_gate_geometries.png")
print("exp22_aperture_timeseries.png")
print("exp22_parameter_mapping.png")
print("exp22_geometry_comparison.png")

print("\nEXP-22 complete.\n")
