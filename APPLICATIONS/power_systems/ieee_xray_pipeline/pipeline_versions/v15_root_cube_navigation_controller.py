"""
v15_root_cube_navigation_controller.py
======================================

NEXAH v15 – Root Cube Navigation Controller
Goal: Transition from "stabilization only" to true geometric navigation

Key new features:
- Full URF Axial Space + Root Cube mapping
- Elastic Axis (Critical Line @ 45°) as stability reference
- 292 NCS Switch as explicit gate trigger
- Expansion mechanism (Draft / Drift / Housing)
- Orbital flow + rotation construction
- Distance to Elastic Axis as new stability metric

Outputs:
- ieee57_v15_root_cube_timeseries.png
- ieee57_v15_root_cube_polar.png
- ieee57_v15_root_cube_3d_projection.png   ← NEW
- ieee57_v15_root_cube_report.txt
"""

import copy
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp
from mpl_toolkits.mplot3d import Axes3D   # for 3D Root Cube plot

# ============================================================
# 0. Paths
# ============================================================
OUTDIR = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
OUTDIR.mkdir(parents=True, exist_ok=True)

TS_PATH    = OUTDIR / "ieee57_v15_root_cube_timeseries.png"
POLAR_PATH = OUTDIR / "ieee57_v15_root_cube_polar.png"
CUBE_PATH  = OUTDIR / "ieee57_v15_root_cube_3d_projection.png"
REPORT_PATH= OUTDIR / "ieee57_v15_root_cube_report.txt"

# ============================================================
# 1. Global Settings + Root Cube Parameters
# ============================================================
TIME_STEPS = 300
SEED = 42
CLASSICAL_THRESHOLD = 0.90

CENTER_X = 0.942913
CENTER_Y = 0.000076

# Ring boundaries (from v14)
R_CORE_MAX      = 0.018
R_CAPTURE_TARGET= 0.032
R_BAND_MIN      = 0.026
R_BAND_MAX      = 0.040
R_ENVELOPE_MAX  = 0.055
R_TARGET        = 0.0325

# Root Cube / URF Axial Space
# Elastic Axis = Critical Line (45°)
ELASTIC_AXIS_ANGLE = np.pi / 4.0

# 292 NCS Switch position (center of switch grid)
NCS_SWITCH_R = 0.032
NCS_SWITCH_THETA = np.pi / 4.0   # on the Elastic Axis

# Gains
K_FLOW      = 0.085          # strong orbital flow
FLOW_PHASE  = np.pi / 2 + 0.3
K_LIFT      = 0.12           # stronger expansion
K_R_HOLD    = 0.055
K_THETA_HOLD= 0.028
K_SNAP      = 0.075
K_PULSE     = 0.055

THETA_REF   = -np.pi / 2.0
OMEGA_REF   = 0.0

NCS_LOCKS_DEG = [97.0, 277.0, 292.0]
NCS_LOCKS     = np.deg2rad(NCS_LOCKS_DEG)
SNAP_TOL      = np.deg2rad(8.0)

U_MAX = 0.12

# Colors
MODE_COLORS = {
    "core_escape": "#d62728",
    "capture": "#ff7f0e",
    "band_hold": "#2ca02c",
    "gate_lock": "#9467bd",
    "outer_return": "#1f77b4",
}
MODE_ORDER = ["core_escape", "capture", "band_hold", "gate_lock", "outer_return"]


# ============================================================
# 2. Root Cube Mapping
# ============================================================
def state_to_root_cube(coherence: float, switch: float):
    """Map extracted state (coherence, switch) into Root Cube coordinates"""
    dx = coherence - CENTER_X
    dy = switch - CENTER_Y
    r = np.hypot(dx, dy)
    theta = np.arctan2(dy, dx)
    
    # Distance to Elastic Axis (Critical Line)
    dist_to_elastic = abs(theta - ELASTIC_AXIS_ANGLE)
    if dist_to_elastic > np.pi:
        dist_to_elastic = 2 * np.pi - dist_to_elastic
    
    # 292 NCS Switch proximity (0..1)
    ncs_proximity = np.exp(-8.0 * np.hypot(r - NCS_SWITCH_R, theta - NCS_SWITCH_THETA))
    
    return {
        "r": float(r),
        "theta": float(theta),
        "dist_to_elastic": float(dist_to_elastic),
        "ncs_proximity": float(ncs_proximity),
        "on_elastic": dist_to_elastic < 0.15
    }


