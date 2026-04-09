"""
v12_adaptive_phase_lock.py
==========================

Goal:
- improve on v11 by using adaptive phase locking instead of a fixed zero-phase controller
- learn the natural orbit phase from the baseline run
- intervene only when the phase deviates beyond a tolerance band
- optionally weight the intervention by radius, so the controller stays quiet near the core
- save all outputs into the local ieee_xray_pipeline/results folder

Core idea:
1. Run baseline
2. Estimate a stable target phase from the baseline trajectory
3. Run controlled simulation with adaptive phase lock:
       u(t) = -k * wrapped_phase_error * radius_weight
   only when |phase_error| > phase_tolerance

State space:
- x = coherence
- y = switch signal

Outputs:
- ieee57_v12_adaptive_phase_timeseries.png
- ieee57_v12_adaptive_phase_phase_space.png
- ieee57_v12_adaptive_phase_polar.png
- ieee57_v12_adaptive_phase_report.txt
"""

import pandapower as pp
import pandapower.networks as pn
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# =========================
# 1. Paths / Config
# =========================

BASE_PATH = Path(__file__).resolve().parent
RESULT_PATH = BASE_PATH.parent / "results"
RESULT_PATH.mkdir(parents=True, exist_ok=True)

TIME_STEPS = 300
SEED = 42

BASE_AMPLITUDE = 0.25
NOISE_STD = 0.02

# adaptive phase-lock parameters
K_PHASE = 0.18
PHASE_TOL = 0.22          # radians; dead zone around learned phase
MAX_CONTROL = 0.08        # clip absolute control
RADIUS_GAIN = 1.5         # stronger action farther from orbit core


# =========================
# 2. Utilities
# =========================

def wrapped_angle_diff(theta: np.ndarray, theta_ref: float) -> np.ndarray:
    """
    Minimal wrapped phase difference in [-pi, pi].
    """
    return np.angle(np.exp(1j * (theta - theta_ref)))


def circular_mean(theta: np.ndarray) -> float:
    """
    Circular mean angle.
    """
    z = np.mean(np.exp(1j * theta))
    return float(np.angle(z))


def robust_phase_target(theta: np.ndarray, radius: np.ndarray, q_low=0.10, q_high=0.90) -> float:
    """
    Learn target phase from the denser mid-orbit, excluding extreme transients.
    """
    r_low = np.quantile(radius, q_low)
    r_high = np.quantile(radius, q_high)
    mask = (radius >= r_low) & (radius <= r_high)
    if np.sum(mask) < 10:
        return circular_mean(theta)
    return circular_mean(theta[mask])


def compute_state(voltages: np.ndarray):
    v_mean = float(np.mean(voltages))
    v_std = float(np.std(voltages))
    coherence = 1.0 - v_std
    return v_mean, coherence


def compute_switch(voltage_history):
    if len(voltage_history) > 2:
        return float(np.gradient(voltage_history)[-1])
    return 0.0


def estimate_center(x_hist: np.ndarray, y_hist: np.ndarray, n=25):
    n_use = min(n, len(x_hist))
    return float(np.mean(x_hist[:n_use])), float(np.mean(y_hist[:n_use]))


# =========================
# 3. Baseline simulation
# =========================

np.random.seed(SEED)
load_factor = 1.0 + BASE_AMPLITUDE * np.sin(np.linspace(0, 6 * np.pi, TIME_STEPS))
noise = np.random.normal(0, NOISE_STD, TIME_STEPS)

net_base = pn.case57()
base_load = net_base.load["p_mw"].to_numpy(copy=True)

baseline_v = []
baseline_x = []
baseline_y = []
baseline_events = []

for t in range(TIME_STEPS):
    scale = float(np.clip(load_factor[t] + noise[t], 0.70, 1.35))
    net_base.load["p_mw"] = base_load * scale

    try:
        pp.runpp(net_base, enforce_q_lims=True, init="results")
        voltages = net_base.res_bus.vm_pu.values
    except Exception:
        voltages = np.ones(len(net_base.bus)) * 0.95

    v_mean, coh = compute_state(voltages)
    sw = compute_switch(baseline_v)

    baseline_v.append(v_mean)
    baseline_x.append(coh)
    baseline_y.append(sw)

    if t > 5 and baseline_v[-2] >= 0.90 and v_mean < 0.90:
        baseline_events.append(t)

baseline_v = np.array(baseline_v)
baseline_x = np.array(baseline_x)
baseline_y = np.array(baseline_y)

