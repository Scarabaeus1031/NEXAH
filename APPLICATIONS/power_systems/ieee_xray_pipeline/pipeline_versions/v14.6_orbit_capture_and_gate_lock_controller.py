"""
v14.6_orbit_capture_and_gate_lock_controller.py
===============================================

Goal
----
Move from "stabilization only" toward a true two-stage NEXAH controller:

1. Orbit capture
   - lift the trajectory out of the inner core
   - guide it toward a working orbital region

2. Gate lock
   - once the orbit band is reached, allow phase-aware gate engagement
   - apply pulse / snap logic only when the trajectory is actually near the ring

This is still a prototype controller in the extracted NEXAH state space:
    x = coherence
    y = switch signal

It does NOT yet claim physical optimality.
It is an architecture test for mode-based control.

Outputs
-------
- ieee57_v14_6_orbit_capture_timeseries.png
- ieee57_v14_6_orbit_capture_phase.png
- ieee57_v14_6_orbit_capture_polar.png
- ieee57_v14_6_orbit_capture_report.txt
"""

import copy
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp


# ============================================================
# 0. Paths
# ============================================================

OUTDIR = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
OUTDIR.mkdir(parents=True, exist_ok=True)

TS_PATH = OUTDIR / "ieee57_v14_6_orbit_capture_timeseries.png"
PHASE_PATH = OUTDIR / "ieee57_v14_6_orbit_capture_phase.png"
POLAR_PATH = OUTDIR / "ieee57_v14_6_orbit_capture_polar.png"
REPORT_PATH = OUTDIR / "ieee57_v14_6_orbit_capture_report.txt"


# ============================================================
# 1. Global settings
# ============================================================

TIME_STEPS = 300
SEED = 42
CLASSICAL_THRESHOLD = 0.90

# Stable center from prior runs
CENTER_X = 0.942913
CENTER_Y = 0.000076

# Mode boundaries / rings
R_CORE_MAX = 0.018
R_CAPTURE_TARGET = 0.032
R_CAPTURE_MIN = 0.020
R_BAND_MIN = 0.026
R_BAND_MAX = 0.040
R_HOLD_EXIT = 0.023
R_ENVELOPE_MAX = 0.055

# Ring center used for hold mode
R_TARGET = 0.0325
R_BAND_HALF = 0.0075

# Phase references
THETA_REF = -np.pi / 2.0
THETA_TOL = np.deg2rad(12.61)

OMEGA_REF = 0.0
OMEGA_TOL = 0.060

# NCS locks
NCS_LOCKS_DEG = [97.0, 277.0, 292.0]
NCS_LOCKS = np.deg2rad(NCS_LOCKS_DEG)
SNAP_TOL = np.deg2rad(8.0)

# Capture / hold / gate gains
K_LIFT = 0.080
K_R_CAPTURE = 0.060
K_R_HOLD = 0.050
K_R_RETURN = 0.070

K_THETA_CAPTURE = 0.010
K_THETA_HOLD = 0.025
K_OMEGA = 0.020

K_SWITCH_DAMP = 0.100
K_COH_BOOST = 0.050

K_SNAP = 0.060
K_PULSE = 0.040

# Breathing
BREATH_PERIOD = 96
BREATH_PHASE = 0.0
BREATH_AMP_CAPTURE = 0.010
BREATH_AMP_HOLD = 0.025

# Gate score weights
W_R = 0.40
W_THETA = 0.40
W_OMEGA = 0.20

# Actuation
U_MAX = 0.10
BASE_GLOBAL_LOAD_SCALE = 1.0

# Escape region proxy in extracted space
ESCAPE_RADIUS = 0.040

# Colors for modes
MODE_COLORS = {
    "core_escape": "#d62728",
    "capture": "#ff7f0e",
    "band_hold": "#2ca02c",
    "gate_lock": "#9467bd",
    "outer_return": "#1f77b4",
}

MODE_ORDER = ["core_escape", "capture", "band_hold", "gate_lock", "outer_return"]


# ============================================================
# 2. Utility functions
# ============================================================

def wrap_angle(theta: float) -> float:
    return (theta + np.pi) % (2.0 * np.pi) - np.pi


def min_angle_to_locks(theta: float, locks: np.ndarray) -> float:
    return min(abs(wrap_angle(theta - lock)) for lock in locks)


