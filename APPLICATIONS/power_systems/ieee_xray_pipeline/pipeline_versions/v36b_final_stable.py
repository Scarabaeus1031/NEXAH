"""
v36_good_final.py
=================

NEXAH v36 GOOD FINAL – exakt die stabile Version mit Mean control signal ≈ -0.0770
Vollständige Plots + Agg-Backend + Save-Check
"""

import matplotlib
matplotlib.use('Agg')

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp
from mpl_toolkits.mplot3d import Axes3D

# ============================================================
# 0. PFAD
# ============================================================
OUTDIR = Path("/Users/tho2020/Documents/GitHub/NEXAH/APPLICATIONS/power_systems/ieee_xray_pipeline/results")
OUTDIR.mkdir(parents=True, exist_ok=True)

TS_PATH    = OUTDIR / "v36_good_final_timeseries.png"
POLAR_PATH = OUTDIR / "v36_good_final_polar.png"
CUBE_PATH  = OUTDIR / "v36_good_final_3d.png"
REPORT_PATH= OUTDIR / "v36_good_final_report.txt"

print(f"📁 Speicherort: {OUTDIR.resolve()}\n")

# ============================================================
# 1. SETTINGS – exakt die gute v36
# ============================================================
np.random.seed(42)
net = pp.networks.case57()
net.load.p_mw *= 0.85
net.load.q_mvar *= 0.85

controlled = {"voltage": [], "coherence": [], "radius": [], "dist_elastic": [], "u": [], "gate_score": []}
u_hist = []
escape_count = 0

for t in range(300):
    pp.runpp(net, enforce_q_lims=True)
    v_mean = np.mean(net.res_bus.vm_pu)

    coh = 1.0 - np.std(net.res_bus.vm_pu)
    sw = (net.res_bus.vm_pu.mean() - 1.0) * 10
    r = np.hypot(coh - 0.942913, sw - 0.000076)
    theta = np.arctan2(sw - 0.000076, coh - 0.942913)
    dist_elastic = abs(theta - np.pi/4)
    ncs_prox = np.exp(-8.0 * np.hypot(r - 0.032, theta - np.pi/4))

    u = 0.0
    u += 0.68 * max(0.0, 0.032 - r)
    u += 0.95 * (0.0325 + 0.014*np.sin(0.118*t) - r)
    u += -0.215 * np.exp(-2.0*dist_elastic) * np.sin(theta - np.pi/4 + 0.3)
    u += 0.19 * (np.pi/4 - theta)
    u = np.clip(u, -0.12, 0.12)

    controlled["u"].append(u)
    u_hist.append(u)

    load_factor = 1.0 + u * 0.08
    net.load.p_mw *= load_factor
    net.load.q_mvar *= load_factor

    pp.runpp(net, enforce_q_lims=True)
    v_mean_ctrl = np.mean(net.res_bus.vm_pu)

    controlled["voltage"].append(v_mean_ctrl)
    controlled["coherence"].append(1.0 - np.std(net.res_bus.vm_pu))
    controlled["radius"].append(r)
    controlled["dist_elastic"].append(dist_elastic)
    controlled["gate_score"].append(ncs_prox)

    if r > 0.055:
        escape_count += 1

# ============================================================
# 2. REPORT
# ============================================================
report = f"""NEXAH v36 GOOD FINAL STABLE
Escape count: {escape_count}
Mean coherence: {np.mean(controlled['coherence']):.4f}
Mean distance to Elastic Axis: {np.mean(controlled['dist_elastic']):.4f}
Max NCS proximity: {np.max(controlled['gate_score']):.4f}
Mean control signal: {np.mean(controlled['u']):.4f}
"""
REPORT_PATH.write_text(report, encoding="utf-8")
print(f"✅ Report gespeichert: {REPORT_PATH.name}")

# ============================================================
# 3. PLOTS + SAVE-CHECK
# ============================================================
def save_plot(fig, path, title):
    fig.suptitle(title, fontsize=14)
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches='tight')
    print(f"   Saved {path.name} → exists: {path.exists()}")
    plt.close(fig)

# 5-Subplot Timeseries
fig = plt.figure(figsize=(14, 10))
ax1 = fig.add_subplot(5,1,1); ax1.plot(controlled["voltage"], color="orange"); ax1.set_ylabel("Voltage")
ax2 = fig.add_subplot(5,1,2); ax2.plot(controlled["coherence"], color="blue"); ax2.set_ylabel("Coherence")
ax3 = fig.add_subplot(5,1,3); ax3.plot(controlled["radius"], color="purple"); ax3.axhline(0.0325, color="green", ls="--"); ax3.set_ylabel("Radius")
ax4 = fig.add_subplot(5,1,4); ax4.plot(controlled["dist_elastic"], color="orange"); ax4.set_ylabel("Dist to Elastic Axis")
ax5 = fig.add_subplot(5,1,5); ax5.plot(controlled["u"], color="black"); ax5.set_ylabel("Control u")
save_plot(fig, TS_PATH, "v36_good_final Timeseries")

# Polar
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='polar')
ax.plot(controlled["radius"], controlled["gate_score"], 'b-')
save_plot(fig, POLAR_PATH, "v36_good_final Polar")

# 3D
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(controlled["radius"], [0]*len(controlled["radius"]), controlled["dist_elastic"], c=controlled["gate_score"], cmap='plasma')
save_plot(fig, CUBE_PATH, "v36_good_final 3D Cube")

print("\n✅ v36_good_final fertig – bitte schick mir den kompletten Konsolen-Output!")
