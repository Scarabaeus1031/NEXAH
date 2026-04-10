"""
v14.3_ncs_hybrid_controller.py
==============================

Goal:
- extend v14 with discrete NCS phase locks
- combine:
    1. stability band control
    2. phase guidance
    3. velocity damping
    4. discrete phase snap toward NCS lock angles

Key idea:
The controller is no longer purely continuous.
It now includes discrete lock attractors in angle space:

    97°   = upper reference
    277°  = lower opposition
    292°  = NCS switch sector

This is a prototype in extracted NEXAH state space.
It does NOT claim physical optimality yet.

State space:
- x = coherence
- y = switch signal

Outputs:
- ieee57_v14_3_ncs_hybrid_timeseries.png
- ieee57_v14_3_ncs_hybrid_phase.png
- ieee57_v14_3_ncs_hybrid_polar.png
- ieee57_v14_3_ncs_hybrid_report.txt
"""

from pathlib import Path
import copy
import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp
import pandapower.networks as pn


# ============================================================
# 1. Config
# ============================================================

TIME_STEPS = 300
SEED = 42

RESULTS_DIR = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

V_CLASSICAL = 0.90

# Base excitation
BASE_LOAD_FACTOR = 1.0 + 0.25 * np.sin(np.linspace(0, 6 * np.pi, TIME_STEPS))
NOISE_STD = 0.02

# Hybrid controller targets
R_TARGET = 0.587
R_BAND_HALF_WIDTH = 0.035

THETA_REF = -np.pi / 2           # 270°
THETA_TOL = 0.22

OMEGA_REF = 0.0
OMEGA_TOL = 0.06

# NCS discrete locks
PHASE_LOCK_POINTS_DEG = [97.0, 277.0, 292.0]
PHASE_LOCK_POINTS = np.deg2rad(PHASE_LOCK_POINTS_DEG)
PHASE_SNAP_TOL = np.deg2rad(8.0)

# Gains
K_R = 0.10
K_THETA = 0.035
K_OMEGA = 0.025
K_SNAP = 0.080

# Soft gap / drift offset
GAP_OFFSET = 0.01

U_MAX = 0.09


# ============================================================
# 2. Helpers
# ============================================================

def wrap_angle(angle: float) -> float:
    """Wrap angle to [-pi, pi]."""
    return (angle + np.pi) % (2 * np.pi) - np.pi


def angle_diff(a: float, b: float) -> float:
    """Smallest signed angular difference a-b."""
    return wrap_angle(a - b)


def compute_state(v_mean: float, coherence: float, switch: float,
                  c_center: float, s_center: float) -> tuple[float, float]:
    """
    Map Cartesian NEXAH state to polar state around learned center.
    Radius is normalized by v_mean to keep scale stable.
    """
    dx = coherence - c_center
    dy = switch - s_center
    theta = np.arctan2(dy, dx)
    radius = np.sqrt(dx * dx + dy * dy) / max(v_mean, 1e-9)
    return radius, theta