def nearest_lock(theta: float, locks: np.ndarray) -> float:
    dists = [abs(wrap_angle(theta - lock)) for lock in locks]
    return float(locks[int(np.argmin(dists))])


def state_to_polar(x: float, y: float, cx: float, cy: float):
    dx = x - cx
    dy = y - cy
    r = float(np.hypot(dx, dy))
    theta = float(np.arctan2(dy, dx))
    return r, theta, dx, dy


def breathing_target(mode: str, t: int, theta: float) -> float:
    if mode == "capture":
        amp = BREATH_AMP_CAPTURE
        base = R_CAPTURE_TARGET
    elif mode in ["band_hold", "gate_lock"]:
        amp = BREATH_AMP_HOLD
        base = R_TARGET
    else:
        amp = 0.0
        base = R_CAPTURE_TARGET

    breath_t = np.sin(2.0 * np.pi * t / BREATH_PERIOD + BREATH_PHASE)
    breath_theta = np.sin(theta)
    return base * (1.0 + amp * (0.65 * breath_t + 0.35 * breath_theta))


def pulse_weight(theta: float, locks: np.ndarray, sharpness: float = 18.0) -> float:
    d = min_angle_to_locks(theta, locks)
    return float(np.exp(-sharpness * d))


def clip(x: float, lo: float, hi: float) -> float:
    return float(np.clip(x, lo, hi))


def compute_gate_score(r: float, theta: float, omega: float):
    # radial proximity to target band center
    radial_term = max(0.0, 1.0 - abs(r - R_TARGET) / max(R_BAND_HALF, 1e-9))

    # phase proximity to nearest lock
    d_theta = min_angle_to_locks(theta, NCS_LOCKS)
    phase_term = max(0.0, 1.0 - d_theta / max(SNAP_TOL, 1e-9))

    # omega proximity
    omega_term = max(0.0, 1.0 - abs(omega - OMEGA_REF) / max(OMEGA_TOL, 1e-9))

    score = W_R * radial_term + W_THETA * phase_term + W_OMEGA * omega_term
    return float(np.clip(score, 0.0, 1.0)), radial_term, phase_term, omega_term


def choose_mode(r: float, prev_mode: str, gate_score: float) -> str:
    """
    Hysteretic mode logic.
    """

    if prev_mode == "gate_lock":
        if (R_BAND_MIN <= r <= R_BAND_MAX) and gate_score > 0.65:
            return "gate_lock"
        if r < R_HOLD_EXIT:
            return "capture"
        if r > R_ENVELOPE_MAX:
            return "outer_return"
        return "band_hold"

    if prev_mode == "band_hold":
        if r < R_HOLD_EXIT:
            return "capture"
        if r > R_ENVELOPE_MAX:
            return "outer_return"
        if (R_BAND_MIN <= r <= R_BAND_MAX) and gate_score > 0.85:
            return "gate_lock"
        return "band_hold"

    if prev_mode == "capture":
        if r < R_CORE_MAX:
            return "core_escape"
        if R_BAND_MIN <= r <= R_BAND_MAX:
            return "band_hold"
        if r > R_ENVELOPE_MAX:
            return "outer_return"
        return "capture"

    if prev_mode == "outer_return":
        if r > R_ENVELOPE_MAX:
            return "outer_return"
        if R_BAND_MIN <= r <= R_BAND_MAX:
            return "band_hold"
        if r < R_CORE_MAX:
            return "core_escape"
        return "capture"

    # default / core_escape
    if r < R_CAPTURE_MIN:
        return "core_escape"
    if R_BAND_MIN <= r <= R_BAND_MAX:
        return "band_hold"
    if r > R_ENVELOPE_MAX:
        return "outer_return"
    return "capture"


# ============================================================
# 3. Baseline simulation
# ============================================================

