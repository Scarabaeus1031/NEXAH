"""
ieee57_pipeline_v6_polar_aligned.py
===================================

Goal:
- re-run the IEEE 57 test
- detect all classical collapse events (threshold crossings)
- extract aligned event windows around each collapse
- overlay their transition morphology in a common polar frame

Aligned polar mapping:
- angle  = relative phase inside each event window
- radius = normalized contraction depth (1 - coherence)
- color  = switch intensity
- all events are aligned such that the classical collapse sits at the same phase

This is a morphology alignment viewer, not a lead-time detector.

Outputs:
- ieee57_pipeline_v6_polar_aligned_overlay.png
- ieee57_pipeline_v6_aligned_event_windows.png
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
classical_events = []


# =========================
# 2. Simulation
# =========================

for t in range(time_steps):
    # perturb loads
    for load in net.load.index:
        net.load.at[load, "p_mw"] *= (load_factor[t] + noise[t])

    # power flow
    try:
        pp.runpp(net, enforce_q_lims=True)
        voltages = net.res_bus.vm_pu.values
    except Exception:
        voltages = np.ones(len(net.bus)) * 0.95

    v_mean = voltages.mean()
    v_std = voltages.std()
    coherence = 1.0 - v_std

    voltage_history.append(v_mean)
    coherence_history.append(coherence)

    # switch signal
    if len(voltage_history) > 2:
        sw = np.gradient(voltage_history)[-1]
    else:
        sw = 0.0
    switch_signal.append(sw)

    # detect threshold crossing from above to below
    if t > 5:
        if voltage_history[-2] >= 0.90 and v_mean < 0.90:
            classical_events.append(t)

print("\n===== CLASSICAL EVENTS =====")
print(f"Detected events at: {classical_events}")


# =========================
# 3. Build aligned windows
# =========================

pre_window = 8
post_window = 16

event_windows = []

for ev in classical_events:
    start = ev - pre_window
    end = ev + post_window

    if start < 0 or end >= time_steps:
        continue

    t_rel = np.arange(-pre_window, post_window + 1)
    coh = np.array(coherence_history[start:end + 1])
    sw = np.array(switch_signal[start:end + 1])
    vol = np.array(voltage_history[start:end + 1])

    event_windows.append(
        {
            "event": ev,
            "t_rel": t_rel,
            "coh": coh,
            "sw": sw,
            "vol": vol,
        }
    )

print(f"Usable aligned windows: {len(event_windows)}")


# =========================
# 4. Plot aligned event windows
# =========================

fig1, ax = plt.subplots(3, 1, figsize=(11, 8), sharex=True)

for ew in event_windows:
    ax[0].plot(ew["t_rel"], ew["vol"], alpha=0.9, label=f"t={ew['event']}")
    ax[1].plot(ew["t_rel"], ew["coh"], alpha=0.9)
    ax[2].plot(ew["t_rel"], ew["sw"], alpha=0.9)

for a in ax:
    a.axvline(0, linestyle="--", color="black", alpha=0.7)
    a.grid(True)

ax[0].axhline(0.90, linestyle="--", color="gray", alpha=0.8)
ax[0].set_ylabel("Voltage")
ax[1].set_ylabel("Coherence")
ax[2].set_ylabel("Switch")
ax[2].set_xlabel("Relative time around collapse")

if len(event_windows) > 0:
    ax[0].legend(loc="best", fontsize=8)

plt.suptitle("Aligned Event Windows Around Classical Collapse")
plt.tight_layout()


# =========================
# 5. Polar aligned overlay
# =========================

fig2 = plt.figure(figsize=(9, 9))
axp = fig2.add_subplot(111, projection="polar")

# align collapse to angle = pi/2
# relative window maps to phase interval [-pi/2, +3pi/2] centered at collapse
for ew in event_windows:
    t_rel = ew["t_rel"]
    coh = ew["coh"]
    sw = ew["sw"]

    contraction = 1.0 - coh
    contraction = (contraction - contraction.min()) / (contraction.max() - contraction.min() + 1e-8)

    theta = np.linspace(0, 2 * np.pi, len(t_rel))
    theta = theta + (np.pi / 2)  # align collapse around top
    theta = np.mod(theta, 2 * np.pi)

    # line overlay
    axp.plot(theta, contraction, alpha=0.5, linewidth=1.5)

    # colored points
    sc = axp.scatter(
        theta,
        contraction,
        c=np.abs(sw),
        cmap="plasma",
        s=35,
        alpha=0.9,
    )

# collapse line marker at aligned phase
axp.plot([np.pi / 2, np.pi / 2], [0, 1.0], linestyle="--", color="black", alpha=0.6)
axp.set_title("Aligned Collapse Morphology Overlay (Polar)")

cbar = plt.colorbar(sc, pad=0.1)
cbar.set_label("Switch intensity")


# =========================
# 6. Save results
# =========================

save_dir = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
save_dir.mkdir(parents=True, exist_ok=True)

fig1.savefig(save_dir / "ieee57_pipeline_v6_aligned_event_windows.png", dpi=200)
fig2.savefig(save_dir / "ieee57_pipeline_v6_polar_aligned_overlay.png", dpi=200)

plt.close(fig1)
plt.close(fig2)

print("\nSaved:")
print("  • ieee57_pipeline_v6_aligned_event_windows.png")
print("  • ieee57_pipeline_v6_polar_aligned_overlay.png")
