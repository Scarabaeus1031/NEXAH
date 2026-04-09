"""
v10_closed_loop_control.py
==========================

Goal:
- close the loop: use the NEXAH navigation policy to modify the system dynamics
- compare:
    1. baseline run
    2. closed-loop controlled run
- test whether the intervention keeps the trajectory closer to the basin

IMPORTANT:
This is still a prototype controller.
It does not claim physical optimality.
It applies a lightweight control action when the system enters an escape-prone region.

State space:
- x = coherence
- y = switch signal

Control idea:
- detect escape-prone region in NEXAH state space
- apply a corrective action to the load scaling
- compare baseline vs controlled dynamics

Outputs:
- ieee57_v10_closed_loop_timeseries.png
- ieee57_v10_closed_loop_phase.png
- ieee57_v10_closed_loop_polar.png
- ieee57_v10_closed_loop_report.txt
"""

import pandapower as pp
import pandapower.networks as pn
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# =========================
# 1. Helpers
# =========================

def simulate_case57(
    time_steps: int = 300,
    seed: int = 42,
    control_enabled: bool = False,
    control_strength: float = 0.10,
):
    """
    Run IEEE 57 baseline or controlled simulation.

    Returns a dict with:
    - voltage_mean
    - coherence
    - switch
    - classical_events
    - escape_mask
    - control_signal
    - control_active
    - phase_x
    - phase_y
    """

    np.random.seed(seed)
    net = pn.case57()

    # store original loads so we do not compound scaling destructively
    base_p = net.load["p_mw"].to_numpy(copy=True)

    load_factor = 1.0 + 0.25 * np.sin(np.linspace(0, 6 * np.pi, time_steps))
    noise = np.random.normal(0, 0.02, time_steps)

    voltage_history = []
    coherence_history = []
    switch_signal = []
    classical_events = []

    control_signal = []
    control_active = []

    # empirical stability center will be estimated online from early history
    center_x = None
    center_y = 0.0

    for t in range(time_steps):
        raw_scale = load_factor[t] + noise[t]

        # -------------------------
        # tentative control policy
        # -------------------------
        u_t = 0.0
        active = 0

        if control_enabled and len(coherence_history) > 20:
            x_hist = np.array(coherence_history)
            y_hist = np.array(switch_signal)

            x = x_hist[-1]
            y = y_hist[-1]

            if center_x is None:
                center_x = np.mean(x_hist[:20])

            dx = x - center_x
            dy = y - center_y

            r = np.sqrt(dx * dx + dy * dy)
            theta = np.arctan2(dy, dx)

            # escape-prone sector:
            # lower-right / lower band, matching prior v8-v9 observations
            in_escape_sector = (-3 * np.pi / 4 < theta < -np.pi / 4)

            # use high radius relative to recent orbit as proxy
            r_recent = np.sqrt((x_hist - center_x) ** 2 + (y_hist - center_y) ** 2)
            r_thresh = np.percentile(r_recent, 75)

            outward_like = r > r_thresh
            switch_large = abs(y) > np.percentile(np.abs(y_hist[-50:]), 75)

            if in_escape_sector and outward_like and switch_large:
                # reduce effective load stress
                # negative u_t = load relief
                u_t = -control_strength
                active = 1

        # controlled scale
        effective_scale = raw_scale * (1.0 + u_t)

        # keep scale in a safe numerical band
        effective_scale = float(np.clip(effective_scale, 0.70, 1.35))

        # apply load profile relative to original base load
        net.load["p_mw"] = base_p * effective_scale

        # run PF
        try:
            pp.runpp(net, enforce_q_lims=True, init="results")
            voltages = net.res_bus.vm_pu.values
        except Exception:
            voltages = np.ones(len(net.bus)) * 0.95

        v_mean = float(np.mean(voltages))
        v_std = float(np.std(voltages))
        coherence = 1.0 - v_std

        voltage_history.append(v_mean)
        coherence_history.append(coherence)

        if len(voltage_history) > 2:
            sw = float(np.gradient(voltage_history)[-1])
        else:
            sw = 0.0
        switch_signal.append(sw)

        # classical collapse event: crossing below 0.90
        if t > 5 and voltage_history[-2] >= 0.90 and v_mean < 0.90:
            classical_events.append(t)

        control_signal.append(u_t)
        control_active.append(active)

    # -------------------------
    # final phase-space analysis
    # -------------------------
    x = np.array(coherence_history)
    y = np.array(switch_signal)

    center_x = float(np.mean(x[:20]))
    center_y = 0.0

    dx = x - center_x
    dy = y - center_y
    r = np.sqrt(dx**2 + dy**2)
    theta = np.arctan2(dy, dx)

    escape_mask = (
        (theta > -3 * np.pi / 4)
        & (theta < -np.pi / 4)
        & (r > np.percentile(r, 75))
    )

    return {
        "voltage_mean": np.array(voltage_history),
        "coherence": np.array(coherence_history),
        "switch": np.array(switch_signal),
        "classical_events": classical_events,
        "escape_mask": escape_mask,
        "control_signal": np.array(control_signal),
        "control_active": np.array(control_active),
        "phase_x": x,
        "phase_y": y,
        "center_x": center_x,
        "center_y": center_y,
        "radius": r,
        "theta": theta,
    }