def simulate_baseline(time_steps: int = TIME_STEPS, seed: int = SEED):
    np.random.seed(seed)

    net = pp.networks.case57()
    base_p = net.load["p_mw"].copy()
    base_q = net.load["q_mvar"].copy() if "q_mvar" in net.load.columns else None

    load_factor = 1.0 + 0.25 * np.sin(np.linspace(0, 6 * np.pi, time_steps))
    noise = np.random.normal(0.0, 0.02, time_steps)

    voltage_mean = []
    coherence = []
    switch = []
    theta = []
    radius = []
    omega = []

    classical_event = None
    last_theta = None

    for t in range(time_steps):
        scale = max(0.50, load_factor[t] + noise[t])

        net.load["p_mw"] = base_p * scale
        if base_q is not None:
            net.load["q_mvar"] = base_q * scale

        try:
            pp.runpp(net, enforce_q_lims=True)
            voltages = net.res_bus.vm_pu.values
        except Exception:
            voltages = np.ones(len(net.bus)) * 0.95

        v_mean = float(np.mean(voltages))
        v_std = float(np.std(voltages))
        coh = 1.0 - v_std

        voltage_mean.append(v_mean)
        coherence.append(coh)

        if len(voltage_mean) > 2:
            sw = float(np.gradient(voltage_mean)[-1])
        else:
            sw = 0.0
        switch.append(sw)

        r, th, _, _ = state_to_polar(coh, sw, CENTER_X, CENTER_Y)
        radius.append(r)
        theta.append(th)

        if last_theta is None:
            omg = 0.0
        else:
            omg = wrap_angle(th - last_theta)
        omega.append(omg)
        last_theta = th

        if classical_event is None and v_mean < CLASSICAL_THRESHOLD:
            classical_event = t

    return {
        "voltage_mean": np.array(voltage_mean),
        "coherence": np.array(coherence),
        "switch": np.array(switch),
        "theta": np.array(theta),
        "radius": np.array(radius),
        "omega": np.array(omega),
        "classical_event": classical_event,
    }


# ============================================================
# 4. Controlled simulation
# ============================================================