center_x, center_y = estimate_center(baseline_x, baseline_y, n=25)
baseline_dx = baseline_x - center_x
baseline_dy = baseline_y - center_y
baseline_r = np.sqrt(baseline_dx**2 + baseline_dy**2)
baseline_theta = np.arctan2(baseline_dy, baseline_dx)

theta_target = robust_phase_target(baseline_theta, baseline_r, q_low=0.15, q_high=0.85)
r_target = float(np.median(baseline_r))
r_scale = float(np.std(baseline_r) + 1e-8)


# =========================
# 4. Controlled simulation
# =========================

net_ctrl = pn.case57()
net_ctrl.load["p_mw"] = base_load.copy()

ctrl_v = []
ctrl_x = []
ctrl_y = []
ctrl_events = []

control_signal = []
control_active = []
phase_error_hist = []
theta_hist = []
radius_hist = []

for t in range(TIME_STEPS):
    # use same external forcing as baseline
    raw_scale = float(np.clip(load_factor[t] + noise[t], 0.70, 1.35))

    # estimate current phase from last state
    if len(ctrl_x) >= 5:
        x_arr = np.array(ctrl_x)
        y_arr = np.array(ctrl_y)

        c_x, c_y = estimate_center(x_arr, y_arr, n=25)
        dx = x_arr[-1] - c_x
        dy = y_arr[-1] - c_y
        r_now = float(np.sqrt(dx * dx + dy * dy))
        theta_now = float(np.arctan2(dy, dx))

        err = float(wrapped_angle_diff(np.array([theta_now]), theta_target)[0])

        # adaptive radius weighting: quiet near target orbit, stronger farther away
        radius_weight = 1.0 + RADIUS_GAIN * np.clip((r_now - r_target) / (r_scale + 1e-8), 0.0, 2.0)

        if abs(err) > PHASE_TOL:
            u = -K_PHASE * err * radius_weight
            active = 1
        else:
            u = 0.0
            active = 0

        u = float(np.clip(u, -MAX_CONTROL, MAX_CONTROL))
    else:
        r_now = 0.0
        theta_now = 0.0
        err = 0.0
        u = 0.0
        active = 0

    eff_scale = float(np.clip(raw_scale * (1.0 + u), 0.70, 1.35))
    net_ctrl.load["p_mw"] = base_load * eff_scale

    try:
        pp.runpp(net_ctrl, enforce_q_lims=True, init="results")
        voltages = net_ctrl.res_bus.vm_pu.values
    except Exception:
        voltages = np.ones(len(net_ctrl.bus)) * 0.95

    v_mean, coh = compute_state(voltages)
    sw = compute_switch(ctrl_v)

    ctrl_v.append(v_mean)
    ctrl_x.append(coh)
    ctrl_y.append(sw)

    control_signal.append(u)
    control_active.append(active)
    phase_error_hist.append(err)
    theta_hist.append(theta_now)
    radius_hist.append(r_now)

    if t > 5 and ctrl_v[-2] >= 0.90 and v_mean < 0.90:
        ctrl_events.append(t)

ctrl_v = np.array(ctrl_v)
ctrl_x = np.array(ctrl_x)
ctrl_y = np.array(ctrl_y)
control_signal = np.array(control_signal)
control_active = np.array(control_active)
phase_error_hist = np.array(phase_error_hist)

ctrl_center_x, ctrl_center_y = estimate_center(ctrl_x, ctrl_y, n=25)
ctrl_dx = ctrl_x - ctrl_center_x
ctrl_dy = ctrl_y - ctrl_center_y
ctrl_r = np.sqrt(ctrl_dx**2 + ctrl_dy**2)
ctrl_theta = np.arctan2(ctrl_dy, ctrl_dx)

# adaptive lock "escape-like" deviation = phase error outside tolerance and high radius
ctrl_phase_err = wrapped_angle_diff(ctrl_theta, theta_target)
ctrl_escape_mask = (np.abs(ctrl_phase_err) > PHASE_TOL) & (ctrl_r > np.quantile(ctrl_r, 0.75))
base_phase_err = wrapped_angle_diff(baseline_theta, theta_target)
base_escape_mask = (np.abs(base_phase_err) > PHASE_TOL) & (baseline_r > np.quantile(baseline_r, 0.75))


# =========================
# 5. Metrics / report
# =========================

def first_or_none(events):
    return events[0] if len(events) > 0 else None

base_first = first_or_none(baseline_events)
ctrl_first = first_or_none(ctrl_events)
shift = None if (base_first is None or ctrl_first is None) else (ctrl_first - base_first)