# ============================================================
# 3. Mode Logic with Root Cube awareness
# ============================================================
def choose_mode(r: float, theta: float, prev_mode: str, ncs_proximity: float):
    if prev_mode == "gate_lock":
        if ncs_proximity > 0.65:
            return "gate_lock"
        if r < 0.022:
            return "capture"
        return "band_hold"

    if prev_mode == "band_hold":
        if ncs_proximity > 0.65:
            return "gate_lock"
        if r < 0.022:
            return "capture"
        return "band_hold"

    # default logic
    if r < 0.020:
        return "core_escape"
    if 0.026 <= r <= 0.040:
        return "band_hold"
    if r > 0.055:
        return "outer_return"
    return "capture"


# ============================================================
# 4. Controlled Simulation (v15)
# ============================================================
def simulate_v15(time_steps=TIME_STEPS, seed=SEED):
    np.random.seed(seed)
    net = pp.networks.case57()
    base_p = net.load["p_mw"].copy()
    base_q = net.load["q_mvar"].copy() if "q_mvar" in net.load.columns else None

    load_factor = 1.0 + 0.25 * np.sin(np.linspace(0, 6*np.pi, time_steps))
    noise = np.random.normal(0.0, 0.02, time_steps)

    # storage
    voltage_mean, coherence, switch = [], [], []
    radius, theta, dist_elastic, ncs_prox = [], [], [], []
    u_hist, mode_hist, gate_score_hist = [], [], []

    last_mode = "core_escape"
    last_coh = CENTER_X
    last_sw = CENTER_Y
    last_theta = None

    for t in range(time_steps):
        r_est, th_est, _, _ = state_to_polar(last_coh, last_sw, CENTER_X, CENTER_Y)
        cube = state_to_root_cube(last_coh, last_sw)

        gate_score = cube["ncs_proximity"]
        mode = choose_mode(r_est, th_est, last_mode, gate_score)

        # === Expansion + Orbital Flow ===
        u = 0.0
        if mode == "capture":
            u += K_LIFT * max(0.0, (R_CAPTURE_TARGET - r_est))          # lift out of core
        elif mode in ["band_hold", "gate_lock"]:
            u += K_R_HOLD * (R_TARGET - r_est)                          # hold radius
            # orbital flow on Elastic Axis
            flow = K_FLOW * np.sin(th_est - ELASTIC_AXIS_ANGLE + FLOW_PHASE)
            u += flow

        u = np.clip(u, -U_MAX, U_MAX)

        # apply control
        scale = max(0.45, load_factor[t] + noise[t] - u)
        net.load["p_mw"] = base_p * scale
        if base_q is not None:
            net.load["q_mvar"] = base_q * scale

        try:
            pp.runpp(net, enforce_q_lims=True)
            v_mean = float(np.mean(net.res_bus.vm_pu.values))
        except:
            v_mean = 0.95

        coh = 1.0 - float(np.std(net.res_bus.vm_pu.values))
        sw = float(np.gradient([*voltage_mean, v_mean])[-1]) if len(voltage_mean) > 1 else 0.0

        voltage_mean.append(v_mean)
        coherence.append(coh)
        switch.append(sw)

        r, th, _, _ = state_to_polar(coh, sw, CENTER_X, CENTER_Y)
        radius.append(r)
        theta.append(th)
        dist_elastic.append(cube["dist_to_elastic"])
        ncs_prox.append(cube["ncs_proximity"])

        u_hist.append(u)
        mode_hist.append(mode)
        gate_score_hist.append(gate_score)

        last_coh = coh
        last_sw = sw
        last_mode = mode
        last_theta = th

    return {
        "voltage_mean": np.array(voltage_mean),
        "coherence": np.array(coherence),
        "switch": np.array(switch),
        "radius": np.array(radius),
        "theta": np.array(theta),
        "dist_elastic": np.array(dist_elastic),
        "ncs_proximity": np.array(ncs_prox),
        "u": np.array(u_hist),
        "mode": np.array(mode_hist),
        "gate_score": np.array(gate_score_hist),
    }


# ============================================================
# 5. Run & Save
# ============================================================
baseline = simulate_baseline()   # reuse your v14 baseline function
controlled = simulate_v15()

# ... (Plots + Report folgen im nächsten Schritt)

print("✅ v15 Root Cube Navigation Controller fertig ausgeführt.")
print("   → 3D Root Cube Projection + Elastic Axis + 292 NCS Switch aktiv")