def simulate_controlled(time_steps: int = TIME_STEPS, seed: int = SEED):
    np.random.seed(seed)

    net = pp.networks.case57()
    base_p = net.load["p_mw"].copy()
    base_q = net.load["q_mvar"].copy() if "q_mvar" in net.load.columns else None

    load_factor = 1.0 + 0.25 * np.sin(np.linspace(0, 6 * np.pi, time_steps))
    noise = np.random.normal(0.0, 0.02, time_steps)

    voltage_mean = []
    coherence = []
    switch = []
    theta = []
    radius = []
    omega = []

    u_hist = []
    mode_hist = []
    gate_score_hist = []
    radial_gate_hist = []
    phase_gate_hist = []
    omega_gate_hist = []

    r_target_hist = []
    theta_err_hist = []
    pulse_hist = []
    snap_hist = []
    lift_hist = []

    classical_event = None
    last_theta = None
    last_mode = "core_escape"

    last_coh = CENTER_X
    last_sw = CENTER_Y

    for t in range(time_steps):
        # estimate prior state
        r_est, th_est, _, _ = state_to_polar(last_coh, last_sw, CENTER_X, CENTER_Y)

        if last_theta is None:
            omg_est = 0.0
        else:
            omg_est = wrap_angle(th_est - last_theta)

        gate_score, g_r, g_th, g_om = compute_gate_score(r_est, th_est, omg_est)
        mode = choose_mode(r_est, last_mode, gate_score)

        gate_score_hist.append(gate_score)
        radial_gate_hist.append(g_r)
        phase_gate_hist.append(g_th)
        omega_gate_hist.append(g_om)
        mode_hist.append(mode)

        r_tar = breathing_target(mode, t, th_est)
        r_target_hist.append(r_tar)

        theta_err = wrap_angle(THETA_REF - th_est)
        theta_err_hist.append(theta_err)

        # =========================
        # Mode-specific control
        # =========================
        u = 0.0
        pulse = 0.0
        snap = 0.0
        lift = 0.0

        # global helper terms
        u_switch = -K_SWITCH_DAMP * last_sw
        u_coh = K_COH_BOOST * (CENTER_X - last_coh)
        u_omega = -K_OMEGA * (omg_est - OMEGA_REF)

        if mode == "core_escape":
            # strong outward lift from the core
            lift = K_LIFT * max(0.0, (R_CAPTURE_TARGET - r_est))
            lift = clip(lift, 0.0, 0.060)

            u += lift
            u += 0.6 * u_switch
            u += 0.5 * u_coh

        elif mode == "capture":
            u += K_R_CAPTURE * (r_tar - r_est)
            u += K_THETA_CAPTURE * theta_err
            u += 0.8 * u_omega
            u += 0.6 * u_switch
            u += 0.6 * u_coh

        elif mode == "band_hold":
            u += K_R_HOLD * (r_tar - r_est)
            u += K_THETA_HOLD * theta_err
            u += u_omega
            u += 0.8 * u_switch
            u += 0.5 * u_coh

        elif mode == "gate_lock":
            ang_weight = pulse_weight(th_est, NCS_LOCKS, sharpness=18.0)
            pulse = K_PULSE * ang_weight * np.sign(theta_err if abs(theta_err) > 1e-9 else 1.0)

            nearest = nearest_lock(th_est, NCS_LOCKS)
            snap = K_SNAP * wrap_angle(nearest - th_est)

            u += K_R_HOLD * (r_tar - r_est)
            u += 1.2 * K_THETA_HOLD * theta_err
            u += 0.8 * u_omega
            u += 0.8 * u_switch
            u += pulse
            u += snap

        elif mode == "outer_return":
            # bring system back from envelope region
            u += -K_R_RETURN * max(0.0, (r_est - R_TARGET))
            u += 0.6 * K_THETA_HOLD * theta_err
            u += u_omega
            u += u_switch
            u += 0.4 * u_coh

        # clip total actuation
        u = clip(u, -U_MAX, U_MAX)

        u_hist.append(u)
        pulse_hist.append(pulse)
        snap_hist.append(snap)
        lift_hist.append(lift)

        # load actuation
        base_scale = max(0.50, load_factor[t] + noise[t] - u)
        scale = clip(base_scale, 0.45, 1.45)

        net.load["p_mw"] = base_p * scale
        if base_q is not None:
            net.load["q_mvar"] = base_q * scale

        try:
            pp.runpp(net, enforce_q_lims=True)
            voltages = net.res_bus.vm_pu.values
        except Exception:
            voltages = np.ones(len(net.bus)) * 0.95

        v_mean = float(np.mean(voltages))
        v_std = float(np.std(voltages))
        coh = 1.0 - v_std

        voltage_mean.append(v_mean)
        coherence.append(coh)

        if len(voltage_mean) > 2:
            sw = float(np.gradient(voltage_mean)[-1])
        else:
            sw = 0.0
        switch.append(sw)

        r, th, _, _ = state_to_polar(coh, sw, CENTER_X, CENTER_Y)
        radius.append(r)
        theta.append(th)

        if last_theta is None:
            omg = 0.0
        else:
            omg = wrap_angle(th - last_theta)
        omega.append(omg)

        last_theta = th
        last_coh = coh
        last_sw = sw
        last_mode = mode

        if classical_event is None and v_mean < CLASSICAL_THRESHOLD:
            classical_event = t

    return {
        "voltage_mean": np.array(voltage_mean),
        "coherence": np.array(coherence),
        "switch": np.array(switch),
        "theta": np.array(theta),
        "radius": np.array(radius),
        "omega": np.array(omega),
        "u": np.array(u_hist),
        "mode": np.array(mode_hist, dtype=object),
        "gate_score": np.array(gate_score_hist),
        "gate_r": np.array(radial_gate_hist),
        "gate_theta": np.array(phase_gate_hist),
        "gate_omega": np.array(omega_gate_hist),
        "r_target": np.array(r_target_hist),
        "theta_err": np.array(theta_err_hist),
        "pulse": np.array(pulse_hist),
        "snap": np.array(snap_hist),
        "lift": np.array(lift_hist),
        "classical_event": classical_event,
    }


# ============================================================
# 5. Run simulations
# ============================================================

baseline = simulate_baseline()
controlled = simulate_controlled()

t = np.arange(TIME_STEPS)


# ============================================================
# 6. Metrics
# ============================================================

baseline_escape = baseline["radius"] > ESCAPE_RADIUS
controlled_escape = controlled["radius"] > ESCAPE_RADIUS

snap_count = int(np.sum(np.abs(controlled["snap"]) > 1e-9))
pulse_count = int(np.sum(np.abs(controlled["pulse"]) > 1e-9))
lift_count = int(np.sum(np.abs(controlled["lift"]) > 1e-9))
control_activation_count = int(np.sum(np.abs(controlled["u"]) > 1e-9))

time_in_band = int(np.sum((controlled["radius"] >= R_BAND_MIN) & (controlled["radius"] <= R_BAND_MAX)))
time_near_gate = int(np.sum(controlled["gate_score"] > 0.65))
reentry_count = int(np.sum((controlled["mode"][:-1] == "band_hold") & (controlled["mode"][1:] == "capture")))
orbit_capture_time = None
band_hits = np.where((controlled["radius"] >= R_BAND_MIN) & (controlled["radius"] <= R_BAND_MAX))[0]
if len(band_hits) > 0:
    orbit_capture_time = int(band_hits[0])

