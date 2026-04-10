import matplotlib
matplotlib.use('Agg')

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp
from mpl_toolkits.mplot3d import Axes3D

# ============================================================
# PATH
# ============================================================
OUTDIR = Path("/Users/tho2020/Documents/GitHub/NEXAH/APPLICATIONS/power_systems/ieee_xray_pipeline/results")
OUTDIR.mkdir(parents=True, exist_ok=True)

REPORT_PATH = OUTDIR / "v40_olgo_report.txt"
CUBE_PATH   = OUTDIR / "v40_olgo_3d.png"

print(f"\n📁 v40 running → {OUTDIR.resolve()}\n")

# ============================================================
# OLGO RESONANCE
# ============================================================
phi = (1 + np.sqrt(5)) / 2
pi = np.pi

f0 = (phi**3) / (pi**2)
epsilon = 0.029

shells = np.array([f0, f0 + epsilon, f0 + 2*epsilon])

def olgo_proximity(z):
    d = np.min(np.abs(shells - z))
    return np.exp(-80 * d)

# ============================================================
# GRID SETUP
# ============================================================
np.random.seed(42)
net = pp.networks.case57()
net.load.p_mw *= 0.85
net.load.q_mvar *= 0.85

# ============================================================
# STORAGE
# ============================================================
controlled = {
    "coherence": [],
    "radius": [],
    "theta": [],
    "olgo": [],
    "z_olgo": []
}

escape_count = 0

# ============================================================
# MAIN LOOP
# ============================================================
for t in range(400):

    pp.runpp(net, enforce_q_lims=True)

    coh = 1.0 - np.std(net.res_bus.vm_pu)
    sw  = (net.res_bus.vm_pu.mean() - 1.0) * 10

    r = np.hypot(coh - 0.942913, sw - 0.000076)
    theta = np.arctan2(sw - 0.000076, coh - 0.942913)

    # ========================================================
    # OLGO MAPPING
    # ========================================================
    z_olgo = 0.5 * coh + 0.5 * (1 - abs(sw))
    prox = olgo_proximity(z_olgo)

    # ========================================================
    # Lissajous Phase Injection
    # ========================================================
    phase_mod = np.sin(3*t) * np.sin(2*t + np.pi/2)

    # ========================================================
    # CONTROL SIGNAL
    # ========================================================
    u = 0.0

    # classical core (v36-like)
    u += 0.6 * max(0.0, 0.032 - r)
    u += 0.85 * (0.032 + 0.012*np.sin(0.1*t) - r)
    u += 0.15 * (np.pi/4 - theta)

    # ========================================================
    # NEW: OLGO RESONANCE DRIVE
    # ========================================================
    u += 0.08 * prox * phase_mod

    u = np.clip(u, -0.12, 0.12)

    # ========================================================
    # APPLY
    # ========================================================
    factor = 1.0 + u * 0.08
    net.load.p_mw *= factor
    net.load.q_mvar *= factor

    # ========================================================
    # STORE
    # ========================================================
    controlled["coherence"].append(coh)
    controlled["radius"].append(r)
    controlled["theta"].append(theta)
    controlled["olgo"].append(prox)
    controlled["z_olgo"].append(z_olgo)

    if r > 0.055:
        escape_count += 1

# ============================================================
# REPORT
# ============================================================
report = f"""
NEXAH v40 – OLGO Resonance Navigation

Escape count: {escape_count}
Mean coherence: {np.mean(controlled['coherence']):.4f}
Mean radius: {np.mean(controlled['radius']):.4f}
Mean OLGO proximity: {np.mean(controlled['olgo']):.4f}
Max OLGO proximity: {np.max(controlled['olgo']):.4f}
"""

REPORT_PATH.write_text(report)
print(report)

# ============================================================
# 3D PLOT
# ============================================================
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(projection='3d')

x = controlled["radius"]
y = controlled["theta"]
z = controlled["z_olgo"]

sc = ax.scatter(x, y, z, c=controlled["olgo"], cmap='plasma', s=10)

ax.set_xlabel("Radius")
ax.set_ylabel("Theta")
ax.set_zlabel("OLGO Z")

fig.colorbar(sc)

plt.savefig(CUBE_PATH, dpi=150)
plt.close()

print(f"📊 Plot saved: {CUBE_PATH.name}")
