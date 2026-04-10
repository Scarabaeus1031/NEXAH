"""
v15_root_cube_navigation_controller.py
======================================

NEXAH v15 – Root Cube Navigation Controller
Goal: From stabilization → true geometric navigation using URF Axial Space

Features:
- Full Root Cube mapping
- Elastic Axis (Critical Line @ 45°) as reference
- 292 NCS Switch as gate trigger
- Expansion + orbital flow
- 3D projection plot

Results saved to: APPLICATIONS/power_systems/ieee_xray_pipeline/results/
"""

import copy
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp
from mpl_toolkits.mplot3d import Axes3D

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
# 1. Global Settings
# ============================================================
TIME_STEPS = 300
SEED = 42
CLASSICAL_THRESHOLD = 0.90

CENTER_X = 0.942913
CENTER_Y = 0.000076

# Ring boundaries
R_CORE_MAX      = 0.018
R_CAPTURE_TARGET= 0.032
R_BAND_MIN      = 0.026
R_BAND_MAX      = 0.040
R_ENVELOPE_MAX  = 0.055
R_TARGET        = 0.0325

# Root Cube Parameters
ELASTIC_AXIS_ANGLE = np.pi / 4.0
NCS_SWITCH_R       = 0.032
NCS_SWITCH_THETA   = np.pi / 4.0

# Gains
K_FLOW      = 0.085
FLOW_PHASE  = np.pi / 2 + 0.3
K_LIFT      = 0.12
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

MODE_COLORS = {
    "core_escape": "#d62728",
    "capture": "#ff7f0e",
    "band_hold": "#2ca02c",
    "gate_lock": "#9467bd",
    "outer_return": "#1f77b4",
}
MODE_ORDER = ["core_escape", "capture", "band_hold", "gate_lock", "outer_return"]


# ============================================================
# 2. Utility Functions
# ============================================================
def state_to_polar(x: float, y: float, cx: float, cy: float):
    dx = x - cx
    dy = y - cy
    r = float(np.hypot(dx, dy))
    theta = float(np.arctan2(dy, dx))
    return r, theta, dx, dy


def state_to_root_cube(coherence: float, switch: float):
    r, theta, _, _ = state_to_polar(coherence, switch, CENTER_X, CENTER_Y)
    
    dist_to_elastic = abs(theta - ELASTIC_AXIS_ANGLE)
    if dist_to_elastic > np.pi:
        dist_to_elastic = 2 * np.pi - dist_to_elastic
    
    ncs_proximity = float(np.exp(-8.0 * np.hypot(r - NCS_SWITCH_R, theta - NCS_SWITCH_THETA)))
    
    return {
        "r": r,
        "theta": theta,
        "dist_to_elastic": dist_to_elastic,
        "ncs_proximity": ncs_proximity,
        "on_elastic": dist_to_elastic < 0.15
    }


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

    if r < 0.020:
        return "core_escape"
    if 0.026 <= r <= 0.040:
        return "band_hold"
    if r > 0.055:
        return "outer_return"
    return "capture"


# ============================================================
# 3. Baseline Simulation
# ============================================================
def simulate_baseline(time_steps=TIME_STEPS, seed=SEED):
    np.random.seed(seed)
    net = pp.networks.case57()
    base_p = net.load["p_mw"].copy()
    base_q = net.load.get("q_mvar", None)

    load_factor = 1.0 + 0.25 * np.sin(np.linspace(0, 6*np.pi, time_steps))
    noise = np.random.normal(0.0, 0.02, time_steps)

    voltage_mean = []
    coherence = []
    switch = []
    classical_event = None

    for t in range(time_steps):
        scale = max(0.50, load_factor[t] + noise[t])
        net.load["p_mw"] = base_p * scale
        if base_q is not None:
            net.load["q_mvar"] = base_q * scale

        try:
            pp.runpp(net, enforce_q_lims=True)
            voltages = net.res_bus.vm_pu.values
        except:
            voltages = np.ones(len(net.bus)) * 0.95

        v_mean = float(np.mean(voltages))
        v_std = float(np.std(voltages))
        coh = 1.0 - v_std

        voltage_mean.append(v_mean)
        coherence.append(coh)

        sw = float(np.gradient(voltage_mean)[-1]) if len(voltage_mean) > 2 else 0.0
        switch.append(sw)

        if classical_event is None and v_mean < CLASSICAL_THRESHOLD:
            classical_event = t

    return {
        "voltage_mean": np.array(voltage_mean),
        "coherence": np.array(coherence),
        "switch": np.array(switch),
        "classical_event": classical_event,
    }