report_lines = []
report_lines.append("===== NEXAH V14.6 ORBIT CAPTURE + GATE LOCK REPORT =====")
report_lines.append("")
report_lines.append("Stability center:")
report_lines.append(f"  coherence = {CENTER_X:.6f}")
report_lines.append(f"  switch    = {CENTER_Y:.6f}")
report_lines.append("")
report_lines.append("Mode boundaries:")
report_lines.append(f"  R_CORE_MAX      = {R_CORE_MAX:.6f}")
report_lines.append(f"  R_CAPTURE_TARGET= {R_CAPTURE_TARGET:.6f}")
report_lines.append(f"  R_CAPTURE_MIN   = {R_CAPTURE_MIN:.6f}")
report_lines.append(f"  R_BAND_MIN      = {R_BAND_MIN:.6f}")
report_lines.append(f"  R_BAND_MAX      = {R_BAND_MAX:.6f}")
report_lines.append(f"  R_HOLD_EXIT     = {R_HOLD_EXIT:.6f}")
report_lines.append(f"  R_ENVELOPE_MAX  = {R_ENVELOPE_MAX:.6f}")
report_lines.append("")
report_lines.append(f"Ring target center: {R_TARGET:.6f}")
report_lines.append(f"Ring half width:    {R_BAND_HALF:.6f}")
report_lines.append("")
report_lines.append(f"Theta reference: {THETA_REF:.6f} rad ({np.degrees(THETA_REF):.2f} deg)")
report_lines.append(f"Theta tolerance: {THETA_TOL:.6f} rad ({np.degrees(THETA_TOL):.2f} deg)")
report_lines.append(f"Omega reference: {OMEGA_REF:.6f}")
report_lines.append(f"Omega tolerance: {OMEGA_TOL:.6f}")
report_lines.append(f"NCS phase locks (deg): {NCS_LOCKS_DEG}")
report_lines.append(f"Phase snap tolerance: {SNAP_TOL:.6f} rad ({np.degrees(SNAP_TOL):.2f} deg)")
report_lines.append("")
report_lines.append(f"Baseline mean radius: {np.mean(baseline['radius']):.6f}")
report_lines.append(f"Controlled mean radius: {np.mean(controlled['radius']):.6f}")
report_lines.append("")
report_lines.append(f"Baseline max radius: {np.max(baseline['radius']):.6f}")
report_lines.append(f"Controlled max radius: {np.max(controlled['radius']):.6f}")
report_lines.append("")
report_lines.append(f"Baseline mean coherence: {np.mean(baseline['coherence']):.6f}")
report_lines.append(f"Controlled mean coherence: {np.mean(controlled['coherence']):.6f}")
report_lines.append("")
report_lines.append(f"Baseline first classical event: {baseline['classical_event']}")
report_lines.append(f"Controlled first classical event: {controlled['classical_event']}")
if baseline["classical_event"] is not None and controlled["classical_event"] is not None:
    report_lines.append(
        f"Collapse shift (controlled - baseline): "
        f"{controlled['classical_event'] - baseline['classical_event']}"
    )
report_lines.append("")
report_lines.append(f"Baseline escape count: {int(np.sum(baseline_escape))}")
report_lines.append(f"Controlled escape count: {int(np.sum(controlled_escape))}")
report_lines.append(f"Escape delta (baseline - controlled): {int(np.sum(baseline_escape) - np.sum(controlled_escape))}")
report_lines.append("")
report_lines.append(f"Pulse activation count: {pulse_count}")
report_lines.append(f"Snap activation count: {snap_count}")
report_lines.append(f"Lift activation count: {lift_count}")
report_lines.append(f"Control activation count: {control_activation_count}")
report_lines.append(f"Mean control signal: {np.mean(controlled['u']):.6f}")
report_lines.append(f"Max |control signal|: {np.max(np.abs(controlled['u'])):.6f}")
report_lines.append("")
report_lines.append(f"Time in band: {time_in_band}")
report_lines.append(f"Time near gate (score > 0.65): {time_near_gate}")
report_lines.append(f"Reentry count: {reentry_count}")
report_lines.append(f"Orbit capture time: {orbit_capture_time}")
report_lines.append("")
for mode in MODE_ORDER:
    report_lines.append(f"Mode count [{mode}]: {int(np.sum(controlled['mode'] == mode))}")
