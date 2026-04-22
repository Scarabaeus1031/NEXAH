# APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/ieee_boundary_tracking.py

"""
NEXAH — IEEE Boundary Tracking

Goal:
→ track boundary formation over time
→ compare with voltage collapse

Output:
→ plot: voltage vs boundary_energy
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# CONFIG
# ============================================================

STEPS = 80
SIZE = 120

OUTDIR = "APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/outputs"
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# SYNTHETIC FIELD EVOLUTION (proxy for system stress)
# ============================================================

def generate_field(t):
    """
    simple evolving field:
    → center gets sharper over time
    → mimics stress / collapse
    """
    x = np.linspace(-2, 2, SIZE)
    y = np.linspace(-2, 2, SIZE)
    X, Y = np.meshgrid(x, y)

    # narrowing Gaussian = increasing instability
    sigma = 1.2 - 0.01 * t
    sigma = max(0.2, sigma)

    field = np.exp(-(X**2 + Y**2) / (2 * sigma**2))

    # add slight asymmetry over time
    field += 0.15 * np.sin(3 * X + t * 0.05)

    return field

# ============================================================
# REGIME MAP (simplified V10 logic)
# ============================================================

def compute_regime_map(field):

    gy, gx = np.gradient(field)

    grad_mag = np.sqrt(gx**2 + gy**2)
    dens_norm = field / (np.max(field) + 1e-8)
    grad_norm = grad_mag / (np.max(grad_mag) + 1e-8)

    regime_map = np.zeros_like(field, dtype=int)

    for y in range(field.shape[0]):
        for x in range(field.shape[1]):

            d = dens_norm[y, x]
            g = grad_norm[y, x]

            if d > 0.6:
                regime_map[y, x] = 0  # core
            elif g > 0.4:
                regime_map[y, x] = 1  # orbit
            elif g < 0.2:
                regime_map[y, x] = 2  # escape
            else:
                regime_map[y, x] = 3  # drift

    return regime_map

# ============================================================
# BOUNDARY ENERGY
# ============================================================

def compute_boundary_energy(regime_map):

    ny, nx = regime_map.shape
    boundary = 0

    for y in range(ny - 1):
        for x in range(nx - 1):
            if (
                regime_map[y, x] != regime_map[y, x + 1] or
                regime_map[y, x] != regime_map[y + 1, x]
            ):
                boundary += 1

    return boundary / (ny * nx)

# ============================================================
# VOLTAGE CURVE (CLASSICAL)
# ============================================================

def voltage_curve(t):
    """
    typical collapse curve
    """
    return np.exp(-0.08 * t)

# ============================================================
# MAIN LOOP
# ============================================================

boundary_energy = []
voltage = []

for t in range(STEPS):

    field = generate_field(t)
    regime_map = compute_regime_map(field)

    b = compute_boundary_energy(regime_map)
    v = voltage_curve(t)

    boundary_energy.append(b)
    voltage.append(v)

    print(f"t={t:02d}  boundary={b:.4f}  voltage={v:.4f}")

boundary_energy = np.array(boundary_energy)
voltage = np.array(voltage)

# ============================================================
# NORMALIZE FOR VISUAL COMPARISON
# ============================================================

boundary_norm = boundary_energy / (np.max(boundary_energy) + 1e-8)
voltage_norm = voltage / np.max(voltage)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(voltage_norm, label="Voltage (classical)", color="red")
plt.plot(boundary_norm, label="Boundary Energy (NEXAH)", color="purple")

plt.xlabel("Time")
plt.ylabel("Normalized Value")
plt.title("NEXAH vs Classical — Boundary vs Voltage Collapse")

plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "ieee_boundary_tracking.png"), dpi=160)

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "boundary_energy.npy"), boundary_energy)
np.save(os.path.join(OUTDIR, "voltage.npy"), voltage)

print("✓ saved results →", OUTDIR)