# ============================================================
# 4. v15 Root Cube Controlled Simulation
# ============================================================
def simulate_v15(time_steps=TIME_STEPS, seed=SEED):
    np.random.seed(seed)
    net = pp.networks.case57()
    base_p = net.load["p_mw"].copy()
    base_q = net.load.get("q_mvar", None)

    load_factor = 1.0 + 0.25 * np.sin(np.linspace(0, 6*np.pi, time_steps))
    noise = np.random.normal(0.0, 0.02, time_steps)

    voltage_mean, coherence, switch = [], [], []
    radius, theta, dist_elastic, ncs_prox = [], [], [], []
    u_hist, mode_hist, gate_score_hist = [], [], []

    last_mode = "core_escape"
    last_coh = CENTER_X
    last_sw = CENTER_Y

    for t in range(time_steps):
        r_est, th_est, _, _ = state_to_polar(last_coh, last_sw, CENTER_X, CENTER_Y)
        cube = state_to_root_cube(last_coh, last_sw)

        gate_score = cube["ncs_proximity"]
        mode = choose_mode(r_est, th_est, last_mode, gate_score)

        # Control signal
        u = 0.0
        if mode == "capture":
            u += K_LIFT * max(0.0, (R_CAPTURE_TARGET - r_est))
        elif mode in ["band_hold", "gate_lock"]:
            u += K_R_HOLD * (R_TARGET - r_est)
            flow = K_FLOW * np.sin(th_est - ELASTIC_AXIS_ANGLE + FLOW_PHASE)
            u += flow

        u = np.clip(u, -U_MAX, U_MAX)

        # Apply to grid
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
# 5. Run both simulations
# ============================================================
baseline = simulate_baseline()
controlled = simulate_v15()

print("✅ v15 Root Cube Navigation Controller erfolgreich ausgeführt!")
print(f"   Ergebnisse werden jetzt gespeichert in: {OUTDIR}")

# ============================================================
# 6. Plots + Report
# ============================================================
t = np.arange(TIME_STEPS)

# --- Timeseries ---
fig, axs = plt.subplots(5, 1, figsize=(14, 18), sharex=True)
axs[0].plot(t, baseline["voltage_mean"], alpha=0.4, label="Baseline")
axs[0].plot(t, controlled["voltage_mean"], label="v15 Controlled")
axs[0].axhline(CLASSICAL_THRESHOLD, color="gray", ls="--")
axs[0].set_ylabel("Voltage mean")
axs[0].legend()

axs[1].plot(t, controlled["coherence"], label="Coherence")
axs[1].set_ylabel("Coherence")

axs[2].plot(t, controlled["radius"], color="purple", label="Radius")
axs[2].axhline(R_BAND_MIN, color="green", ls="--", alpha=0.6)
axs[2].axhline(R_BAND_MAX, color="green", ls="--", alpha=0.6)
axs[2].set_ylabel("Radius")

axs[3].plot(t, controlled["dist_elastic"], color="orange", label="Dist to Elastic Axis")
axs[3].set_ylabel("Dist to Elastic Axis")

axs[4].plot(t, controlled["u"], color="black", label="Control signal u")
axs[4].set_ylabel("Control u")
axs[4].set_xlabel("Time step")

fig.suptitle("NEXAH v15 – Root Cube Navigation Controller")
fig.tight_layout()
fig.savefig(TS_PATH, dpi=160)
plt.close(fig)

# --- Polar ---
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='polar')
ax.plot(controlled["theta"], controlled["radius"], alpha=0.7, label="Controlled trajectory")
ax.scatter(controlled["theta"], controlled["radius"], c=controlled["gate_score"], cmap="viridis", s=30, label="Gate Score")
ax.set_title("Polar View – Root Cube Projection")
ax.legend()
fig.tight_layout()
fig.savefig(POLAR_PATH, dpi=160)
plt.close(fig)

# --- 3D Root Cube Projection ---
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(controlled["radius"], controlled["theta"], controlled["dist_elastic"],
           c=controlled["gate_score"], cmap="plasma", s=40)
ax.set_xlabel("Radius")
ax.set_ylabel("Theta")
ax.set_zlabel("Dist to Elastic Axis")
ax.set_title("3D Root Cube Projection (v15)")
fig.tight_layout()
fig.savefig(CUBE_PATH, dpi=160)
plt.close(fig)

# --- Report ---
report = f"""NEXAH v15 Root Cube Navigation Report
========================================
Escape count: {int(np.sum(controlled['radius'] > 0.055))}
Mean coherence: {np.mean(controlled['coherence']):.4f}
Mean distance to Elastic Axis: {np.mean(controlled['dist_elastic']):.4f}
Max NCS proximity: {np.max(controlled['ncs_proximity']):.4f}
Mean control signal: {np.mean(controlled['u']):.4f}
"""
REPORT_PATH.write_text(report, encoding="utf-8")

print(f"   • {TS_PATH.name}")
print(f"   • {POLAR_PATH.name}")
print(f"   • {CUBE_PATH.name}   ← 3D Root Cube View")
print(f"   • {REPORT_PATH.name}")
print("\nFertig!")
MODE_COLORS = {
    "core_escape": "#d62728",
    "capture": "#ff7f0e",
    "band_hold": "#2ca02c",
    "gate_lock": "#9467bd",
    "outer_return": "#1f77b4",
}
MODE_ORDER = ["core_escape", "capture", "band_hold", "gate_lock", "outer_return"]