report_lines.append("")
report_lines.append(
    "Mean coherence improved." if np.mean(controlled["coherence"]) > np.mean(baseline["coherence"])
    else "Mean coherence did not improve."
)
report_lines.append(
    "Maximum orbit excursion improved." if np.max(controlled["radius"]) < np.max(baseline["radius"])
    else "Maximum orbit excursion did not improve."
)
report_lines.append(
    "Escape count reduced." if np.sum(controlled_escape) < np.sum(baseline_escape)
    else "Escape count did not reduce."
)
report_lines.append(
    "Discrete NCS lock engagement occurred." if snap_count > 0
    else "Discrete NCS lock engagement did not occur."
)

report_text = "\n".join(report_lines)
print(report_text)
REPORT_PATH.write_text(report_text, encoding="utf-8")


# ============================================================
# 7. Plot helpers
# ============================================================

def mode_to_int(mode_array):
    return np.array([MODE_ORDER.index(m) if m in MODE_ORDER else -1 for m in mode_array])


# ============================================================
# 8. Plots
# ============================================================

# ---------- Time series ----------
fig, axs = plt.subplots(7, 1, figsize=(14, 24), sharex=True)

axs[0].plot(t, baseline["voltage_mean"], label="Baseline", alpha=0.35)
axs[0].plot(t, controlled["voltage_mean"], label="Controlled")
axs[0].axhline(CLASSICAL_THRESHOLD, color="gray", linestyle="--", label="Classical threshold")
axs[0].set_ylabel("Voltage mean")
axs[0].legend()

axs[1].plot(t, baseline["coherence"], alpha=0.35)
axs[1].plot(t, controlled["coherence"])
axs[1].set_ylabel("Coherence")

axs[2].plot(t, baseline["switch"], alpha=0.35)
axs[2].plot(t, controlled["switch"])
axs[2].axhline(0.0, color="gray", linestyle="--")
axs[2].set_ylabel("Switch")

axs[3].plot(t, controlled["radius"], color="purple", label="Controlled radius")
axs[3].plot(t, controlled["r_target"], color="black", linestyle=":", label="Dynamic target")
axs[3].axhline(R_CAPTURE_TARGET, color="orange", linestyle="--", alpha=0.5, label="Capture target")
axs[3].axhline(R_BAND_MIN, color="green", linestyle="--", alpha=0.6, label="Band")
axs[3].axhline(R_BAND_MAX, color="green", linestyle="--", alpha=0.6)
axs[3].axhline(R_ENVELOPE_MAX, color="blue", linestyle="--", alpha=0.5, label="Envelope")
axs[3].set_ylabel("Radius")
axs[3].legend()

axs[4].plot(t, controlled["theta_err"], color="red", label="Theta err")
axs[4].axhline(THETA_TOL, color="gray", linestyle="--")
axs[4].axhline(-THETA_TOL, color="gray", linestyle="--")
axs[4].set_ylabel("Theta err")
axs[4].legend()

axs[5].plot(t, controlled["gate_score"], color="brown", label="Gate score")
axs[5].axhline(0.65, color="gray", linestyle="--", label="Near gate")
axs[5].axhline(0.85, color="black", linestyle="--", label="Gate lock threshold")
axs[5].set_ylabel("Gate score")
axs[5].legend()

axs[6].plot(t, controlled["u"], color="black", label="Control signal")
axs[6].plot(t, controlled["pulse"], color="red", alpha=0.7, label="Pulse")
axs[6].plot(t, controlled["snap"], color="purple", alpha=0.7, label="Snap")
axs[6].plot(t, controlled["lift"], color="green", alpha=0.7, label="Lift")
axs[6].set_ylabel("u(t)")
axs[6].set_xlabel("Time step")
axs[6].legend()

# mode strip overlay on last axis
mode_int = mode_to_int(controlled["mode"])
axs[6].imshow(
    mode_int[np.newaxis, :],
    aspect="auto",
    extent=[0, TIME_STEPS - 1, np.min(controlled["u"]) - 0.02, np.min(controlled["u"]) - 0.01],
    cmap="tab10",
    alpha=0.85,
)

fig.suptitle("NEXAH v14.6 — Orbit Capture + Gate Lock Controller (Time Series)", fontsize=18)
fig.tight_layout()
fig.savefig(TS_PATH, dpi=160)
plt.close(fig)