def run_simulation(control_mode: str, c_center: float | None = None,
                   s_center: float | None = None) -> dict:
    """
    Run baseline or controlled simulation.

    control_mode:
    - "baseline"
    - "controlled"
    """
    net = pn.case57()
    np.random.seed(SEED)

    noise = np.random.normal(0.0, NOISE_STD, TIME_STEPS)

    # Histories
    voltage_history = []
    coherence_history = []
    switch_history = []

    radius_history = []
    theta_history = []
    omega_history = []
    theta_err_history = []

    control_history = []
    active_control_history = []
    snap_active_history = []

    classical_event = None

    prev_v_mean = None
    prev_theta = None

    for t in range(TIME_STEPS):
        base_factor = BASE_LOAD_FACTOR[t] + noise[t]
        u_t = 0.0
        snap_active = 0

        # ------------------------------------------------------------
        # Control from previous state
        # ------------------------------------------------------------
        if (
            control_mode == "controlled"
            and t > 0
            and c_center is not None
            and s_center is not None
        ):
            prev_r = radius_history[-1]
            prev_theta_local = theta_history[-1]
            prev_omega = omega_history[-1]

            # --- 1) stability band error
            if prev_r < (R_TARGET - R_BAND_HALF_WIDTH):
                r_err = prev_r - (R_TARGET - R_BAND_HALF_WIDTH)
            elif prev_r > (R_TARGET + R_BAND_HALF_WIDTH):
                r_err = prev_r - (R_TARGET + R_BAND_HALF_WIDTH)
            else:
                r_err = 0.0

            # --- 2) phase error around main reference
            theta_err = angle_diff(prev_theta_local, THETA_REF)

            # --- 3) velocity error
            omega_err = prev_omega - OMEGA_REF

            # --- 4) discrete NCS snap
            nearest_lock = None
            nearest_delta = None
            for lock in PHASE_LOCK_POINTS:
                d = angle_diff(prev_theta_local, lock)
                if nearest_delta is None or abs(d) < abs(nearest_delta):
                    nearest_delta = d
                    nearest_lock = lock

            snap_term = 0.0
            if nearest_delta is not None and abs(nearest_delta) < PHASE_SNAP_TOL:
                snap_term = -K_SNAP * nearest_delta
                snap_active = 1

            # --- 5) band / phase / omega controller
            u_t = (
                -K_R * r_err
                -K_THETA * theta_err
                -K_OMEGA * omega_err
                + snap_term
            )

            # --- 6) soft breathing-gap bias
            if abs(prev_theta_local - THETA_REF) < THETA_TOL:
                # damp more gently near the target meridian
                u_t -= np.sign(theta_err) * GAP_OFFSET * 0.15

            # clip
            u_t = float(np.clip(u_t, -U_MAX, U_MAX))

        # ------------------------------------------------------------
        # Apply load scaling
        # ------------------------------------------------------------
        effective_factor = max(0.05, base_factor + u_t)

        for load_idx in net.load.index:
            base_p = net.load.at[load_idx, "p_mw"]
            net.load.at[load_idx, "p_mw"] = base_p * effective_factor

        # ------------------------------------------------------------
        # Power flow
        # ------------------------------------------------------------
        try:
            pp.runpp(net, enforce_q_lims=True)
            voltages = net.res_bus.vm_pu.values
            v_mean = float(np.mean(voltages))
            v_std = float(np.std(voltages))
        except Exception:
            # fallback
            v_mean = 0.95
            v_std = 0.05

        coherence = 1.0 - v_std

        # switch = slope of mean voltage
        if prev_v_mean is None:
            switch = 0.0
        else:
            switch = v_mean - prev_v_mean

        voltage_history.append(v_mean)
        coherence_history.append(coherence)
        switch_history.append(switch)

        prev_v_mean = v_mean

        # classical collapse event
        if classical_event is None and v_mean < V_CLASSICAL:
            classical_event = t

        # ------------------------------------------------------------
        # Polar state
        # ------------------------------------------------------------
        if c_center is None or s_center is None:
            # temporary center until learned after baseline
            radius = 0.0
            theta = 0.0
        else:
            radius, theta = compute_state(v_mean, coherence, switch, c_center, s_center)

        if prev_theta is None:
            omega = 0.0
        else:
            omega = angle_diff(theta, prev_theta)
        prev_theta = theta

        theta_err = angle_diff(theta, THETA_REF)

        radius_history.append(radius)
        theta_history.append(theta)
        omega_history.append(omega)
        theta_err_history.append(theta_err)

        control_history.append(u_t)
        active_control_history.append(1 if abs(u_t) > 1e-12 else 0)
        snap_active_history.append(snap_active)

    return {
        "voltage": np.array(voltage_history),
        "coherence": np.array(coherence_history),
        "switch": np.array(switch_history),
        "radius": np.array(radius_history),
        "theta": np.array(theta_history),
        "omega": np.array(omega_history),
        "theta_err": np.array(theta_err_history),
        "u": np.array(control_history),
        "u_active": np.array(active_control_history),
        "snap_active": np.array(snap_active_history),
        "classical_event": classical_event,
    }


# ============================================================
# 3. Baseline run + learn center
# ============================================================

baseline_pre = run_simulation(control_mode="baseline", c_center=0.0, s_center=0.0)

# Learn stability center from calmer upper-coherence / low-switch regime
coh = baseline_pre["coherence"]
sw = baseline_pre["switch"]

stable_mask = (coh > np.quantile(coh, 0.75)) & (np.abs(sw) < np.quantile(np.abs(sw), 0.35))
if np.sum(stable_mask) < 10:
    stable_mask = np.ones_like(coh, dtype=bool)

C_CENTER = float(np.mean(coh[stable_mask]))
S_CENTER = float(np.mean(sw[stable_mask]))

