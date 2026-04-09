"""
ieee57_pipeline_v6_polar.py
===========================

Goal:
- Re-run the IEEE 57 test
- Extract an event-centered window around the collapse event
- Visualize the transition morphology in polar form

Polar mapping:
- angle  = normalized time phase inside the event window
- radius = normalized structural contraction depth
- color  = switch intensity

This is not a lead-time detector.
It is a morphology viewer for the collapse transition.

Outputs:
- ieee57_pipeline_v6_polar_morphology.png
- ieee57_pipeline_v6_event_window.png
"""

import pandapower as pp
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# =========================
# 1. Load system
# =========================

net = pp.networks.case57()

time_steps = 300
np.random.seed(42)

load_factor = 1.0 + 0.25 * np.sin(np.linspace(0, 6 * np.pi, time_steps))
noise = np.random.normal(0, 0.02, time_steps)

voltage_history = []
coherence_history = []
switch_signal = []

band_96 = []
band_94 = []
band_92 = []
band_90 = []

coherence_slope_history = []
coherence_accel_history = []
switch_cluster_history = []
instability_score_history = []
band_break_history = []

classical_event = None


# =========================
# 2. Simulation
# =========================

for t in range(time_steps):

    # --- perturb loads ---
    for load in net.load.index:
        net.load.at[load, "p_mw"] *= (load_factor[t] + noise[t])

    # --- power flow ---
    try:
        pp.runpp(net, enforce_q_lims=True)
        voltages = net.res_bus.vm_pu.values
    except Exception:
        voltages = np.ones(len(net.bus)) * 0.95

    # --- core signals ---
    v_mean = voltages.mean()
    v_std = voltages.std()
    coherence = 1.0 - v_std

    voltage_history.append(v_mean)
    coherence_history.append(coherence)

    # --- switch signal ---
    if len(voltage_history) > 2:
        sw = np.gradient(voltage_history)[-1]
    else:
        sw = 0.0
    switch_signal.append(sw)

    # --- bands ---
    b96 = 1 if coherence > 0.96 else 0
    b94 = 1 if coherence > 0.94 else 0
    b92 = 1 if coherence > 0.92 else 0
    b90 = 1 if coherence > 0.90 else 0

    band_96.append(b96)
    band_94.append(b94)
    band_92.append(b92)
    band_90.append(b90)

    # --- derivatives ---
    if len(coherence_history) > 1:
        dcoh = coherence_history[-1] - coherence_history[-2]
    else:
        dcoh = 0.0
    coherence_slope_history.append(dcoh)

    if len(coherence_slope_history) > 1:
        ddcoh = coherence_slope_history[-1] - coherence_slope_history[-2]
    else:
        ddcoh = 0.0
    coherence_accel_history.append(ddcoh)

    # --- switch cluster ---
    switch_cluster = np.mean(np.abs(switch_signal[-5:]))
    switch_cluster_history.append(switch_cluster)

    # --- band break ---
    band_break = (
        (len(band_96) > 1 and band_96[-2] == 1 and band_96[-1] == 0)
    )
    band_break_history.append(int(band_break))

    # --- instability score ---
    score = (
        (coherence < 0.94)
        + (coherence < 0.92)
        + (abs(dcoh) > 0.01)
        + (abs(ddcoh) > 0.02)
        + (switch_cluster > 0.02)
        + band_break
    )
    instability_score_history.append(score)

    # --- classical collapse ---
    if classical_event is None and v_mean < 0.90:
        classical_event = t


print("\n===== DETECTION =====")
print(f"Classical collapse at t = {classical_event}")


# =========================
# 3. Event window
# =========================

window = 25

start = max(0, classical_event - window)
end = min(time_steps, classical_event + window)

t_window = np.arange(start, end)

coh_window = np.array(coherence_history[start:end])
switch_window = np.array(switch_signal[start:end])
score_window = np.array(instability_score_history[start:end])


# =========================
# 4. Normalize for polar
# =========================

# radius = contraction (lower coherence → larger radius)
radius = 1.0 - coh_window
radius = (radius - radius.min()) / (radius.max() - radius.min() + 1e-8)

# angle = phase
angles = np.linspace(0, 2 * np.pi, len(radius))

# color = switch intensity
color = np.abs(switch_window)


# =========================
# 5. Plot event window
# =========================

fig1, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

ax[0].plot(t_window, coh_window)
ax[0].set_ylabel("Coherence")
ax[0].grid(True)

ax[1].plot(t_window, switch_window)
ax[1].set_ylabel("Switch")
ax[1].grid(True)

ax[2].plot(t_window, score_window)
ax[2].set_ylabel("Score")
ax[2].set_xlabel("Time")
ax[2].grid(True)

plt.suptitle("Event-Centered Window (Collapse Morphology)")
plt.tight_layout()


# =========================
# 6. Polar plot
# =========================

fig2 = plt.figure(figsize=(7, 7))
axp = fig2.add_subplot(111, projection="polar")

sc = axp.scatter(
    angles,
    radius,
    c=color,
    cmap="plasma",
    s=40,
)

axp.set_title("NEXAH Collapse Morphology (Polar View)")

cbar = plt.colorbar(sc, pad=0.1)
cbar.set_label("Switch intensity")


# =========================
# 7. Save results
# =========================

save_dir = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
save_dir.mkdir(parents=True, exist_ok=True)

fig1.savefig(save_dir / "ieee57_pipeline_v6_event_window.png", dpi=200)
fig2.savefig(save_dir / "ieee57_pipeline_v6_polar_morphology.png", dpi=200)

plt.close(fig1)
plt.close(fig2)

print(f"\nSaved:")
print(f"  • ieee57_pipeline_v6_event_window.png")
print(f"  • ieee57_pipeline_v6_polar_morphology.png")