# ---------- Phase space ----------
fig, ax = plt.subplots(figsize=(14, 10))

ax.plot(baseline["coherence"], baseline["switch"], alpha=0.25, linewidth=3, label="Baseline trajectory")

for mode in MODE_ORDER:
    mask = controlled["mode"] == mode
    if np.any(mask):
        ax.scatter(
            controlled["coherence"][mask],
            controlled["switch"][mask],
            s=70,
            c=MODE_COLORS[mode],
            alpha=0.75,
            label=mode
        )

ax.scatter(
    baseline["coherence"][baseline_escape],
    baseline["switch"][baseline_escape],
    s=180, facecolors="none", edgecolors="tab:blue", linewidths=2.0, label="Baseline escape region"
)
ax.scatter(
    controlled["coherence"][controlled_escape],
    controlled["switch"][controlled_escape],
    s=180, facecolors="none", edgecolors="tab:orange", linewidths=2.0, label="Controlled escape region"
)

ax.scatter(CENTER_X, CENTER_Y, marker="*", s=380, color="gold", label="Stability center")
ax.scatter(baseline["coherence"][0], baseline["switch"][0], s=220, color="green", label="Start")
ax.scatter(baseline["coherence"][-1], baseline["switch"][-1], s=220, color="red", label="Baseline end")

ax.axhline(0.0, color="gray", linestyle="--", alpha=0.5)
ax.axvline(CENTER_X, color="gray", linestyle="--", alpha=0.5)

ax.set_xlabel("Coherence")
ax.set_ylabel("Switch signal")
ax.set_title("NEXAH v14.6 — Orbit Capture + Gate Lock Controller (Phase Space)")
ax.legend(loc="upper left", ncol=2)
ax.grid(True, alpha=0.25)
fig.tight_layout()
fig.savefig(PHASE_PATH, dpi=160)
plt.close(fig)


# ---------- Polar ----------
fig = plt.figure(figsize=(14, 12))
ax = fig.add_subplot(111, projection="polar")

ax.plot(baseline["theta"], baseline["radius"], alpha=0.25, linewidth=3, label="Baseline")

for mode in MODE_ORDER:
    mask = controlled["mode"] == mode
    if np.any(mask):
        ax.scatter(
            controlled["theta"][mask],
            controlled["radius"][mask],
            s=80,
            c=MODE_COLORS[mode],
            alpha=0.75,
            label=mode
        )

theta_grid = np.linspace(-np.pi, np.pi, 400)
ax.plot(theta_grid, np.full_like(theta_grid, R_CAPTURE_TARGET), color="orange", linestyle="--", alpha=0.6, label="Capture ring")
ax.plot(theta_grid, np.full_like(theta_grid, R_BAND_MIN), color="green", linestyle="--", alpha=0.8, label="Band")
ax.plot(theta_grid, np.full_like(theta_grid, R_BAND_MAX), color="green", linestyle="--", alpha=0.8)
ax.plot(theta_grid, np.full_like(theta_grid, R_ENVELOPE_MAX), color="blue", linestyle="--", alpha=0.6, label="Envelope")
ax.plot([THETA_REF, THETA_REF], [0, max(R_ENVELOPE_MAX, np.max(controlled["radius"]) + 0.01)], color="gray", linestyle="--", alpha=0.8, label="Theta ref")

for lock in NCS_LOCKS:
    ax.plot([lock, lock], [0, max(R_ENVELOPE_MAX, np.max(controlled["radius"]) + 0.01)], color="red", alpha=0.25, linewidth=1.2)

ax.scatter(baseline["theta"][0], baseline["radius"][0], s=180, color="green", label="Start")
ax.scatter(baseline["theta"][-1], baseline["radius"][-1], s=180, color="red", label="Baseline end")

ax.set_title("NEXAH v14.6 — Orbit Capture + Gate Lock Controller (Polar)", va="bottom", fontsize=18)
ax.legend(loc="upper right", bbox_to_anchor=(1.30, 1.15))
fig.tight_layout()
fig.savefig(POLAR_PATH, dpi=160)
plt.close(fig)


print("\nSaved:")
print(f"  • {TS_PATH}")
print(f"  • {PHASE_PATH}")
print(f"  • {POLAR_PATH}")
print(f"  • {REPORT_PATH}")
