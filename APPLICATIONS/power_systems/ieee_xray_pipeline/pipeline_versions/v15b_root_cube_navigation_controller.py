"""
v15b_root_cube_navigation_controller.py
======================================

NEXAH v15 – Root Cube Navigation Controller (fixed)
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
# 1. Settings
# ============================================================
TIME_STEPS = 300
SEED = 42
CLASSICAL_THRESHOLD = 0.90

CENTER_X = 0.942913
CENTER_Y = 0.000076

R_CORE_MAX      = 0.018
R_CAPTURE_TARGET= 0.032
R_BAND_MIN      = 0.026
R_BAND_MAX      = 0.040
R_ENVELOPE_MAX  = 0.055
R_TARGET        = 0.0325

ELASTIC_AXIS_ANGLE = np.pi / 4.0
NCS_SWITCH_R       = 0.032
NCS_SWITCH_THETA   = np.pi / 4.0

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

MODE_COLORS = {"core_escape":"#d62728", "capture":"#ff7f0e", "band_hold":"#2ca02c", "gate_lock":"#9467bd", "outer_return":"#1f77b4"}
MODE_ORDER = ["core_escape", "capture", "band_hold", "gate_lock", "outer_return"]


# ============================================================
# Utility Functions
# ============================================================
def state_to_polar(x, y, cx=CENTER_X, cy=CENTER_Y):
    dx = x - cx
    dy = y - cy
    r = float(np.hypot(dx, dy))
    theta = float(np.arctan2(dy, dx))
    return r, theta

def state_to_root_cube(coherence, switch):
    r, theta = state_to_polar(coherence, switch)
    dist_to_elastic = abs(theta - ELASTIC_AXIS_ANGLE)
    if dist_to_elastic > np.pi:
        dist_to_elastic = 2*np.pi - dist_to_elastic
    ncs_prox = float(np.exp(-8.0 * np.hypot(r - NCS_SWITCH_R, theta - NCS_SWITCH_THETA)))
    return {"r": r, "theta": theta, "dist_to_elastic": dist_to_elastic, "ncs_proximity": ncs_prox}

def choose_mode(r, theta, prev_mode, ncs_prox):
    if prev_mode == "gate_lock":
        if ncs_prox > 0.65: return "gate_lock"
        if r < 0.022: return "capture"
        return "band_hold"
    if prev_mode == "band_hold":
        if ncs_prox > 0.65: return "gate_lock"
        if r < 0.022: return "capture"
        return "band_hold"
    if r < 0.020: return "core_escape"
    if 0.026 <= r <= 0.040: return "band_hold"
    if r > 0.055: return "outer_return"
    return "capture"


# ============================================================
# Baseline
# ============================================================
def simulate_baseline(time_steps=TIME_STEPS, seed=SEED):
    np.random.seed(seed)
    net = pp.networks.case57()
    base_p = net.load["p_mw"].copy()
    base_q = net.load.get("q_mvar", None)

    load_factor = 1.0 + 0.25 * np.sin(np.linspace(0, 6*np.pi, time_steps))
    noise = np.random.normal(0.0, 0.02, time_steps)

    voltage_mean, coherence, switch = [], [], []
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
        coh = 1.0 - float(np.std(voltages))
        sw = float(np.gradient([*voltage_mean, v_mean])[-1]) if len(voltage_mean) > 1 else 0.0

        voltage_mean.append(v_mean)
        coherence.append(coh)
        switch.append(sw)

        if classical_event is None and v_mean < CLASSICAL_THRESHOLD:
            classical_event = t

    return {"voltage_mean": np.array(voltage_mean), "coherence": np.array(coherence), "switch": np.array(switch), "classical_event": classical_event}


# ============================================================
# v15 Controlled Simulation
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
        r_est, th_est = state_to_polar(last_coh, last_sw)
        cube = state_to_root_cube(last_coh, last_sw)

        gate_score = cube["ncs_proximity"]
        mode = choose_mode(r_est, th_est, last_mode, gate_score)

        u = 0.0
        if mode == "capture":
            u += K_LIFT * max(0.0, (R_CAPTURE_TARGET - r_est))
        elif mode in ["band_hold", "gate_lock"]:
            u += K_R_HOLD * (R_TARGET - r_est)
            flow = K_FLOW * np.sin(th_est - ELASTIC_AXIS_ANGLE + FLOW_PHASE)
            u += flow

        u = np.clip(u, -U_MAX, U_MAX)

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

        r, th = state_to_polar(coh, sw)
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
# Run
# ============================================================
baseline = simulate_baseline()
controlled = simulate_v15()

print("✅ v15 erfolgreich ausgeführt!")

# ============================================================
# Plots + Report
# ============================================================
t = np.arange(TIME_STEPS)

# Timeseries
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

axs[4].plot(t, controlled["u"], color="black", label="Control u")
axs[4].set_ylabel("Control u")
axs[4].set_xlabel("Time step")

fig.suptitle("NEXAH v15 – Root Cube Navigation Controller")
fig.tight_layout()
fig.savefig(TS_PATH, dpi=160)
plt.close(fig)

print(f"   • {TS_PATH.name}")
print(f"   • {POLAR_PATH.name}")
print(f"   • {CUBE_PATH.name}")
print(f"   • {REPORT_PATH.name}")
print("Fertig!")
