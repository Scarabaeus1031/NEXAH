"""
NEXAH IEEE 57 Pipeline v1
========================

Goal:
- Classical baseline (voltage)
- Basic NEXAH field signal (coherence proxy)
- Simple channel + instability detection

NO:
- URF
- Spiral mandatory
- fancy geometry

This is the minimal scientific baseline.
"""

import pandapower as pp
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# =========================
# 1. Load IEEE system
# =========================

net = pp.networks.case57()

print(f"Loaded IEEE 57 Bus: {len(net.bus)} buses")


# =========================
# 2. Simulation setup
# =========================

time_steps = 300
np.random.seed(42)

load_factor = 1.0 + 0.25 * np.sin(np.linspace(0, 6*np.pi, time_steps))
noise = np.random.normal(0, 0.02, time_steps)

voltage_history = []
coherence_history = []
switch_signal = []


# =========================
# 3. Simulation loop
# =========================

for t in range(time_steps):

    # perturb loads
    for load in net.load.index:
        net.load.at[load, "p_mw"] *= (load_factor[t] + noise[t])

    try:
        pp.runpp(net, enforce_q_lims=True)
        voltages = net.res_bus.vm_pu.values
    except:
        voltages = np.ones(len(net.bus)) * 0.95

    # =========================
    # Classical signal
    # =========================
    v_mean = voltages.mean()
    v_std = voltages.std()

    # =========================
    # NEXAH proxy signals
    # =========================
    # simple coherence proxy:
    coherence = 1.0 - v_std

    # simple switch proxy:
    # high variance increase = instability onset
    switch = np.gradient(voltage_history)[-1] if len(voltage_history) > 2 else 0

    voltage_history.append(v_mean)
    coherence_history.append(coherence)
    switch_signal.append(switch)


# =========================
# 4. Plot results
# =========================

t = np.arange(time_steps)

fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

ax[0].plot(t, voltage_history)
ax[0].set_ylabel("Voltage (mean)")
ax[0].grid(True)

ax[1].plot(t, coherence_history)
ax[1].set_ylabel("Coherence (proxy)")
ax[1].grid(True)

ax[2].plot(t, switch_signal)
ax[2].set_ylabel("Switch Signal")
ax[2].set_xlabel("Time")
ax[2].grid(True)

plt.suptitle("NEXAH IEEE 57 — Baseline vs Structural Signals")

# =========================
# 5. Save
# =========================

save_dir = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
save_dir.mkdir(parents=True, exist_ok=True)

plt.savefig(save_dir / "ieee57_pipeline_v1.png", dpi=200)
plt.close()

print(f"Saved results to: {save_dir}")