report_lines = [
    "===== NEXAH ADAPTIVE PHASE LOCK REPORT =====",
    "",
    f"Baseline mean radius: {baseline_r.mean():.6f}",
    f"Controlled mean radius: {ctrl_r.mean():.6f}",
    "",
    f"Baseline max radius: {baseline_r.max():.6f}",
    f"Controlled max radius: {ctrl_r.max():.6f}",
    "",
    f"Baseline mean coherence: {baseline_x.mean():.6f}",
    f"Controlled mean coherence: {ctrl_x.mean():.6f}",
    "",
    f"Baseline first classical event: {base_first}",
    f"Controlled first classical event: {ctrl_first}",
    f"Collapse shift (controlled - baseline): {shift}",
    "",
    f"Baseline escape count: {int(np.sum(base_escape_mask))}",
    f"Controlled escape count: {int(np.sum(ctrl_escape_mask))}",
    f"Control activation count: {int(np.sum(control_active))}",
    "",
    f"Learned theta_target: {theta_target:.6f} rad ({np.degrees(theta_target):.2f} deg)",
    f"Target radius (median): {r_target:.6f}",
    f"Phase tolerance: {PHASE_TOL:.6f} rad ({np.degrees(PHASE_TOL):.2f} deg)",
    "",
    f"Mean control signal: {control_signal.mean():.6f}",
    f"Max |control signal|: {np.max(np.abs(control_signal)):.6f}",
    "",
    "Interpretation:",
]

if ctrl_x.mean() > baseline_x.mean():
    report_lines.append("- adaptive phase lock improved mean coherence.")
else:
    report_lines.append("- adaptive phase lock did not improve mean coherence.")

if ctrl_r.max() < baseline_r.max():
    report_lines.append("- adaptive phase lock reduced maximum orbit excursion.")
else:
    report_lines.append("- adaptive phase lock did not reduce maximum orbit excursion.")

if np.sum(ctrl_escape_mask) < np.sum(base_escape_mask):
    report_lines.append("- adaptive phase lock reduced escape-like phase deviations.")
elif np.sum(ctrl_escape_mask) > np.sum(base_escape_mask):
    report_lines.append("- adaptive phase lock increased escape-like phase deviations.")
else:
    report_lines.append("- adaptive phase lock kept the same number of escape-like deviations.")

report_text = "\n".join(report_lines)


# =========================
# 6. Plot: time series
# =========================

t = np.arange(TIME_STEPS)
fig1, ax = plt.subplots(5, 1, figsize=(12, 11), sharex=True)

ax[0].plot(t, baseline_v, label="Baseline", alpha=0.9)
ax[0].plot(t, ctrl_v, label="Controlled", alpha=0.9)
ax[0].axhline(0.90, linestyle="--", color="gray", alpha=0.8, label="Classical threshold")
if base_first is not None:
    ax[0].axvline(base_first, linestyle="--", color="tab:blue", alpha=0.7)
if ctrl_first is not None:
    ax[0].axvline(ctrl_first, linestyle="--", color="tab:orange", alpha=0.7)
ax[0].set_ylabel("Voltage mean")
ax[0].legend(loc="best")
ax[0].grid(True)

ax[1].plot(t, baseline_x, label="Baseline")
ax[1].plot(t, ctrl_x, label="Controlled")
ax[1].set_ylabel("Coherence")
ax[1].grid(True)

ax[2].plot(t, baseline_y, label="Baseline")
ax[2].plot(t, ctrl_y, label="Controlled")
ax[2].set_ylabel("Switch")
ax[2].grid(True)

ax[3].plot(t, ctrl_phase_err, color="purple", label="Phase error")
ax[3].axhline(PHASE_TOL, linestyle="--", color="gray", alpha=0.7)
ax[3].axhline(-PHASE_TOL, linestyle="--", color="gray", alpha=0.7)
ax[3].set_ylabel("Phase err")
ax[3].legend(loc="best")
ax[3].grid(True)

ax[4].plot(t, control_signal, color="black", label="Control signal")
ax[4].fill_between(t, 0, control_signal, where=control_active > 0, alpha=0.25, color="black", label="Active control")
ax[4].set_ylabel("u(t)")
ax[4].set_xlabel("Time step")
ax[4].legend(loc="best")
ax[4].grid(True)

fig1.suptitle("NEXAH v12 — Adaptive Phase Lock (Time Series)")
fig1.tight_layout()


# =========================
# 7. Plot: phase space
# =========================

fig2, ax2 = plt.subplots(figsize=(10, 8))

