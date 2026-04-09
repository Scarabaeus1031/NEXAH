"""
v13_stability_band_controller.py
================================

Goal:
- replace point-lock control with a stability-band controller
- learn a stable annulus / corridor from the baseline run
- intervene only when the system leaves the learned band
- compare:
    1. baseline run
    2. band-controlled run

Core idea:
- learn a stable operating band in NEXAH state space:
    x = coherence
    y = switch signal
- derive:
    * coherence band
    * switch band
    * radius band around empirical center
- apply gentle corrective control only outside the band

This is the first NEXAH-native controller:
- no fixed point lock
- no forced phase pinning
- no hard radial shock
- just soft return into the learned stability corridor

Outputs:
- ieee57_v13_band_timeseries.png
- ieee57_v13_band_phase_space.png
- ieee57_v13_band_polar.png
- ieee57_v13_band_report.txt
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import pandapower as pp
import pandapower.networks as pn


# =========================
# 1. Paths / config
# =========================

BASE_PATH = Path(__file__).resolve().parent
RESULT_PATH = BASE_PATH.parent / "results"
RESULT_PATH.mkdir(parents=True, exist_ok=True)

TIME_STEPS = 300
SEED = 42

BASE_AMPLITUDE = 0.25
NOISE_STD = 0.02

# controller parameters
K_X = 0.60            # coherence correction weight
K_Y = 1.80            # switch damping weight
K_R = 0.35            # radial correction weight
MAX_CONTROL = 0.06    # clip absolute control
DEAD_BAND_SCALE = 1.0 # >1 widens allowed band
RADIUS_GAIN = 0.8     # stronger action farther outside r band


# =========================
# 2. Utilities
# =========================

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


def first_or_none(events):
    return events[0] if len(events) > 0 else None


def outside_interval(val, lo, hi):
    if val < lo:
        return lo - val
    if val > hi:
        return hi - val
    return 0.0


def normalize_radius(r):
    return (r - np.min(r)) / (np.max(r) - np.min(r) + 1e-8)


# =========================
# 3. Forcing
# =========================

np.random.seed(SEED)
load_factor = 1.0 + BASE_AMPLITUDE * np.sin(np.linspace(0, 6 * np.pi, TIME_STEPS))
noise = np.random.normal(0, NOISE_STD, TIME_STEPS)


# =========================
# 4. Baseline simulation
# =========================

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

# learned center + learned bands
center_x, center_y = estimate_center(baseline_x, baseline_y, n=25)

dx_base = baseline_x - center_x
dy_base = baseline_y - center_y
r_base = np.sqrt(dx_base**2 + dy_base**2)
theta_base = np.arctan2(dy_base, dx_base)

# learn stable corridor from baseline distribution
x_lo = float(np.quantile(baseline_x, 0.20))
x_hi = float(np.quantile(baseline_x, 0.80))

y_abs_q = float(np.quantile(np.abs(baseline_y), 0.75))
y_lo = -DEAD_BAND_SCALE * y_abs_q
y_hi = +DEAD_BAND_SCALE * y_abs_q

r_lo = float(np.quantile(r_base, 0.20))
r_hi = float(np.quantile(r_base, 0.80))
r_med = float(np.median(r_base))
r_std = float(np.std(r_base) + 1e-8)

baseline_escape_mask = (
    ((baseline_x < x_lo) | (baseline_x > x_hi)) |
    ((baseline_y < y_lo) | (baseline_y > y_hi)) |
    ((r_base < r_lo) | (r_base > r_hi))
)


# =========================
# 5. Controlled simulation
# =========================

net_ctrl = pn.case57()
net_ctrl.load["p_mw"] = base_load.copy()

ctrl_v = []
ctrl_x = []
ctrl_y = []
ctrl_events = []

control_signal = []
control_active = []
band_violation = []

for t in range(TIME_STEPS):
    raw_scale = float(np.clip(load_factor[t] + noise[t], 0.70, 1.35))

    # compute control from previous state
    if len(ctrl_x) >= 5:
        x_now = ctrl_x[-1]
        y_now = ctrl_y[-1]

        c_x, c_y = estimate_center(np.array(ctrl_x), np.array(ctrl_y), n=25)
        dx = x_now - c_x
        dy = y_now - c_y
        r_now = float(np.sqrt(dx * dx + dy * dy))

        ex = outside_interval(x_now, x_lo, x_hi)
        ey = outside_interval(y_now, y_lo, y_hi)
        er = outside_interval(r_now, r_lo, r_hi)

        violation = abs(ex) + abs(ey) + abs(er)
        band_violation.append(violation)

        if violation > 0:
            # soft guidance:
            # - if coherence too low, reduce load
            # - if switch magnitude too high, reduce load in proportion
            # - if radius too large, reduce load gently
            radius_weight = 1.0 + RADIUS_GAIN * np.clip((r_now - r_med) / (r_std + 1e-8), 0.0, 2.0)

            u = (
                -K_X * ex
                -K_Y * ey
                -K_R * er * radius_weight
            )
            active = 1
        else:
            u = 0.0
            active = 0

        u = float(np.clip(u, -MAX_CONTROL, MAX_CONTROL))
    else:
        u = 0.0
        active = 0
        band_violation.append(0.0)

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

    if t > 5 and ctrl_v[-2] >= 0.90 and v_mean < 0.90:
        ctrl_events.append(t)

ctrl_v = np.array(ctrl_v)
ctrl_x = np.array(ctrl_x)
ctrl_y = np.array(ctrl_y)
control_signal = np.array(control_signal)
control_active = np.array(control_active)
band_violation = np.array(band_violation)

ctrl_center_x, ctrl_center_y = estimate_center(ctrl_x, ctrl_y, n=25)
dx_ctrl = ctrl_x - ctrl_center_x
dy_ctrl = ctrl_y - ctrl_center_y
r_ctrl = np.sqrt(dx_ctrl**2 + dy_ctrl**2)
theta_ctrl = np.arctan2(dy_ctrl, dx_ctrl)

ctrl_escape_mask = (
    ((ctrl_x < x_lo) | (ctrl_x > x_hi)) |
    ((ctrl_y < y_lo) | (ctrl_y > y_hi)) |
    ((r_ctrl < r_lo) | (r_ctrl > r_hi))
)


# =========================
# 6. Metrics / report
# =========================

base_first = first_or_none(baseline_events)
ctrl_first = first_or_none(ctrl_events)
collapse_shift = None if (base_first is None or ctrl_first is None) else (ctrl_first - base_first)

report_lines = [
    "===== NEXAH STABILITY BAND CONTROLLER REPORT =====",
    "",
    f"Baseline mean radius: {r_base.mean():.6f}",
    f"Controlled mean radius: {r_ctrl.mean():.6f}",
    "",
    f"Baseline max radius: {r_base.max():.6f}",
    f"Controlled max radius: {r_ctrl.max():.6f}",
    "",
    f"Baseline mean coherence: {baseline_x.mean():.6f}",
    f"Controlled mean coherence: {ctrl_x.mean():.6f}",
    "",
    f"Baseline first classical event: {base_first}",
    f"Controlled first classical event: {ctrl_first}",
    f"Collapse shift (controlled - baseline): {collapse_shift}",
    "",
    f"Baseline escape count: {int(np.sum(baseline_escape_mask))}",
    f"Controlled escape count: {int(np.sum(ctrl_escape_mask))}",
    f"Control activation count: {int(np.sum(control_active))}",
    "",
    f"Learned coherence band: [{x_lo:.6f}, {x_hi:.6f}]",
    f"Learned switch band:    [{y_lo:.6f}, {y_hi:.6f}]",
    f"Learned radius band:    [{r_lo:.6f}, {r_hi:.6f}]",
    f"Empirical center:       ({center_x:.6f}, {center_y:.6f})",
    "",
    f"Mean control signal: {control_signal.mean():.6f}",
    f"Max |control signal|: {np.max(np.abs(control_signal)):.6f}",
    "",
    "Interpretation:",
]

if ctrl_x.mean() > baseline_x.mean():
    report_lines.append("- stability band control improved mean coherence.")
else:
    report_lines.append("- stability band control did not improve mean coherence.")

if r_ctrl.max() < r_base.max():
    report_lines.append("- stability band control reduced maximum orbit excursion.")
else:
    report_lines.append("- stability band control did not reduce maximum orbit excursion.")

if np.sum(ctrl_escape_mask) < np.sum(baseline_escape_mask):
    report_lines.append("- stability band control reduced escape-like states.")
elif np.sum(ctrl_escape_mask) > np.sum(baseline_escape_mask):
    report_lines.append("- stability band control increased escape-like states.")
else:
    report_lines.append("- stability band control kept the same number of escape-like states.")

if collapse_shift is None:
    report_lines.append("- collapse shift could not be computed.")
elif collapse_shift > 0:
    report_lines.append(f"- controller delayed first classical collapse by {collapse_shift} steps.")
elif collapse_shift < 0:
    report_lines.append(f"- controller accelerated first classical collapse by {-collapse_shift} steps.")
else:
    report_lines.append("- controller left first classical collapse timing unchanged.")

report_text = "\n".join(report_lines)


# =========================
# 7. Plot — time series
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
ax[1].axhline(x_lo, linestyle="--", color="gray", alpha=0.6)
ax[1].axhline(x_hi, linestyle="--", color="gray", alpha=0.6)
ax[1].set_ylabel("Coherence")
ax[1].grid(True)

ax[2].plot(t, baseline_y, label="Baseline")
ax[2].plot(t, ctrl_y, label="Controlled")
ax[2].axhline(y_lo, linestyle="--", color="gray", alpha=0.6)
ax[2].axhline(y_hi, linestyle="--", color="gray", alpha=0.6)
ax[2].set_ylabel("Switch")
ax[2].grid(True)

ax[3].plot(t, band_violation, color="purple", label="Band violation")
ax[3].set_ylabel("Violation")
ax[3].legend(loc="best")
ax[3].grid(True)

ax[4].plot(t, control_signal, color="black", label="Control signal")
ax[4].fill_between(t, 0, control_signal, where=control_active > 0, alpha=0.25, color="black", label="Active control")
ax[4].set_ylabel("u(t)")
ax[4].set_xlabel("Time step")
ax[4].legend(loc="best")
ax[4].grid(True)

fig1.suptitle("NEXAH v13 — Stability Band Controller (Time Series)")
fig1.tight_layout()


# =========================
# 8. Plot — phase space
# =========================

fig2, ax2 = plt.subplots(figsize=(10, 8))

ax2.plot(baseline_x, baseline_y, color="lightsteelblue", linewidth=2.0, alpha=0.8, label="Baseline trajectory")
ax2.plot(ctrl_x, ctrl_y, color="orange", linewidth=2.0, alpha=0.85, label="Controlled trajectory")

ax2.scatter(
    baseline_x[baseline_escape_mask],
    baseline_y[baseline_escape_mask],
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

# learned band rectangle
ax2.plot([x_lo, x_hi, x_hi, x_lo, x_lo], [y_lo, y_lo, y_hi, y_hi, y_lo],
         linestyle="--", color="gray", alpha=0.7, label="Learned stability band")

ax2.scatter(center_x, center_y, color="gold", marker="*", s=220, label="Stability center")
ax2.scatter(baseline_x[0], baseline_y[0], color="green", s=90, label="Start")
ax2.scatter(baseline_x[-1], baseline_y[-1], color="red", s=90, label="Baseline end")
ax2.scatter(ctrl_x[-1], ctrl_y[-1], color="purple", s=90, label="Controlled end")

ax2.set_title("NEXAH v13 — Stability Band Controller (Phase Space)")
ax2.set_xlabel("Coherence")
ax2.set_ylabel("Switch signal")
ax2.grid(True)
ax2.legend(loc="best")


# =========================
# 9. Plot — polar
# =========================

fig3 = plt.figure(figsize=(10, 10))
ax3 = fig3.add_subplot(111, projection="polar")

r_base_n = normalize_radius(r_base)
r_ctrl_n = normalize_radius(r_ctrl)

theta_base_plot = np.mod(np.linspace(0, 2 * np.pi * 3, TIME_STEPS), 2 * np.pi)
theta_ctrl_plot = np.mod(np.linspace(0, 2 * np.pi * 3, TIME_STEPS), 2 * np.pi)

ax3.plot(theta_base_plot, r_base_n, color="lightsteelblue", linewidth=1.8, alpha=0.8, label="Baseline")
ax3.plot(theta_ctrl_plot, r_ctrl_n, color="orange", linewidth=1.8, alpha=0.9, label="Controlled")

ax3.scatter(
    theta_base_plot[baseline_escape_mask],
    r_base_n[baseline_escape_mask],
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

ax3.scatter(theta_base_plot[0], r_base_n[0], color="green", s=90, label="Start")
ax3.scatter(theta_base_plot[-1], r_base_n[-1], color="red", s=90, label="Baseline end")
ax3.scatter(theta_ctrl_plot[-1], r_ctrl_n[-1], color="purple", s=90, label="Controlled end")

ax3.set_title("NEXAH v13 — Stability Band Controller (Polar)")
ax3.legend(loc="upper right")


# =========================
# 10. Save / print
# =========================

fig1_path = RESULT_PATH / "ieee57_v13_band_timeseries.png"
fig2_path = RESULT_PATH / "ieee57_v13_band_phase_space.png"
fig3_path = RESULT_PATH / "ieee57_v13_band_polar.png"
report_path = RESULT_PATH / "ieee57_v13_band_report.txt"

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