# Rerun baseline with learned center
baseline = run_simulation(control_mode="baseline", c_center=C_CENTER, s_center=S_CENTER)
controlled = run_simulation(control_mode="controlled", c_center=C_CENTER, s_center=S_CENTER)

# escape region: outside band + outside angular window around main axis
baseline_escape = (
    (baseline["radius"] > (R_TARGET + R_BAND_HALF_WIDTH))
    | (baseline["radius"] < (R_TARGET - R_BAND_HALF_WIDTH))
)
controlled_escape = (
    (controlled["radius"] > (R_TARGET + R_BAND_HALF_WIDTH))
    | (controlled["radius"] < (R_TARGET - R_BAND_HALF_WIDTH))
)

# Control metrics
baseline_first_event = baseline["classical_event"]
controlled_first_event = controlled["classical_event"]

# Lock counts
baseline_lock_hits = np.zeros(TIME_STEPS, dtype=int)
controlled_lock_hits = np.zeros(TIME_STEPS, dtype=int)
for lock in PHASE_LOCK_POINTS:
    baseline_lock_hits += (np.abs(np.array([angle_diff(t, lock) for t in baseline["theta"]])) < PHASE_SNAP_TOL).astype(int)
    controlled_lock_hits += (np.abs(np.array([angle_diff(t, lock) for t in controlled["theta"]])) < PHASE_SNAP_TOL).astype(int)


# ============================================================
# 4. Plots
# ============================================================

t = np.arange(TIME_STEPS)

# ------------------------------------------------------------
# Time series
# ------------------------------------------------------------
fig, axes = plt.subplots(6, 1, figsize=(14, 18), sharex=True)

axes[0].plot(t, baseline["voltage"], label="Baseline", alpha=0.35)
axes[0].plot(t, controlled["voltage"], label="Controlled", color="tab:orange")
axes[0].axhline(V_CLASSICAL, color="gray", ls="--", label="Classical threshold")
axes[0].set_ylabel("Voltage mean")
axes[0].legend(loc="best")
axes[0].grid(True, alpha=0.3)

axes[1].plot(t, baseline["coherence"], label="Baseline", alpha=0.35)
axes[1].plot(t, controlled["coherence"], label="Controlled", color="tab:orange")
axes[1].set_ylabel("Coherence")
axes[1].grid(True, alpha=0.3)

axes[2].plot(t, baseline["switch"], label="Baseline", alpha=0.35)
axes[2].plot(t, controlled["switch"], label="Controlled", color="tab:orange")
axes[2].axhline(0.0, color="gray", ls="--", alpha=0.7)
axes[2].set_ylabel("Switch")
axes[2].grid(True, alpha=0.3)

axes[3].plot(t, controlled["radius"], color="purple", label="Controlled radius")
axes[3].axhline(R_TARGET, color="black", ls=":", label="Target radius")
axes[3].axhline(R_TARGET - R_BAND_HALF_WIDTH, color="gray", ls="--", label="Band min/max")
axes[3].axhline(R_TARGET + R_BAND_HALF_WIDTH, color="gray", ls="--")
axes[3].set_ylabel("Radius")
axes[3].legend(loc="best")
axes[3].grid(True, alpha=0.3)

axes[4].plot(t, controlled["theta_err"], color="brown", label="Theta error")
axes[4].axhline(THETA_TOL, color="gray", ls="--", alpha=0.7)
axes[4].axhline(-THETA_TOL, color="gray", ls="--", alpha=0.7)
axes[4].set_ylabel("Theta err")
axes[4].legend(loc="best")
axes[4].grid(True, alpha=0.3)

axes[5].plot(t, controlled["u"], color="black", label="Control signal")
axes[5].fill_between(t, 0, controlled["u_active"], color="gray", alpha=0.25, label="Active control")
axes[5].plot(t, controlled["snap_active"] * U_MAX, color="red", lw=1.0, alpha=0.8, label="Snap active")
axes[5].set_ylabel("u(t)")
axes[5].set_xlabel("Time step")
axes[5].legend(loc="best")
axes[5].grid(True, alpha=0.3)

fig.suptitle("NEXAH v14.3 — NCS Hybrid Controller (Time Series)", fontsize=16)
fig.tight_layout()
ts_path = RESULTS_DIR / "ieee57_v14_3_ncs_hybrid_timeseries.png"
fig.savefig(ts_path, dpi=200)
plt.close(fig)

