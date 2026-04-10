"""
v29_root_cube_navigation_controller.py
=======================================

NEXAH v29 – 5×17 Prime Trigger + Full Möbius Rotation
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp
from mpl_toolkits.mplot3d import Axes3D

OUTDIR = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
OUTDIR.mkdir(parents=True, exist_ok=True)

TS_PATH    = OUTDIR / "ieee57_v29_root_cube_timeseries.png"
POLAR_PATH = OUTDIR / "ieee57_v29_root_cube_polar.png"
CUBE_PATH  = OUTDIR / "ieee57_v29_root_cube_3d_projection.png"
REPORT_PATH= OUTDIR / "ieee57_v29_root_cube_report.txt"

print(f"📁 Saving to → {OUTDIR.resolve()}\n")

# ============================================================
# Settings (v29 – 5×17 Prime Trigger)
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

K_FLOW          = 0.265
FLOW_PHASE      = np.pi / 2 + 0.3
K_LIFT          = 0.36
K_AXIS_PULL     = 0.34
K_R_HOLD        = 0.13
K_SNAP          = 0.20
K_PULSE         = 0.18

BREATH_FREQ     = 0.112
BREATH_AMP      = 0.038
BREATH_TWIST    = 0.021

PRIME_NUDGE_AMP = 0.032
PRIME_BREAK     = 64
FIVE_SEVENTEEN_TRIGGER = 0.0085

NCS_LOCKS_DEG = [97.0, 277.0, 292.0]
NCS_LOCKS     = np.deg2rad(NCS_LOCKS_DEG)
SNAP_TOL      = np.deg2rad(3.0)

U_MAX = 0.15


def state_to_polar(x, y, cx=CENTER_X, cy=CENTER_Y):
    dx = x - cx
    dy = y - cy
    r = float(np.hypot(dx, dy))
    theta = float(np.arctan2(dy, dx))
    return r, theta

def state_to_root_cube(coherence, switch):
    r, theta = state_to_polar(coherence, switch)
    dist = abs(theta - ELASTIC_AXIS_ANGLE)
    if dist > np.pi:
        dist = 2 * np.pi - dist
    ncs_prox = float(np.exp(-8.0 * np.hypot(r - NCS_SWITCH_R, theta - NCS_SWITCH_THETA)))
    return {"r": r, "theta": theta, "dist_to_elastic": dist, "ncs_proximity": ncs_prox}

def is_enclosed_white_pattern(u_history):
    if len(u_history) < 30:
        return False
    recent = np.array(u_history[-30:])
    transitions = np.sum(np.abs(np.diff(np.sign(recent))) > 0)
    strong_blocks = np.sum(np.abs(recent) > 0.08)
    return transitions >= 14 and strong_blocks >= 20

def is_five_seventeen_trigger(u_mean):
    return abs(u_mean - FIVE_SEVENTEEN_TRIGGER) < 0.001

def choose_mode(r, theta, prev_mode, ncs_prox, escape_count, u_history, u_mean):
    if escape_count == PRIME_BREAK or is_enclosed_white_pattern(u_history) or is_five_seventeen_trigger(u_mean):
        return "gate_lock"
    if prev_mode == "gate_lock":
        if ncs_prox > 0.80: return "gate_lock"
        if r < 0.022: return "capture"
        return "band_hold"
    if prev_mode == "band_hold":
        if ncs_prox > 0.80: return "gate_lock"
        if r < 0.022: return "capture"
        return "band_hold"
    if r < 0.020: return "core_escape"
    if 0.026 <= r <= 0.040: return "band_hold"
    if r > 0.055: return "outer_return"
    return "capture"


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


def simulate_v29(time_steps=TIME_STEPS, seed=SEED):
    np.random.seed(seed)
    net = pp.networks.case57()
    base_p = net.load["p_mw"].copy()
    base_q = net.load.get("q_mvar", None)

    load_factor = 1.0 + 0.25 * np.sin(np.linspace(0, 6*np.pi, time_steps))
    noise = np.random.normal(0.0, 0.02, time_steps)

    voltage_mean, coherence, switch = [], [], []
    radius, theta, dist_elastic, ncs_prox = [], [], [], []
    u_hist, mode_hist, gate_score_hist = [], [], []
    escape_count = 0

    last_mode = "core_escape"
    last_coh = CENTER_X
    last_sw = CENTER_Y

    for t in range(time_steps):
        r_est, th_est = state_to_polar(last_coh, last_sw)
        cube = state_to_root_cube(last_coh, last_sw)

        gate_score = cube["ncs_proximity"]
        u_mean_recent = np.mean(u_hist[-20:]) if len(u_hist) > 20 else 0.0
        mode = choose_mode(r_est, th_est, last_mode, gate_score, escape_count, u_hist, u_mean_recent)

        breath_main = BREATH_AMP * np.sin(BREATH_FREQ * t)
        breath_twist = BREATH_TWIST * np.sin(2 * BREATH_FREQ * t)
        breath = breath_main + breath_twist

        nudge = PRIME_NUDGE_AMP * np.cos(BREATH_FREQ * t * 1.5)
        if escape_count == PRIME_BREAK or is_enclosed_white_pattern(u_hist) or is_five_seventeen_trigger(u_mean_recent):
            nudge *= 6.0

        u = 0.0
        if mode == "capture":
            u += K_LIFT * max(0.0, (R_CAPTURE_TARGET - r_est))
        elif mode in ["band_hold", "gate_lock"]:
            u += K_R_HOLD * (R_TARGET + breath - r_est)

            axis_factor = np.exp(-2.0 * cube["dist_to_elastic"])
            flow = -K_FLOW * axis_factor * np.sin(th_est - ELASTIC_AXIS_ANGLE + FLOW_PHASE)
            axis_pull = K_AXIS_PULL * (ELASTIC_AXIS_ANGLE - th_est)

            snap = K_SNAP * gate_score if gate_score > 0.80 else 0.0

            u += flow + axis_pull + snap + nudge

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

        if r > 0.055:
            escape_count += 1

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
        "escape_count": escape_count,
    }


# Run
baseline = simulate_baseline()
controlled = simulate_v29()

print("✅ v29 (5×17 Prime Trigger + Full Möbius Rotation) erfolgreich ausgeführt!")

# Plots + Report
t = np.arange(TIME_STEPS)

fig, axs = plt.subplots(5, 1, figsize=(14, 18), sharex=True)
axs[0].plot(t, baseline["voltage_mean"], alpha=0.4, label="Baseline")
axs[0].plot(t, controlled["voltage_mean"], label="v29 Controlled")
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

fig.suptitle("NEXAH v29 – Golden Scarabaeus Möbius Breathing Pulse + 5×17 Prime Trigger")
fig.tight_layout()
fig.savefig(TS_PATH, dpi=160)
plt.close(fig)

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='polar')
ax.plot(controlled["theta"], controlled["radius"], alpha=0.7, label="Controlled trajectory")
ax.scatter(controlled["theta"], controlled["radius"], c=controlled["gate_score"], cmap="viridis", s=30, label="Gate Score")
ax.set_title("Polar View – Root Cube Projection (v29)")
ax.legend()
fig.tight_layout()
fig.savefig(POLAR_PATH, dpi=160)
plt.close(fig)

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(controlled["radius"], controlled["theta"], controlled["dist_elastic"],
           c=controlled["gate_score"], cmap="plasma", s=40)
ax.set_xlabel("Radius")
ax.set_ylabel("Theta")
ax.set_zlabel("Dist to Elastic Axis")
ax.set_title("3D Root Cube Projection (v29)")
fig.tight_layout()
fig.savefig(CUBE_PATH, dpi=160)
plt.close(fig)

report = f"""NEXAH v29 Root Cube Navigation Report (5×17 Prime Trigger + Full Möbius Rotation)
========================================
Escape count: {controlled['escape_count']}
Mean coherence: {np.nanmean(controlled['coherence']):.4f}
Mean distance to Elastic Axis: {np.nanmean(controlled['dist_elastic']):.4f}
Max NCS proximity: {np.nanmax(controlled['ncs_proximity']):.4f}
Mean control signal: {np.nanmean(controlled['u']):.4f}
"""
REPORT_PATH.write_text(report, encoding="utf-8")

print(f"   • {TS_PATH.name}")
print(f"   • {POLAR_PATH.name}")
print(f"   • {CUBE_PATH.name}   ← 3D Root Cube View")
print(f"   • {REPORT_PATH.name}")
print("Fertig!")
