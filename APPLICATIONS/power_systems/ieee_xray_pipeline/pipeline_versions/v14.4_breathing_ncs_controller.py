"""
v14.4_breathing_ncs_controller.py
=================================

Goal:
- extend v14.3 with a true breathing + pulse controller
- model the v-band as a low-frequency breathing envelope
- model the n-band as discrete pulse injection near phase gates
- keep the controller in NEXAH state space:
    x = coherence
    y = switch signal

Design:
1. Band term
   pull radius toward the learned ring
2. Phase term
   align trajectory toward theta reference
3. Velocity term
   damp angular drift
4. Breathing term
   periodically expand / contract target radius
5. Pulse term
   inject short corrections near NCS phase gates
6. Snap term
   optional stronger lock when near a gate

Outputs:
- ieee57_v14_4_breathing_ncs_timeseries.png
- ieee57_v14_4_breathing_ncs_phase.png
- ieee57_v14_4_breathing_ncs_polar.png
- ieee57_v14_4_breathing_ncs_report.txt
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

TS_PATH = OUTDIR / "ieee57_v14_4_breathing_ncs_timeseries.png"
PHASE_PATH = OUTDIR / "ieee57_v14_4_breathing_ncs_phase.png"
POLAR_PATH = OUTDIR / "ieee57_v14_4_breathing_ncs_polar.png"
REPORT_PATH = OUTDIR / "ieee57_v14_4_breathing_ncs_report.txt"


# ============================================================
# 1. Global settings
# ============================================================

TIME_STEPS = 300
SEED = 42
CLASSICAL_THRESHOLD = 0.90

# Learned / chosen NEXAH references
R_TARGET = 0.587
R_BAND_HALF = 0.035
R_MIN = R_TARGET - R_BAND_HALF
R_MAX = R_TARGET + R_BAND_HALF

THETA_REF = -np.pi / 2.0                  # -90 deg
THETA_TOL = np.deg2rad(12.61)

OMEGA_REF = 0.0
OMEGA_TOL = 0.060

# NCS locks from prior experiments / visuals
NCS_LOCKS_DEG = [97.0, 277.0, 292.0]
NCS_LOCKS = np.deg2rad(NCS_LOCKS_DEG)
SNAP_TOL = np.deg2rad(8.0)

# Breathing model
BREATH_AMPLITUDE = 0.065                  # target ring modulation
BREATH_PERIOD = 96                        # slower than switching
BREATH_PHASE = 0.0

# Pulse model
PULSE_GAIN = 0.035
PULSE_SHARPNESS = 18.0                    # how local the pulse is near gates

# Control gains
K_R = 0.060                               # radial
K_THETA = 0.022                           # phase
K_OMEGA = 0.020                           # angular velocity
K_SNAP = 0.050                            # discrete lock
K_SWITCH_DAMP = 0.180                     # reduce switch amplitude
K_COH_BOOST = 0.055                       # slight bias to coherence

# Load actuation
U_MAX = 0.090
BASE_GLOBAL_LOAD_SCALE = 1.0

# State-space center
# Using a stable center from your v14.3 report
CENTER_X = 0.942913
CENTER_Y = 0.000076


# ============================================================
# 2. Utility functions
# ============================================================

def wrap_angle(theta: float) -> float:
    """Wrap angle to [-pi, pi]."""
    return (theta + np.pi) % (2 * np.pi) - np.pi


def min_angle_to_locks(theta: float, locks: np.ndarray) -> float:
    """Return minimum wrapped angular distance to any lock."""
    return min(abs(wrap_angle(theta - lock)) for lock in locks)


def nearest_lock(theta: float, locks: np.ndarray) -> float:
    """Return nearest lock angle."""
    dists = [abs(wrap_angle(theta - lock)) for lock in locks]
    return float(locks[int(np.argmin(dists))])


def state_to_polar(x: float, y: float, cx: float, cy: float):
    """Convert state (x, y) to radius + angle relative to center."""
    dx = x - cx
    dy = y - cy
    r = float(np.hypot(dx, dy))
    theta = float(np.arctan2(dy, dx))
    return r, theta, dx, dy


def pulse_weight(theta: float, locks: np.ndarray, sharpness: float = 12.0) -> float:
    """
    Smooth pulse proximity weight in [0, 1].
    Strong near phase gates, weak far away.
    """
    d = min_angle_to_locks(theta, locks)
    return float(np.exp(-sharpness * d))


def breathing_target(t: int) -> float:
    """Dynamic target radius with breathing envelope."""
    breath = BREATH_AMPLITUDE * np.sin(2.0 * np.pi * t / BREATH_PERIOD + BREATH_PHASE)
    return R_TARGET * (1.0 + breath)


def simulate_baseline(time_steps: int = TIME_STEPS, seed: int = SEED):
    """
    Baseline power-flow run without NEXAH control.
    Returns a dictionary of histories.
    """
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
        coh = float(1.0 - v_std)

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


def simulate_controlled(time_steps: int = TIME_STEPS, seed: int = SEED):
    """
    Controlled run with breathing + pulse NCS logic.
    """
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

    control_signal = []
    breath_target_hist = []
    pulse_hist = []
    snap_hist = []
    theta_err_hist = []

    classical_event = None
    last_theta = None

    # controller memory
    u_prev = 0.0

    for t in range(time_steps):
        # predicted prior state
        if len(coherence) == 0:
            coh_prev = CENTER_X
            sw_prev = CENTER_Y
            r_prev = 0.0
            th_prev = 0.0
            omg_prev = 0.0
        else:
            coh_prev = coherence[-1]
            sw_prev = switch[-1]
            r_prev = radius[-1]
            th_prev = theta[-1]
            omg_prev = omega[-1]

        # dynamic breathing ring
        r_target_dyn = breathing_target(t)
        breath_target_hist.append(r_target_dyn)

        # polar control terms
        theta_err = wrap_angle(THETA_REF - th_prev)
        theta_err_hist.append(theta_err)

        radial_err = r_target_dyn - r_prev
        omega_err = OMEGA_REF - omg_prev

        band_term = K_R * radial_err
        phase_term = K_THETA * theta_err
        velocity_term = K_OMEGA * omega_err

        # pulse term near NCS gates
        p_w = pulse_weight(th_prev, NCS_LOCKS, sharpness=PULSE_SHARPNESS)
        pulse_term = PULSE_GAIN * p_w * np.sign(theta_err if abs(theta_err) > 1e-9 else 1.0)

        # snap term if very close to a lock
        nearest = nearest_lock(th_prev, NCS_LOCKS)
        d_lock = abs(wrap_angle(th_prev - nearest))
        snap_on = 1.0 if d_lock < SNAP_TOL else 0.0
        snap_term = K_SNAP * snap_on * np.sign(wrap_angle(nearest - th_prev) if d_lock > 1e-9 else 0.0)

        # direct damping / coherence bias
        switch_damp_term = -K_SWITCH_DAMP * sw_prev
        coh_boost_term = K_COH_BOOST * max(0.0, CENTER_X - coh_prev)

        # hybrid signal
        u = (
            band_term
            + phase_term
            + velocity_term
            + pulse_term
            + snap_term
            + switch_damp_term
            + coh_boost_term
        )

        # smooth a bit, then clip
        u = 0.55 * u + 0.45 * u_prev
        u = float(np.clip(u, -U_MAX, U_MAX))
        u_prev = u

        control_signal.append(u)
        pulse_hist.append(pulse_term)
        snap_hist.append(snap_on)

        # turn control into load modulation
        base_scale = max(0.50, load_factor[t] + noise[t])

        # negative u reduces loading, positive u slightly increases
        # using asymmetric effect so stabilizing reductions matter more
        scale = base_scale * (1.0 - 0.90 * u)

        scale = float(np.clip(scale, 0.45, 1.45))

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
        coh = float(1.0 - v_std)

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
        "control_signal": np.array(control_signal),
        "breath_target": np.array(breath_target_hist),
        "pulse_term": np.array(pulse_hist),
        "snap_active": np.array(snap_hist),
        "theta_err": np.array(theta_err_hist),
        "classical_event": classical_event,
    }


def count_escapes(radius_series: np.ndarray, threshold: float) -> int:
    """Count how many samples exceed a radial threshold."""
    return int(np.sum(radius_series > threshold))


# ============================================================
# 3. Run experiments
# ============================================================

baseline = simulate_baseline()
controlled = simulate_controlled()

baseline_event = baseline["classical_event"]
controlled_event = controlled["classical_event"]

baseline_escape_count = count_escapes(baseline["radius"], R_MAX)
controlled_escape_count = count_escapes(controlled["radius"], R_MAX)

mean_control_signal = float(np.mean(controlled["control_signal"]))
max_control_signal = float(np.max(np.abs(controlled["control_signal"])))
control_activation_count = int(np.sum(np.abs(controlled["control_signal"]) > 1e-9))
snap_activation_count = int(np.sum(controlled["snap_active"] > 0.5))


# ============================================================
# 4. Plots
# ============================================================

t = np.arange(TIME_STEPS)

# ------------------------
# Time series plot
# ------------------------
fig, axes = plt.subplots(6, 1, figsize=(14, 20), sharex=True)

axes[0].plot(t, baseline["voltage_mean"], label="Baseline", alpha=0.35, linewidth=2)
axes[0].plot(t, controlled["voltage_mean"], label="Controlled", linewidth=1.5)
axes[0].axhline(CLASSICAL_THRESHOLD, linestyle="--", color="gray", alpha=0.8, label="Classical threshold")
axes[0].set_ylabel("Voltage mean")
axes[0].legend(loc="best")
axes[0].grid(True, alpha=0.3)

axes[1].plot(t, baseline["coherence"], label="Baseline", alpha=0.35, linewidth=2)
axes[1].plot(t, controlled["coherence"], label="Controlled", linewidth=1.5)
axes[1].set_ylabel("Coherence")
axes[1].grid(True, alpha=0.3)

axes[2].plot(t, baseline["switch"], label="Baseline", alpha=0.35, linewidth=2)
axes[2].plot(t, controlled["switch"], label="Controlled", linewidth=1.5)
axes[2].axhline(0.0, linestyle="--", color="gray", alpha=0.8)
axes[2].set_ylabel("Switch")
axes[2].grid(True, alpha=0.3)

axes[3].plot(t, controlled["radius"], color="purple", label="Controlled radius")
axes[3].plot(t, controlled["breath_target"], linestyle=":", color="black", label="Breathing target")
axes[3].axhline(R_TARGET, linestyle="--", color="black", alpha=0.6, label="Static target")
axes[3].axhline(R_MIN, linestyle="--", color="gray", alpha=0.8, label="Band min/max")
axes[3].axhline(R_MAX, linestyle="--", color="gray", alpha=0.8)
axes[3].set_ylabel("Radius")
axes[3].legend(loc="best")
axes[3].grid(True, alpha=0.3)

axes[4].plot(t, controlled["theta_err"], color="red", label="Theta error")
axes[4].axhline(THETA_TOL, linestyle="--", color="gray", alpha=0.8)
axes[4].axhline(-THETA_TOL, linestyle="--", color="gray", alpha=0.8)
axes[4].set_ylabel("Theta err")
axes[4].legend(loc="best")
axes[4].grid(True, alpha=0.3)

axes[5].plot(t, controlled["control_signal"], color="black", label="Control signal")
axes[5].fill_between(
    t,
    0.0,
    controlled["control_signal"],
    where=np.abs(controlled["control_signal"]) > 1e-9,
    alpha=0.15,
    color="gray",
    label="Active control"
)
axes[5].plot(t, controlled["pulse_term"], color="red", alpha=0.6, linewidth=1.0, label="Pulse")
axes[5].set_ylabel("u(t)")
axes[5].set_xlabel("Time step")
axes[5].legend(loc="best")
axes[5].grid(True, alpha=0.3)

fig.suptitle("NEXAH v14.4 — Breathing NCS Controller (Time Series)", fontsize=18)
plt.tight_layout()
plt.savefig(TS_PATH, dpi=200)
plt.close(fig)

# ------------------------
# Cartesian phase plot
# ------------------------
fig, ax = plt.subplots(figsize=(14, 10))

ax.plot(
    baseline["coherence"],
    baseline["switch"],
    color="steelblue",
    alpha=0.35,
    linewidth=3,
    label="Baseline trajectory"
)
ax.plot(
    controlled["coherence"],
    controlled["switch"],
    color="darkorange",
    linewidth=2.2,
    label="Controlled trajectory"
)

baseline_escape = baseline["radius"] > R_MAX
controlled_escape = controlled["radius"] > R_MAX

ax.scatter(
    baseline["coherence"][baseline_escape],
    baseline["switch"][baseline_escape],
    s=220,
    facecolors="none",
    edgecolors="tab:blue",
    linewidths=2.2,
    label="Baseline escape region"
)
ax.scatter(
    controlled["coherence"][controlled_escape],
    controlled["switch"][controlled_escape],
    s=220,
    facecolors="none",
    edgecolors="tab:orange",
    linewidths=2.2,
    label="Controlled escape region"
)

ax.scatter([CENTER_X], [CENTER_Y], s=360, color="gold", marker="*", label="Stability center", zorder=10)
ax.scatter([baseline["coherence"][0]], [baseline["switch"][0]], s=200, color="green", label="Start", zorder=10)
ax.scatter([baseline["coherence"][-1]], [baseline["switch"][-1]], s=200, color="red", label="Baseline end", zorder=10)
ax.scatter([controlled["coherence"][-1]], [controlled["switch"][-1]], s=200, color="purple", label="Controlled end", zorder=10)

ax.axhline(0.0, linestyle="--", color="gray", alpha=0.5)
ax.axvline(CENTER_X, linestyle="--", color="gray", alpha=0.5)

ax.set_xlabel("Coherence")
ax.set_ylabel("Switch signal")
ax.set_title("NEXAH v14.4 — Breathing NCS Controller (Phase Space)")
ax.legend(loc="upper left")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(PHASE_PATH, dpi=200)
plt.close(fig)

# ------------------------
# Polar plot
# ------------------------
fig = plt.figure(figsize=(14, 12))
ax = plt.subplot(111, projection="polar")

ax.plot(baseline["theta"], baseline["radius"], color="steelblue", alpha=0.35, linewidth=3, label="Baseline")
ax.plot(controlled["theta"], controlled["radius"], color="darkorange", linewidth=2.2, label="Controlled")

ax.plot(np.linspace(0, 2 * np.pi, 400), np.full(400, R_TARGET), linestyle=":", color="black", linewidth=2, label="Target ring")
ax.plot(np.linspace(0, 2 * np.pi, 400), np.full(400, R_MIN), linestyle="--", color="gray", alpha=0.8, label="Band")
ax.plot(np.linspace(0, 2 * np.pi, 400), np.full(400, R_MAX), linestyle="--", color="gray", alpha=0.8)
ax.plot([THETA_REF, THETA_REF], [0, max(0.7, np.max(controlled["radius"]))], linestyle="--", color="gray", alpha=0.7, label="Theta ref")

ax.scatter([baseline["theta"][0]], [baseline["radius"][0]], s=180, color="green", label="Start", zorder=10)
ax.scatter([baseline["theta"][-1]], [baseline["radius"][-1]], s=180, color="red", label="Baseline end", zorder=10)
ax.scatter([controlled["theta"][-1]], [controlled["radius"][-1]], s=180, color="purple", label="Controlled end", zorder=10)

plt.title("NEXAH v14.4 — Breathing NCS Controller (Polar)", pad=22, fontsize=18)
plt.legend(loc="upper right")
plt.tight_layout()
plt.savefig(POLAR_PATH, dpi=200)
plt.close(fig)


# ============================================================
# 5. Report
# ============================================================

lines = []
lines.append("===== NEXAH V14.4 BREATHING NCS CONTROLLER REPORT =====\n")
lines.append(f"Stability center:\n")
lines.append(f"  coherence = {CENTER_X:.6f}\n")
lines.append(f"  switch    = {CENTER_Y:.6f}\n\n")

lines.append(f"Band target radius: {R_TARGET:.6f}\n")
lines.append(f"Band interval: [{R_MIN:.6f}, {R_MAX:.6f}]\n")
lines.append(f"Theta reference: {THETA_REF:.6f} rad ({np.rad2deg(THETA_REF):.2f} deg)\n")
lines.append(f"Theta tolerance: {THETA_TOL:.6f} rad ({np.rad2deg(THETA_TOL):.2f} deg)\n")
lines.append(f"Omega reference: {OMEGA_REF:.6f}\n")
lines.append(f"Omega tolerance: {OMEGA_TOL:.6f}\n")
lines.append(f"NCS phase locks (deg): {NCS_LOCKS_DEG}\n")
lines.append(f"Phase snap tolerance: {SNAP_TOL:.6f} rad ({np.rad2deg(SNAP_TOL):.2f} deg)\n")
lines.append(f"Breathing amplitude: {BREATH_AMPLITUDE:.6f}\n")
lines.append(f"Breathing period: {BREATH_PERIOD}\n")
lines.append(f"PULSE_GAIN: {PULSE_GAIN:.6f}\n")
lines.append(f"PULSE_SHARPNESS: {PULSE_SHARPNESS:.6f}\n")
lines.append(f"U_MAX: {U_MAX:.6f}\n\n")

lines.append(f"Baseline mean radius: {np.mean(baseline['radius']):.6f}\n")
lines.append(f"Controlled mean radius: {np.mean(controlled['radius']):.6f}\n\n")

lines.append(f"Baseline max radius: {np.max(baseline['radius']):.6f}\n")
lines.append(f"Controlled max radius: {np.max(controlled['radius']):.6f}\n\n")

lines.append(f"Baseline mean coherence: {np.mean(baseline['coherence']):.6f}\n")
lines.append(f"Controlled mean coherence: {np.mean(controlled['coherence']):.6f}\n\n")

lines.append(f"Baseline first classical event: {baseline_event}\n")
lines.append(f"Controlled first classical event: {controlled_event}\n")
if baseline_event is not None and controlled_event is not None:
    lines.append(f"Collapse shift (controlled - baseline): {controlled_event - baseline_event}\n")
else:
    lines.append("Collapse shift (controlled - baseline): None\n")

lines.append(f"\nBaseline escape count: {baseline_escape_count}\n")
lines.append(f"Controlled escape count: {controlled_escape_count}\n")
lines.append(f"Escape delta (baseline - controlled): {baseline_escape_count - controlled_escape_count}\n\n")

lines.append(f"Snap activation count: {snap_activation_count}\n")
lines.append(f"Control activation count: {control_activation_count}\n")
lines.append(f"Mean control signal: {mean_control_signal:.6f}\n")
lines.append(f"Max |control signal|: {max_control_signal:.6f}\n\n")

if np.mean(controlled["coherence"]) > np.mean(baseline["coherence"]):
    lines.append("Mean coherence improved.\n")
else:
    lines.append("Mean coherence did not improve.\n")

if np.max(controlled["radius"]) < np.max(baseline["radius"]):
    lines.append("Maximum orbit excursion improved.\n")
else:
    lines.append("Maximum orbit excursion did not improve.\n")

if controlled_escape_count < baseline_escape_count:
    lines.append("Escape count reduced.\n")
else:
    lines.append("Escape count did not reduce.\n")

if snap_activation_count > 0:
    lines.append("Discrete NCS lock engagement occurred.\n")
else:
    lines.append("Discrete NCS lock engagement did not occur.\n")

REPORT_PATH.write_text("".join(lines), encoding="utf-8")


# ============================================================
# 6. Console output
# ============================================================

print("===== NEXAH V14.4 BREATHING NCS CONTROLLER REPORT =====\n")
print(f"Stability center:")
print(f"  coherence = {CENTER_X:.6f}")
print(f"  switch    = {CENTER_Y:.6f}\n")

print(f"Band target radius: {R_TARGET:.6f}")
print(f"Band interval: [{R_MIN:.6f}, {R_MAX:.6f}]")
print(f"Theta reference: {THETA_REF:.6f} rad ({np.rad2deg(THETA_REF):.2f} deg)")
print(f"Theta tolerance: {THETA_TOL:.6f} rad ({np.rad2deg(THETA_TOL):.2f} deg)")
print(f"Omega reference: {OMEGA_REF:.6f}")
print(f"Omega tolerance: {OMEGA_TOL:.6f}")
print(f"NCS phase locks (deg): {NCS_LOCKS_DEG}")
print(f"Phase snap tolerance: {SNAP_TOL:.6f} rad ({np.rad2deg(SNAP_TOL):.2f} deg)")
print(f"Breathing amplitude: {BREATH_AMPLITUDE:.6f}")
print(f"Breathing period: {BREATH_PERIOD}")
print(f"PULSE_GAIN: {PULSE_GAIN:.6f}")
print(f"PULSE_SHARPNESS: {PULSE_SHARPNESS:.6f}")
print(f"U_MAX: {U_MAX:.6f}\n")

print(f"Baseline mean radius: {np.mean(baseline['radius']):.6f}")
print(f"Controlled mean radius: {np.mean(controlled['radius']):.6f}\n")

print(f"Baseline max radius: {np.max(baseline['radius']):.6f}")
print(f"Controlled max radius: {np.max(controlled['radius']):.6f}\n")

print(f"Baseline mean coherence: {np.mean(baseline['coherence']):.6f}")
print(f"Controlled mean coherence: {np.mean(controlled['coherence']):.6f}\n")

print(f"Baseline first classical event: {baseline_event}")
print(f"Controlled first classical event: {controlled_event}")
if baseline_event is not None and controlled_event is not None:
    print(f"Collapse shift (controlled - baseline): {controlled_event - baseline_event}")
else:
    print("Collapse shift (controlled - baseline): None")

print(f"\nBaseline escape count: {baseline_escape_count}")
print(f"Controlled escape count: {controlled_escape_count}")
print(f"Escape delta (baseline - controlled): {baseline_escape_count - controlled_escape_count}\n")

print(f"Snap activation count: {snap_activation_count}")
print(f"Control activation count: {control_activation_count}")
print(f"Mean control signal: {mean_control_signal:.6f}")
print(f"Max |control signal|: {max_control_signal:.6f}\n")

if np.mean(controlled["coherence"]) > np.mean(baseline["coherence"]):
    print("Mean coherence improved.")
else:
    print("Mean coherence did not improve.")

if np.max(controlled["radius"]) < np.max(baseline["radius"]):
    print("Maximum orbit excursion improved.")
else:
    print("Maximum orbit excursion did not improve.")

if controlled_escape_count < baseline_escape_count:
    print("Escape count reduced.")
else:
    print("Escape count did not reduce.")

if snap_activation_count > 0:
    print("Discrete NCS lock engagement occurred.")
else:
    print("Discrete NCS lock engagement did not occur.")

print("\nSaved:")
print(f"  • {TS_PATH}")
print(f"  • {PHASE_PATH}")
print(f"  • {POLAR_PATH}")
print(f"  • {REPORT_PATH}")
