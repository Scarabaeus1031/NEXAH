"""
NEXAH IEEE 57 Pipeline v3.b — Detection Comparison (Fixed)
=========================================================

Fix:
- Classical detection now detects TRANSITION, not initial condition
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

load_factor = 1.0 + 0.25 * np.sin(np.linspace(0, 6*np.pi, time_steps))
noise = np.random.normal(0, 0.02, time_steps)

voltage_history = []
coherence_history = []
channel_history = []

classical_event = None
nexah_event = None


# =========================
# 2. Simulation
# =========================

for t in range(time_steps):

    for load in net.load.index:
        net.load.at[load, "p_mw"] *= (load_factor[t] + noise[t])

    try:
        pp.runpp(net, enforce_q_lims=True)
        voltages = net.res_bus.vm_pu.values
    except:
        voltages = np.ones(len(net.bus)) * 0.95

    v_mean = voltages.mean()
    v_std = voltages.std()

    coherence = 1.0 - v_std
    channel = 1 if (coherence > 0.92 and v_mean > 0.90) else 0

    voltage_history.append(v_mean)
    coherence_history.append(coherence)
    channel_history.append(channel)

    # =========================
    # Classical detection (FIXED)
    # =========================
    if classical_event is None and t > 5:
        if voltage_history[-2] >= 0.90 and v_mean < 0.90:
            classical_event = t

    # =========================
    # NEXAH detection
    # =========================
    if nexah_event is None and t > 5:
        if channel_history[-2] == 1 and channel == 0:
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

fig, ax = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

# Voltage
ax[0].plot(t, voltage_history)
ax[0].axhline(0.90, linestyle="--")
ax[0].set_ylabel("Voltage")

if classical_event is not None:
    ax[0].axvline(classical_event, linestyle="--", label="Classical")

# Coherence
ax[1].plot(t, coherence_history)
ax[1].set_ylabel("Coherence")

# Channel
ax[2].plot(t, channel_history)
ax[2].set_ylabel("Channel")

if nexah_event is not None:
    ax[2].axvline(nexah_event, linestyle="--", label="NEXAH")

plt.suptitle("NEXAH vs Classical Collapse Detection (Fixed)")


# =========================
# 5. Save
# =========================

save_dir = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
save_dir.mkdir(parents=True, exist_ok=True)

plt.savefig(save_dir / "ieee57_pipeline_v3b_detection.png", dpi=200)
plt.close()

print(f"\nSaved: {save_dir}/ieee57_pipeline_v3b_detection.png")
