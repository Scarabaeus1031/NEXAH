"""
v14.5_orbital_gate_activation_controller.py
===========================================

Goal:
- extend v14.4 toward true orbital activation
- move from pure stabilization to field entry + gate-sensitive control

Core upgrades vs v14.4:
1. Radial Lift
   - if the trajectory is trapped too close to the center,
     actively push it outward toward the orbital field
2. Phase-Coupled Breathing
   - breathing no longer depends only on time
   - breathing envelope is coupled to polar phase theta
3. Radius-Gated Pulse
   - NCS pulse near locks only matters when the orbit is actually developed
4. Smart Snap
   - discrete snap only allowed outside the inner core

Outputs:
- ieee57_v14_5_orbital_gate_timeseries.png
- ieee57_v14_5_orbital_gate_phase.png
- ieee57_v14_5_orbital_gate_polar.png
- ieee57_v14_5_orbital_gate_report.txt
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

TS_PATH = OUTDIR / "ieee57_v14_5_orbital_gate_timeseries.png"
PHASE_PATH = OUTDIR / "ieee57_v14_5_orbital_gate_phase.png"
POLAR_PATH = OUTDIR / "ieee57_v14_5_orbital_gate_polar.png"
REPORT_PATH = OUTDIR / "ieee57_v14_5_orbital_gate_report.txt"


# ============================================================
# 1. Global settings
# ============================================================

TIME_STEPS = 300
SEED = 42
CLASSICAL_THRESHOLD = 0.90

# Stable state-space center from v14.3/v14.4
CENTER_X = 0.942913
CENTER_Y = 0.000076

# Learned orbital references
R_TARGET = 0.587
R_BAND_HALF = 0.035
R_MIN = R_TARGET - R_BAND_HALF
R_MAX = R_TARGET + R_BAND_HALF

THETA_REF = -np.pi / 2.0              # -90°
THETA_TOL = np.deg2rad(12.61)

OMEGA_REF = 0.0
OMEGA_TOL = 0.060

# NCS locks
NCS_LOCKS_DEG = [97.0, 277.0, 292.0]
NCS_LOCKS = np.deg2rad(NCS_LOCKS_DEG)
SNAP_TOL = np.deg2rad(8.0)

# Breathing model
BREATH_AMPLITUDE = 0.065
BREATH_PERIOD = 96
BREATH_PHASE = 0.0

# Pulse model
PULSE_GAIN = 0.045
PULSE_SHARPNESS = 18.0

# Orbital activation additions
INNER_CORE_R = 0.10                   # if below this, system is too close to center
LIFT_GAIN = 0.090                     # outward push into the field
LIFT_SAT = 0.060                      # safety saturation for lift part
RADIUS_PULSE_GATE_POWER = 1.5         # suppress pulses in tiny-radius region

# Gains
K_R = 0.055
K_THETA = 0.022
K_OMEGA = 0.018
K_SNAP = 0.055
K_SWITCH_DAMP = 0.200
K_COH_BOOST = 0.050

# Actuation
U_MAX = 0.090


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


def breathing_target(t: int, theta: float) -> float:
    """
    Dynamic target radius:
    - slow temporal breathing
    - coupled phase breathing
    """
    breath_t = np.sin(2.0 * np.pi * t / BREATH_PERIOD + BREATH_PHASE)
    breath_theta = np.sin(theta)
    mod = 0.65 * breath_t + 0.35 * breath_theta
    return R_TARGET * (1.0 + BREATH_AMPLITUDE * mod)


def pulse_weight(theta: float, locks: np.ndarray, sharpness: float = 18.0) -> float:
    """
    Smooth angular pulse proximity.
    """
    d = min_angle_to_locks(theta, locks)
    return float(np.exp(-sharpness * d))


def radius_gate(r: float, r_target: float, power: float = 1.5) -> float:
    """
    Suppress pulse/snap when radius is tiny.
    0 near center, approaches 1 as orbit develops.
    """
    ratio = np.clip(r / max(r_target, 1e-9), 0.0, 1.0)
    return float(ratio ** power)


def clip(x: float, lo: float, hi: float) -> float:
    return float(np.clip(x, lo, hi))


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
    radius = []
    theta = []
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
            om = 0.0
        else:
            om = wrap_angle(th - last_theta)
        omega.append(om)
        last_theta = th

        if classical_event is None and v_mean < CLASSICAL_THRESHOLD:
            classical_event = t

    return {
        "voltage_mean": np.array(voltage_mean),
        "coherence": np.array(coherence),
        "switch": np.array(switch),
        "radius": np.array(radius),
        "theta": np.array(theta),
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
    radius = []
    theta = []
    omega = []

    r_target_hist = []
    theta_err_hist = []
    u_hist = []
    pulse_hist = []
    snap_hist = []
    lift_hist = []

    classical_event = None
    last_theta = None

    last_coh = CENTER_X
    last_sw = CENTER_Y

    for t in range(time_steps):
        # use last state estimate to compute control
        r_est, th_est, dx, dy = state_to_polar(last_coh, last_sw, CENTER_X, CENTER_Y)

        # dynamic breathing target
        r_tar = breathing_target(t, th_est)
        r_target_hist.append(r_tar)

        # errors
        r_err = r_tar - r_est
        theta_err = wrap_angle(THETA_REF - th_est)
        theta_err_hist.append(theta_err)

        if last_theta is None:
            om_est = 0.0
        else:
            om_est = wrap_angle(th_est - last_theta)

        # ---------------------------------------------
        # 4.1 Base controller parts
        # ---------------------------------------------
        u_r = K_R * r_err
        u_theta = K_THETA * theta_err
        u_omega = -K_OMEGA * (om_est - OMEGA_REF)
        u_switch = -K_SWITCH_DAMP * last_sw
        u_coh = K_COH_BOOST * (CENTER_X - last_coh)

        # ---------------------------------------------
        # 4.2 Radial lift: missing field-entry step
        # ---------------------------------------------
        if r_est < INNER_CORE_R:
            lift = LIFT_GAIN * (INNER_CORE_R - r_est) / max(INNER_CORE_R, 1e-9)
            lift = clip(lift, 0.0, LIFT_SAT)
        else:
            lift = 0.0
        lift_hist.append(lift)

        # ---------------------------------------------
        # 4.3 Radius-gated pulse near NCS locks
        # ---------------------------------------------
        ang_weight = pulse_weight(th_est, NCS_LOCKS, PULSE_SHARPNESS)
        rad_weight = radius_gate(r_est, R_TARGET, RADIUS_PULSE_GATE_POWER)
        pulse = PULSE_GAIN * ang_weight * rad_weight * np.sign(theta_err if abs(theta_err) > 1e-9 else 1.0)
        pulse_hist.append(pulse)

        # ---------------------------------------------
        # 4.4 Smart snap only outside inner core
        # ---------------------------------------------
        d_lock = min_angle_to_locks(th_est, NCS_LOCKS)
        if (d_lock < SNAP_TOL) and (r_est > INNER_CORE_R):
            lock = nearest_lock(th_est, NCS_LOCKS)
            snap = K_SNAP * wrap_angle(lock - th_est)
        else:
            snap = 0.0
        snap_hist.append(snap)

        # final control
        u = u_r + u_theta + u_omega + u_switch + u_coh + lift + pulse + snap
        u = clip(u, -U_MAX, U_MAX)
        u_hist.append(u)

        # actuation on load scale
        scale = max(0.50, load_factor[t] + noise[t] - u)

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
            om = 0.0
        else:
            om = wrap_angle(th - last_theta)
        omega.append(om)

        last_theta = th
        last_coh = coh
        last_sw = sw

        if classical_event is None and v_mean < CLASSICAL_THRESHOLD:
            classical_event = t

    return {
        "voltage_mean": np.array(voltage_mean),
        "coherence": np.array(coherence),
        "switch": np.array(switch),
        "radius": np.array(radius),
        "theta": np.array(theta),
        "omega": np.array(omega),
        "r_target": np.array(r_target_hist),
        "theta_err": np.array(theta_err_hist),
        "u": np.array(u_hist),
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

baseline_escape = baseline["radius"] > np.percentile(baseline["radius"], 90)
controlled_escape = controlled["radius"] > np.percentile(baseline["radius"], 90)

snap_count = int(np.sum(np.abs(controlled["snap"]) > 1e-9))
pulse_count = int(np.sum(np.abs(controlled["pulse"]) > 1e-6))
lift_count = int(np.sum(np.abs(controlled["lift"]) > 1e-9))
control_activation_count = int(np.sum(np.abs(controlled["u"]) > 1e-6))

report_lines = []
report_lines.append("===== NEXAH V14.5 ORBITAL + GATE ACTIVATION REPORT =====")
report_lines.append("")
report_lines.append("Stability center:")
report_lines.append(f"  coherence = {CENTER_X:.6f}")
report_lines.append(f"  switch    = {CENTER_Y:.6f}")
report_lines.append("")
report_lines.append(f"Band target radius: {R_TARGET:.6f}")
report_lines.append(f"Band interval: [{R_MIN:.6f}, {R_MAX:.6f}]")
report_lines.append(f"Theta reference: {THETA_REF:.6f} rad ({np.degrees(THETA_REF):.2f} deg)")
report_lines.append(f"Theta tolerance: {THETA_TOL:.6f} rad ({np.degrees(THETA_TOL):.2f} deg)")
report_lines.append(f"Omega reference: {OMEGA_REF:.6f}")
report_lines.append(f"Omega tolerance: {OMEGA_TOL:.6f}")
report_lines.append(f"NCS phase locks (deg): {NCS_LOCKS_DEG}")
report_lines.append(f"Phase snap tolerance: {SNAP_TOL:.6f} rad ({np.degrees(SNAP_TOL):.2f} deg)")
report_lines.append("")
report_lines.append(f"Inner core radius: {INNER_CORE_R:.6f}")
report_lines.append(f"Lift gain: {LIFT_GAIN:.6f}")
report_lines.append(f"Lift saturation: {LIFT_SAT:.6f}")
report_lines.append(f"Breathing amplitude: {BREATH_AMPLITUDE:.6f}")
report_lines.append(f"Breathing period: {BREATH_PERIOD}")
report_lines.append(f"PULSE_GAIN: {PULSE_GAIN:.6f}")
report_lines.append(f"PULSE_SHARPNESS: {PULSE_SHARPNESS:.6f}")
report_lines.append(f"U_MAX: {U_MAX:.6f}")
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
# 7. Plots
# ============================================================

# ---------- Time series ----------
fig, axs = plt.subplots(6, 1, figsize=(14, 22), sharex=True)

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
axs[3].plot(t, controlled["r_target"], color="black", linestyle=":", label="Breathing target")
axs[3].axhline(R_TARGET, color="gray", linestyle="--", label="Static target")
axs[3].axhline(R_MIN, color="gray", linestyle="--", alpha=0.6, label="Band min/max")
axs[3].axhline(R_MAX, color="gray", linestyle="--", alpha=0.6)
axs[3].set_ylabel("Radius")
axs[3].legend()

axs[4].plot(t, controlled["theta_err"], color="red", label="Theta err")
axs[4].axhline(THETA_TOL, color="gray", linestyle="--")
axs[4].axhline(-THETA_TOL, color="gray", linestyle="--")
axs[4].set_ylabel("Theta err")
axs[4].legend()

axs[5].plot(t, controlled["u"], color="black", label="Control signal")
axs[5].fill_between(t, 0, 1, where=np.abs(controlled["u"]) > 1e-6, color="lightgray", alpha=0.6, transform=axs[5].get_xaxis_transform(), label="Active control")
axs[5].plot(t, controlled["pulse"], color="red", alpha=0.7, label="Pulse")
axs[5].plot(t, controlled["lift"], color="green", alpha=0.7, label="Lift")
axs[5].set_ylabel("u(t)")
axs[5].set_xlabel("Time step")
axs[5].legend()

fig.suptitle("NEXAH v14.5 — Orbital + Gate Activation Controller (Time Series)", fontsize=18)
fig.tight_layout()
fig.savefig(TS_PATH, dpi=160)
plt.close(fig)


# ---------- Phase space ----------
fig, ax = plt.subplots(figsize=(14, 10))

ax.plot(baseline["coherence"], baseline["switch"], alpha=0.25, linewidth=3, label="Baseline trajectory")
ax.plot(controlled["coherence"], controlled["switch"], color="tab:orange", linewidth=2.2, label="Controlled trajectory")

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
ax.scatter(controlled["coherence"][-1], controlled["switch"][-1], s=220, color="purple", label="Controlled end")

ax.axhline(0.0, color="gray", linestyle="--", alpha=0.5)
ax.axvline(CENTER_X, color="gray", linestyle="--", alpha=0.5)

ax.set_xlabel("Coherence")
ax.set_ylabel("Switch signal")
ax.set_title("NEXAH v14.5 — Orbital + Gate Activation Controller (Phase Space)")
ax.legend(loc="upper left")
ax.grid(True, alpha=0.25)
fig.tight_layout()
fig.savefig(PHASE_PATH, dpi=160)
plt.close(fig)


# ---------- Polar ----------
fig = plt.figure(figsize=(14, 12))
ax = fig.add_subplot(111, projection="polar")

ax.plot(baseline["theta"], baseline["radius"], alpha=0.25, linewidth=3, label="Baseline")
ax.plot(controlled["theta"], controlled["radius"], color="tab:orange", linewidth=2.0, label="Controlled")

ax.plot(np.linspace(-np.pi, np.pi, 400), np.full(400, R_TARGET), "k:", linewidth=2.2, label="Target ring")
ax.plot(np.linspace(-np.pi, np.pi, 400), np.full(400, R_MIN), color="gray", linestyle="--", alpha=0.8, label="Band")
ax.plot(np.linspace(-np.pi, np.pi, 400), np.full(400, R_MAX), color="gray", linestyle="--", alpha=0.8)
ax.plot([THETA_REF, THETA_REF], [0, max(R_MAX, np.max(controlled["radius"]) + 0.05)], color="gray", linestyle="--", alpha=0.8, label="Theta ref")

ax.scatter(baseline["theta"][0], baseline["radius"][0], s=180, color="green", label="Start")
ax.scatter(baseline["theta"][-1], baseline["radius"][-1], s=180, color="red", label="Baseline end")
ax.scatter(controlled["theta"][-1], controlled["radius"][-1], s=180, color="purple", label="Controlled end")

ax.set_title("NEXAH v14.5 — Orbital + Gate Activation Controller (Polar)", va="bottom", fontsize=18)
ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.15))
fig.tight_layout()
fig.savefig(POLAR_PATH, dpi=160)
plt.close(fig)


print("\nSaved:")
print(f"  • {TS_PATH}")
print(f"  • {PHASE_PATH}")
print(f"  • {POLAR_PATH}")
print(f"  • {REPORT_PATH}")
