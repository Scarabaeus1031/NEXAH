"""
v36_minimal_test.py
===================

Minimal-Test für v36 – nur 3 Plots + Save-Check
Genau die Parameter mit Mean control signal ≈ -0.0770
"""

import matplotlib
matplotlib.use('Agg')

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp

# ============================================================
# 0. PFAD
# ============================================================
OUTDIR = Path("/Users/tho2020/Documents/GitHub/NEXAH/APPLICATIONS/power_systems/ieee_xray_pipeline/results")
OUTDIR.mkdir(parents=True, exist_ok=True)

TS_PATH    = OUTDIR / "v36_test_timeseries.png"
POLAR_PATH = OUTDIR / "v36_test_polar.png"
CUBE_PATH  = OUTDIR / "v36_test_3d.png"

print(f"📁 Speicherort: {OUTDIR.resolve()}\n")

# ============================================================
# 1. EINFACHE SIMULATION (v36-Parameter)
# ============================================================
np.random.seed(42)
net = pp.networks.case57()
net.load.p_mw *= 0.85
net.load.q_mvar *= 0.85

controlled = {"voltage": [], "coherence": [], "radius": [], "dist_elastic": [], "u": []}

for t in range(300):
    pp.runpp(net, enforce_q_lims=True)
    v_mean = np.mean(net.res_bus.vm_pu)
    coh = 1.0