# =========================
# 2. Run baseline + control
# =========================

TIME_STEPS = 300
SEED = 42
CONTROL_STRENGTH = 0.10

baseline = simulate_case57(
    time_steps=TIME_STEPS,
    seed=SEED,
    control_enabled=False,
    control_strength=CONTROL_STRENGTH,
)

controlled = simulate_case57(
    time_steps=TIME_STEPS,
    seed=SEED,
    control_enabled=True,
    control_strength=CONTROL_STRENGTH,
)


# =========================
# 3. Metrics
# =========================

def first_event_or_none(events):
    return events[0] if len(events) > 0 else None


baseline_event = first_event_or_none(baseline["classical_events"])
controlled_event = first_event_or_none(controlled["classical_events"])

baseline_mean_r = float(np.mean(baseline["radius"]))
controlled_mean_r = float(np.mean(controlled["radius"]))

baseline_max_r = float(np.max(baseline["radius"]))
controlled_max_r = float(np.max(controlled["radius"]))

baseline_escape_count = int(np.sum(baseline["escape_mask"]))
controlled_escape_count = int(np.sum(controlled["escape_mask"]))

control_activation_count = int(np.sum(controlled["control_active"]))

if baseline_event is not None and controlled_event is not None:
    collapse_shift = controlled_event - baseline_event
else:
    collapse_shift = None


# =========================
# 4. Plots — time series
# =========================

t = np.arange(TIME_STEPS)

fig1, ax = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

# voltage
ax[0].plot(t, baseline["voltage_mean"], label="Baseline", alpha=0.9)
ax[0].plot(t, controlled["voltage_mean"], label="Controlled", alpha=0.9)
ax[0].axhline(0.90, linestyle="--", color="gray", alpha=0.7, label="Classical threshold")
if baseline_event is not None:
    ax[0].axvline(baseline_event, linestyle="--", color="tab:blue", alpha=0.7)
if controlled_event is not None:
    ax[0].axvline(controlled_event, linestyle="--", color="tab:orange", alpha=0.7)
ax[0].set_ylabel("Voltage mean")
ax[0].legend(loc="best")
ax[0].grid(True)

# coherence
ax[1].plot(t, baseline["coherence"], label="Baseline")
ax[1].plot(t, controlled["coherence"], label="Controlled")
ax[1].set_ylabel("Coherence")
ax[1].grid(True)

# switch
ax[2].plot(t, baseline["switch"], label="Baseline")
ax[2].plot(t, controlled["switch"], label="Controlled")
ax[2].set_ylabel("Switch")
ax[2].grid(True)