# ============================================================
# 2. Utility Functions
# ============================================================
def state_to_polar(x: float, y: float, cx: float, cy: float):
    """Convert (coherence, switch) to polar coordinates"""
    dx = x - cx
    dy = y - cy
    r = float(np.hypot(dx, dy))
    theta = float(np.arctan2(dy, dx))
    return r, theta, dx, dy


def state_to_root_cube(coherence: float, switch: float):
    """Map extracted state into Root Cube coordinates"""
    r, theta, _, _ = state_to_polar(coherence, switch, CENTER_X, CENTER_Y)
    
    dist_to_elastic = abs(theta - ELASTIC_AXIS_ANGLE)
    if dist_to_elastic > np.pi:
        dist_to_elastic = 2 * np.pi - dist_to_elastic
    
    ncs_proximity = float(np.exp(-8.0 * np.hypot(r - NCS_SWITCH_R, theta - NCS_SWITCH_THETA)))
    
    return {
        "r": r,
        "theta": theta,
        "dist_to_elastic": dist_to_elastic,
        "ncs_proximity": ncs_proximity,
        "on_elastic": dist_to_elastic < 0.15
    }


# ============================================================
# 3. Mode Logic
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

    if r < 0.020:
        return "core_escape"
    if 0.026 <= r <= 0.040:
        return "band_hold"
    if r > 0.055:
        return "outer_return"
    return "capture"


# ============================================================
# 4. Baseline Simulation (v14)
# ============================================================
def simulate_baseline(time_steps=TIME_STEPS, seed=SEED):
    np.random.seed(seed)
    net = pp.networks.case57()
    base_p = net.load["p_mw"].copy()
    base_q = net.load.get("q_mvar", None)

    load_factor = 1.0 + 0.25 * np.sin(np.linspace(0, 6*np.pi, time_steps))
    noise = np.random.normal(0.0, 0.02, time_steps)

    voltage_mean = []
    coherence = []
    switch = []
    classical_event = None

    for t in range(time_steps):
        scale = max(0.50, load_factor[t] + noise[t])
        net.load["p_mw"] = base_p * scale
        if base_q is not None:
            net.load["q_mvar"] = base_q * scale

        try:
            pp.runpp(net, enforce_q_lims=True)
            voltages = net.res_bus.vm_pu.values
        except:
            voltages = np.ones(len(net.bus)) * 0.95

        v_mean = float(np.mean(voltages))
        v_std = float(np.std(voltages))
        coh = 1.0 - v_std

        voltage_mean.append(v_mean)
        coherence.append(coh)

        sw = float(np.gradient(voltage_mean)[-1]) if len(voltage_mean) > 2 else 0.0
        switch.append(sw)

        if classical_event is None and v_mean < CLASSICAL_THRESHOLD:
            classical_event = t

    return {
        "voltage_mean": np.array(voltage_mean),
        "coherence": np.array(coherence),
        "switch": np.array(switch),
        "classical_event": classical_event,
    }


# ============================================================
# 5. v15 Root Cube Controlled Simulation
# ============================================================
def simulate_v15(time_steps=TIME_STEPS, seed=SEED):
    np.random.seed(seed)
    net = pp.networks.case57()
    base_p = net.load["p_mw"].copy()
    base_q = net.load.get("q_mvar", None)

    load_factor = 1.0 + 0.25 * np.sin(np.linspace(0, 6*np.pi, time_steps))
    noise = np.random.normal(0.0, 0.02, time_steps)

    voltage_mean, coherence, switch = [], [], []
    radius, theta, dist_elastic, ncs_prox = [], [], [], []
    u_hist, mode_hist, gate_score_hist = [], [], []

    last_mode = "core_escape"
    last_coh = CENTER_X
    last_sw = CENTER_Y

    for t in range(time_steps):
        r_est, th_est, _, _ = state_to_polar(last_coh, last_sw, CENTER_X, CENTER_Y)
        cube = state_to_root_cube(last_coh, last_sw)

        gate_score = cube["ncs_proximity"]
        mode = choose_mode(r_est, th_est, last_mode, gate_score)

        # Control signal
        u = 0.0
        if mode == "capture":
            u += K_LIFT * max(0.0, (R_CAPTURE_TARGET - r_est))
        elif mode in ["band_hold", "gate_lock"]:
            u += K_R_HOLD * (R_TARGET - r_est)
            flow = K_FLOW * np.sin(th_est - ELASTIC_AXIS_ANGLE + FLOW_PHASE)
            u += flow

        u = np.clip(u, -U_MAX, U_MAX)

        # Apply to grid
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
# 6. Run
# ============================================================
baseline = simulate_baseline()
controlled = simulate_v15()

print("✅ v15 Root Cube Navigation Controller erfolgreich ausgeführt!")
print(f"   Alle Ergebnisse liegen in: {OUTDIR}")