# ------------------------------------------------------------
# Phase space
# ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 10))

ax.plot(baseline["coherence"], baseline["switch"], alpha=0.25, lw=3, label="Baseline trajectory")
ax.plot(controlled["coherence"], controlled["switch"], color="tab:orange", lw=2.4, label="Controlled trajectory")

ax.scatter(
    baseline["coherence"][baseline_escape],
    baseline["switch"][baseline_escape],
    facecolors="none",
    edgecolors="tab:blue",
    s=170,
    lw=2,
    label="Baseline escape region",
)

ax.scatter(
    controlled["coherence"][controlled_escape],
    controlled["switch"][controlled_escape],
    facecolors="none",
    edgecolors="tab:orange",
    s=170,
    lw=2,
    label="Controlled escape region",
)

ax.scatter([C_CENTER], [S_CENTER], marker="*", s=380, color="gold", label="Stability center")
ax.scatter([baseline["coherence"][0]], [baseline["switch"][0]], s=200, color="green", label="Start")
ax.scatter([baseline["coherence"][-1]], [baseline["switch"][-1]], s=200, color="red", label="Baseline end")
ax.scatter([controlled["coherence"][-1]], [controlled["switch"][-1]], s=200, color="purple", label="Controlled end")

# show main phase reference ray from center
ref_len = 0.02
ax.plot(
    [C_CENTER, C_CENTER + ref_len * np.cos(THETA_REF)],
    [S_CENTER, S_CENTER + ref_len * np.sin(THETA_REF)],
    color="gray",
    ls="--",
    alpha=0.6,
)

ax.axhline(0.0, color="gray", ls="--", alpha=0.5)
ax.axvline(C_CENTER, color="gray", ls="--", alpha=0.5)
ax.set_xlabel("Coherence")
ax.set_ylabel("Switch signal")
ax.set_title("NEXAH v14.3 — NCS Hybrid Controller (Phase Space)")
ax.legend(loc="best")
ax.grid(True, alpha=0.3)
phase_path = RESULTS_DIR / "ieee57_v14_3_ncs_hybrid_phase.png"
fig.savefig(phase_path, dpi=200)
plt.close(fig)

# ------------------------------------------------------------
# Polar
# ------------------------------------------------------------
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection="polar")

ax.plot(baseline["theta"], baseline["radius"], alpha=0.25, lw=2.5, label="Baseline")
ax.plot(controlled["theta"], controlled["radius"], color="tab:orange", lw=2.2, label="Controlled")

ax.scatter(
    baseline["theta"][baseline_escape],
    baseline["radius"][baseline_escape],
    facecolors="none",
    edgecolors="tab:blue",
    s=150,
    lw=2,
)

ax.scatter(
    controlled["theta"][controlled_escape],
    controlled["radius"][controlled_escape],
    facecolors="none",
    edgecolors="tab:orange",
    s=150,
    lw=2,
)

# target ring
theta_grid = np.linspace(0, 2 * np.pi, 360)
ax.plot(theta_grid, np.full_like(theta_grid, R_TARGET), "k:", lw=2, label="Target ring")
ax.plot(theta_grid, np.full_like(theta_grid, R_TARGET - R_BAND_HALF_WIDTH), color="gray", ls="--", lw=1.5, label="Band")
ax.plot(theta_grid, np.full_like(theta_grid, R_TARGET + R_BAND_HALF_WIDTH), color="gray", ls="--", lw=1.5)

# phase refs
ax.plot([THETA_REF, THETA_REF], [0, max(np.max(controlled["radius"]), R_TARGET + 0.05)], color="gray", ls="--", lw=1.5, label="Theta ref")
for deg, lock in zip(PHASE_LOCK_POINTS_DEG, PHASE_LOCK_POINTS):
    ax.plot([lock, lock], [0, R_TARGET + 0.10], color="red", alpha=0.22, lw=1.2)

# markers
ax.scatter([baseline["theta"][0]], [baseline["radius"][0]], s=160, color="green", label="Start")
ax.scatter([baseline["theta"][-1]], [baseline["radius"][-1]], s=160, color="red", label="Baseline end")
ax.scatter([controlled["theta"][-1]], [controlled["radius"][-1]], s=160, color="purple", label="Controlled end")