ax2.plot(baseline_x, baseline_y, color="lightsteelblue", linewidth=2.0, alpha=0.8, label="Baseline trajectory")
ax2.plot(ctrl_x, ctrl_y, color="orange", linewidth=2.0, alpha=0.85, label="Controlled trajectory")

ax2.scatter(
    baseline_x[base_escape_mask],
    baseline_y[base_escape_mask],
    facecolors="none",
    edgecolors="tab:blue",
    s=100,
    linewidths=1.4,
    label="Baseline escape region",
)

ax2.scatter(
    ctrl_x[ctrl_escape_mask],
    ctrl_y[ctrl_escape_mask],
    facecolors="none",
    edgecolors="tab:orange",
    s=100,
    linewidths=1.4,
    label="Controlled escape region",
)

ax2.scatter(ctrl_center_x, ctrl_center_y, color="gold", marker="*", s=220, label="Stability center")
ax2.scatter(baseline_x[0], baseline_y[0], color="green", s=90, label="Start")
ax2.scatter(baseline_x[-1], baseline_y[-1], color="red", s=90, label="Baseline end")
ax2.scatter(ctrl_x[-1], ctrl_y[-1], color="purple", s=90, label="Controlled end")

ax2.set_title("NEXAH v12 — Adaptive Phase Lock (Phase Space)")
ax2.set_xlabel("Coherence")
ax2.set_ylabel("Switch signal")
ax2.grid(True)
ax2.legend(loc="best")


# =========================
# 8. Plot: polar
# =========================

fig3 = plt.figure(figsize=(10, 10))
ax3 = fig3.add_subplot(111, projection="polar")

def normalize_radius(r):
    return (r - np.min(r)) / (np.max(r) - np.min(r) + 1e-8)

r_base_n = normalize_radius(baseline_r)
r_ctrl_n = normalize_radius(ctrl_r)

theta_base_plot = np.mod(np.linspace(0, 2 * np.pi * 3, TIME_STEPS), 2 * np.pi)
theta_ctrl_plot = np.mod(np.linspace(0, 2 * np.pi * 3, TIME_STEPS), 2 * np.pi)

ax3.plot(theta_base_plot, r_base_n, color="lightsteelblue", linewidth=1.8, alpha=0.8, label="Baseline")
ax3.plot(theta_ctrl_plot, r_ctrl_n, color="orange", linewidth=1.8, alpha=0.9, label="Controlled")

ax3.scatter(
    theta_base_plot[base_escape_mask],
    r_base_n[base_escape_mask],
    facecolors="none",
    edgecolors="tab:blue",
    s=90,
    linewidths=1.3,
)

ax3.scatter(
    theta_ctrl_plot[ctrl_escape_mask],
    r_ctrl_n[ctrl_escape_mask],
    facecolors="none",
    edgecolors="tab:orange",
    s=90,
    linewidths=1.3,
)

# learned target phase line
theta_target_plot = theta_target if theta_target >= 0 else theta_target + 2 * np.pi
ax3.plot(
    [theta_target_plot, theta_target_plot],
    [0.0, 1.0],
    linestyle="--",
    color="black",
    alpha=0.7,
    label="Learned phase target"
)

ax3.scatter(theta_base_plot[0], r_base_n[0], color="green", s=90, label="Start")
ax3.scatter(theta_base_plot[-1], r_base_n[-1], color="red", s=90, label="Baseline end")
ax3.scatter(theta_ctrl_plot[-1], r_ctrl_n[-1], color="purple", s=90, label="Controlled end")

ax3.set_title("NEXAH v12 — Adaptive Phase Lock (Polar)")
ax3.legend(loc="upper right")


# =========================
# 9. Save / print
# =========================

(fig1_path := RESULT_PATH / "ieee57_v12_adaptive_phase_timeseries.png")
(fig2_path := RESULT_PATH / "ieee57_v12_adaptive_phase_phase_space.png")
(fig3_path := RESULT_PATH / "ieee57_v12_adaptive_phase_polar.png")
(report_path := RESULT_PATH / "ieee57_v12_adaptive_phase_report.txt")

fig1.savefig(fig1_path, dpi=200)
fig2.savefig(fig2_path, dpi=200)
fig3.savefig(fig3_path, dpi=200)
report_path.write_text(report_text, encoding="utf-8")

plt.close(fig1)
plt.close(fig2)
plt.close(fig3)

print(report_text)
print("\nSaved:")
print(f"  • {fig1_path}")
print(f"  • {fig2_path}")
print(f"  • {fig3_path}")
print(f"  • {report_path}")