# control signal
ax[3].plot(t, controlled["control_signal"], label="Control signal")
ax[3].fill_between(
    t,
    0,
    controlled["control_signal"],
    where=controlled["control_active"] > 0,
    alpha=0.25,
    label="Active control"
)
ax[3].set_ylabel("u(t)")
ax[3].set_xlabel("Time step")
ax[3].legend(loc="best")
ax[3].grid(True)

fig1.suptitle("NEXAH v10 — Closed-Loop Control (Time Series)")
fig1.tight_layout()


# =========================
# 5. Plots — phase space
# =========================

fig2, ax2 = plt.subplots(figsize=(10, 8))

# baseline trajectory
ax2.plot(
    baseline["phase_x"],
    baseline["phase_y"],
    color="lightsteelblue",
    linewidth=2.0,
    alpha=0.8,
    label="Baseline trajectory",
)

# controlled trajectory
ax2.plot(
    controlled["phase_x"],
    controlled["phase_y"],
    color="orange",
    linewidth=2.0,
    alpha=0.85,
    label="Controlled trajectory",
)

# escape points
ax2.scatter(
    baseline["phase_x"][baseline["escape_mask"]],
    baseline["phase_y"][baseline["escape_mask"]],
    facecolors="none",
    edgecolors="tab:blue",
    s=100,
    linewidths=1.4,
    label="Baseline escape region",
)

ax2.scatter(
    controlled["phase_x"][controlled["escape_mask"]],
    controlled["phase_y"][controlled["escape_mask"]],
    facecolors="none",
    edgecolors="tab:orange",
    s=100,
    linewidths=1.4,
    label="Controlled escape region",
)

# stability centers
ax2.scatter(
    baseline["center_x"],
    baseline["center_y"],
    color="gold",
    marker="*",
    s=220,
    label="Stability center",
)

# start/end markers
ax2.scatter(
    baseline["phase_x"][0],
    baseline["phase_y"][0],
    color="green",
    s=100,
    label="Baseline start",
)
ax2.scatter(
    baseline["phase_x"][-1],
    baseline["phase_y"][-1],
    color="red",
    s=100,
    label="Baseline end",
)

ax2.scatter(
    controlled["phase_x"][-1],
    controlled["phase_y"][-1],
    color="purple",
    s=90,
    label="Controlled end",
)

ax2.set_title("NEXAH v10 — Closed-Loop Control (Phase Space)")
ax2.set_xlabel("Coherence")
ax2.set_ylabel("Switch signal")
ax2.grid(True)
ax2.legend(loc="best")


# =========================
# 6. Plots — polar
# =========================

fig3 = plt.figure(figsize=(10, 10))
ax3 = fig3.add_subplot(111, projection="polar")

# map to normalized radius for visual comparison
def normalize_radius(r):
    return (r - np.min(r)) / (np.max(r) - np.min(r) + 1e-8)

r_base = normalize_radius(baseline["radius"])
r_ctrl = normalize_radius(controlled["radius"])

theta_base = np.mod(np.linspace(0, 2 * np.pi * 3, len(r_base)), 2 * np.pi)
theta_ctrl = np.mod(np.linspace(0, 2 * np.pi * 3, len(r_ctrl)), 2 * np.pi)

ax3.plot(theta_base, r_base, color="lightsteelblue", linewidth=1.8, alpha=0.85, label="Baseline")
ax3.plot(theta_ctrl, r_ctrl, color="orange", linewidth=1.8, alpha=0.90, label="Controlled")

ax3.scatter(
    theta_base[baseline["escape_mask"]],
    r_base[baseline["escape_mask"]],
    facecolors="none",
    edgecolors="tab:blue",
    s=90,
    linewidths=1.4,
)

ax3.scatter(
    theta_ctrl[controlled["escape_mask"]],
    r_ctrl[controlled["escape_mask"]],
    facecolors="none",
    edgecolors="tab:orange",
    s=90,
    linewidths=1.4,
)

