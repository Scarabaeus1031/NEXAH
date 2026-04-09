"""
NEXAH IEEE 57 Pipeline v4 — Pre-Collapse Detection
==================================================

Goal:
- Classical collapse detection via voltage threshold crossing
- NEXAH early detection via structural instability signals:
    * coherence slope
    * switch spikes
    * unstable channel behavior

This is the first real pre-collapse detector candidate.
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
channel_history = []
switch_signal = []
coherence_slope_history = []

classical_event = None
nexah_event = None


# =========================
# 2. Simulation
# =========================

for t in range(time_steps):
    # Perturb loads
    for load in net.load.index:
        net.load.at[load, "p_mw"] *= (load_factor[t] + noise[t])

    # Power flow
    try:
        pp.runpp(net, enforce_q_lims=True)
        voltages = net.res_bus.vm_pu.values
    except Exception:
        voltages = np.ones(len(net.bus)) * 0.95

    # =========================
    # Classical signals
    # =========================
    v_mean = voltages.mean()
    v_std = voltages.std()

    # =========================
    # NEXAH proxy signals
    # =========================
    coherence = 1.0 - v_std

    # Store raw before derived signals
    voltage_history.append(v_mean)
    coherence_history.append(coherence)

    # Switch signal = derivative of voltage mean
    if len(voltage_history) > 2:
        sw = np.gradient(voltage_history)[-1]
    else:
        sw = 0.0
    switch_signal.append(sw)

    # Coherence slope
    if len(coherence_history) > 1:
        dcoh = coherence_history[-1] - coherence_history[-2]
    else:
        dcoh = 0.0
    coherence_slope_history.append(dcoh)

    # Grey channel
    channel = 1 if (coherence > 0.92 and v_mean > 0.90) else 0
    channel_history.append(channel)

    # =========================
    # Classical detection
    # =========================
    if classical_event is None and t > 5:
        if voltage_history[-2] >= 0.90 and v_mean < 0.90:
            classical_event = t

    # =========================
    # NEXAH early detection
    # =========================
    if nexah_event is None and t > 8:
        unstable_channel = (
            channel_history[-1] == 1
            and coherence_slope_history[-1] < -0.003
        )

        switch_spike = abs(switch_signal[-1]) > 0.015

        pre_collapse_combo = (
            coherence_history[-1] < 0.94
            and coherence_slope_history[-1] < -0.002
        )

        if unstable_channel or switch_spike or pre_collapse_combo:
            nexah_event = t


# =========================
# 3. Lead time
# =========================

if classical_event is not None and nexah_event is not None:
    lead_time = classical_event - nexah_event
else:
    lead_time = None


print("\n===== DETECTION RESULTS =====")
print(f"Classical collapse at t = {classical_event}")
print(f"NEXAH detection at t = {nexah_event}")

if lead_time is not None:
    print(f"🚀 Lead Time = {lead_time} steps")
else:
    print("⚠️ Could not compute lead time")


# =========================
# 4. Plot
# =========================

t = np.arange(time_steps)

fig, ax = plt.subplots(5, 1, figsize=(12, 11), sharex=True)

# Voltage
ax[0].plot(t, voltage_history, label="Voltage mean")
ax[0].axhline(0.90, linestyle="--", label="Classical threshold")
if classical_event is not None:
    ax[0].axvline(classical_event, linestyle="--", label=f"Classical t={classical_event}")
if nexah_event is not None:
    ax[0].axvline(nexah_event, linestyle=":", label=f"NEXAH t={nexah_event}")
ax[0].set_ylabel("Voltage")
ax[0].grid(True)
ax[0].legend(loc="best")

# Coherence
ax[1].plot(t, coherence_history, label="Coherence")
if nexah_event is not None:
    ax[1].axvline(nexah_event, linestyle=":")
if classical_event is not None:
    ax[1].axvline(classical_event, linestyle="--")
ax[1].set_ylabel("Coherence")
ax[1].grid(True)

# Coherence slope
ax[2].plot(t, coherence_slope_history, label="d(Coherence)")
ax[2].axhline(-0.003, linestyle="--", label="Early-warning slope")
if nexah_event is not None:
    ax[2].axvline(nexah_event, linestyle=":")
if classical_event is not None:
    ax[2].axvline(classical_event, linestyle="--")
ax[2].set_ylabel("dCoherence")
ax[2].grid(True)
ax[2].legend(loc="best")

# Switch signal
ax[3].plot(t, switch_signal, label="Switch signal")
ax[3].axhline(0.015, linestyle="--")
ax[3].axhline(-0.015, linestyle="--")
if nexah_event is not None:
    ax[3].axvline(nexah_event, linestyle=":")
if classical_event is not None:
    ax[3].axvline(classical_event, linestyle="--")
ax[3].set_ylabel("Switch")
ax[3].grid(True)

# Channel
ax[4].plot(t, channel_history, label="Channel")
if nexah_event is not None:
    ax[4].axvline(nexah_event, linestyle=":", label="NEXAH")
if classical_event is not None:
    ax[4].axvline(classical_event, linestyle="--", label="Classical")
ax[4].set_ylabel("Channel")
ax[4].set_xlabel("Time")
ax[4].grid(True)
ax[4].legend(loc="best")

title = "NEXAH IEEE 57 — Pre-Collapse Detection (v4)"
if lead_time is not None:
    title += f"\nLead Time = {lead_time} steps"

plt.suptitle(title)
plt.tight_layout(rect=[0, 0, 1, 0.97])


# =========================
# 5. Save
# =========================

save_dir = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
save_dir.mkdir(parents=True, exist_ok=True)

out_file = save_dir / "ieee57_pipeline_v4_precollapse.png"
plt.savefig(out_file, dpi=200)
plt.close()

print(f"\nSaved: {out_file}")