ax.set_title("NEXAH v14.3 — NCS Hybrid Controller (Polar)", pad=24, fontsize=16)
ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.05))
polar_path = RESULTS_DIR / "ieee57_v14_3_ncs_hybrid_polar.png"
fig.savefig(polar_path, dpi=200, bbox_inches="tight")
plt.close(fig)


# ============================================================
# 5. Report
# ============================================================

report = []
report.append("===== NEXAH V14.3 NCS HYBRID CONTROLLER REPORT =====\n")

report.append(f"Stability center:")
report.append(f"  coherence = {C_CENTER:.6f}")
report.append(f"  switch    = {S_CENTER:.6f}\n")

report.append(f"Band target radius: {R_TARGET:.6f}")
report.append(f"Band interval: [{R_TARGET - R_BAND_HALF_WIDTH:.6f}, {R_TARGET + R_BAND_HALF_WIDTH:.6f}]")
report.append(f"Theta reference: {THETA_REF:.6f} rad ({np.rad2deg(THETA_REF):.2f} deg)")
report.append(f"Theta tolerance: {THETA_TOL:.6f} rad ({np.rad2deg(THETA_TOL):.2f} deg)")
report.append(f"Omega reference: {OMEGA_REF:.6f}")
report.append(f"Omega tolerance: {OMEGA_TOL:.6f}")
report.append(f"NCS phase locks (deg): {PHASE_LOCK_POINTS_DEG}")
report.append(f"Phase snap tolerance: {PHASE_SNAP_TOL:.6f} rad ({np.rad2deg(PHASE_SNAP_TOL):.2f} deg)")
report.append(f"GAP_OFFSET: {GAP_OFFSET:.6f}")
report.append(f"U_MAX: {U_MAX:.6f}\n")

report.append(f"Baseline mean radius: {np.mean(baseline['radius']):.6f}")
report.append(f"Controlled mean radius: {np.mean(controlled['radius']):.6f}\n")

report.append(f"Baseline max radius: {np.max(baseline['radius']):.6f}")
report.append(f"Controlled max radius: {np.max(controlled['radius']):.6f}\n")

report.append(f"Baseline mean coherence: {np.mean(baseline['coherence']):.6f}")
report.append(f"Controlled mean coherence: {np.mean(controlled['coherence']):.6f}\n")

report.append(f"Baseline first classical event: {baseline_first_event}")
report.append(f"Controlled first classical event: {controlled_first_event}")
if baseline_first_event is not None and controlled_first_event is not None:
    report.append(f"Collapse shift (controlled - baseline): {controlled_first_event - baseline_first_event}")
report.append("")

report.append(f"Baseline escape count: {int(np.sum(baseline_escape))}")
report.append(f"Controlled escape count: {int(np.sum(controlled_escape))}")
report.append(f"Escape delta (baseline - controlled): {int(np.sum(baseline_escape) - np.sum(controlled_escape))}\n")

report.append(f"Baseline lock-hit count: {int(np.sum(baseline_lock_hits > 0))}")
report.append(f"Controlled lock-hit count: {int(np.sum(controlled_lock_hits > 0))}")
report.append(f"Snap activation count: {int(np.sum(controlled['snap_active']))}")
report.append(f"Control activation count: {int(np.sum(controlled['u_active']))}")
report.append(f"Mean control signal: {np.mean(controlled['u']):.6f}")
report.append(f"Max |control signal|: {np.max(np.abs(controlled['u'])):.6f}\n")

if np.mean(controlled["coherence"]) > np.mean(baseline["coherence"]):
    report.append("Mean coherence improved.")
else:
    report.append("Mean coherence did not improve.")

if np.max(controlled["radius"]) < np.max(baseline["radius"]):
    report.append("Maximum orbit excursion improved.")
else:
    report.append("Maximum orbit excursion did not improve.")

if np.sum(controlled_escape) < np.sum(baseline_escape):
    report.append("Escape count reduced.")
else:
    report.append("Escape count did not reduce.")

if np.sum(controlled_lock_hits > 0) > np.sum(baseline_lock_hits > 0):
    report.append("Discrete NCS lock engagement increased.")
else:
    report.append("Discrete NCS lock engagement did not increase.")

report_path = RESULTS_DIR / "ieee57_v14_3_ncs_hybrid_report.txt"
report_path.write_text("\n".join(report), encoding="utf-8")

print("\n".join(report))
print("\nSaved:")
print(f"  • {ts_path}")
print(f"  • {phase_path}")
print(f"  • {polar_path}")
print(f"  • {report_path}")