ax3.scatter(theta_base[0], r_base[0], color="green", s=100, label="Start")
ax3.scatter(theta_base[-1], r_base[-1], color="red", s=100, label="Baseline end")
ax3.scatter(theta_ctrl[-1], r_ctrl[-1], color="purple", s=90, label="Controlled end")

ax3.set_title("NEXAH v10 — Closed-Loop Control (Polar)")
ax3.legend(loc="upper right")


# =========================
# 7. Report
# =========================

report_lines = [
    "NEXAH v10 Closed-Loop Control Report",
    "====================================",
    "",
    f"Time steps: {TIME_STEPS}",
    f"Seed: {SEED}",
    f"Control strength: {CONTROL_STRENGTH}",
    "",
    f"Baseline first classical event: {baseline_event}",
    f"Controlled first classical event: {controlled_event}",
    f"Collapse shift (controlled - baseline): {collapse_shift}",
    "",
    f"Baseline mean radius: {baseline_mean_r:.6f}",
    f"Controlled mean radius: {controlled_mean_r:.6f}",
    f"Baseline max radius: {baseline_max_r:.6f}",
    f"Controlled max radius: {controlled_max_r:.6f}",
    "",
    f"Baseline escape count: {baseline_escape_count}",
    f"Controlled escape count: {controlled_escape_count}",
    f"Control activation count: {control_activation_count}",
    "",
    f"Baseline stability center: ({baseline['center_x']:.6f}, {baseline['center_y']:.6f})",
    f"Controlled stability center: ({controlled['center_x']:.6f}, {controlled['center_y']:.6f})",
    "",
    "Interpretation:",
]

if collapse_shift is None:
    report_lines.append("- Collapse shift could not be computed because one run had no detected classical event.")
elif collapse_shift > 0:
    report_lines.append(f"- Controlled run delayed the first classical collapse by {collapse_shift} steps.")
elif collapse_shift < 0:
    report_lines.append(f"- Controlled run accelerated the first classical collapse by {-collapse_shift} steps.")
else:
    report_lines.append("- Controlled and baseline runs reached the first classical collapse at the same step.")

if controlled_escape_count < baseline_escape_count:
    report_lines.append("- Controlled run reduced the number of escape-prone states.")
elif controlled_escape_count > baseline_escape_count:
    report_lines.append("- Controlled run increased the number of escape-prone states.")
else:
    report_lines.append("- Controlled and baseline runs had the same number of escape-prone states.")

if controlled_mean_r < baseline_mean_r:
    report_lines.append("- Controlled trajectory stayed closer to the basin center on average.")
elif controlled_mean_r > baseline_mean_r:
    report_lines.append("- Controlled trajectory drifted farther from the basin center on average.")
else:
    report_lines.append("- Controlled and baseline trajectories had the same average basin radius.")

report_text = "\n".join(report_lines)


# =========================
# 8. Save
# =========================

save_dir = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
save_dir.mkdir(parents=True, exist_ok=True)

fig1.savefig(save_dir / "ieee57_v10_closed_loop_timeseries.png", dpi=200)
fig2.savefig(save_dir / "ieee57_v10_closed_loop_phase.png", dpi=200)
fig3.savefig(save_dir / "ieee57_v10_closed_loop_polar.png", dpi=200)

report_path = save_dir / "ieee57_v10_closed_loop_report.txt"
report_path.write_text(report_text, encoding="utf-8")

plt.close(fig1)
plt.close(fig2)
plt.close(fig3)

print("\n===== NEXAH V10 CLOSED-LOOP REPORT =====")
print(report_text)
print("\nSaved:")
print("  • ieee57_v10_closed_loop_timeseries.png")
print("  • ieee57_v10_closed_loop_phase.png")
print("  • ieee57_v10_closed_loop_polar.png")
print("  • ieee57_v10_closed_loop_report.txt")
