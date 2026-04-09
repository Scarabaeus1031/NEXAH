"""
NEXAH IEEE 57 Pipeline v6 — Impulse Cluster Detector
====================================================

Goal:
- move beyond persistence and detect clustered structural destabilization
- compare against classical voltage-threshold collapse detection

Core idea:
Instability may appear as a pulse / cluster sequence before a sustained collapse state.
This detector triggers when a local window contains:
- repeated switch spikes
- repeated instability-score peaks
- at least one high-band break
- optional negative coherence slope support

This version is designed to detect event-density, not only state persistence.
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
impulse_density_history = []
score_peak_count_history = []
switch_peak_count_history = []
cluster_trigger_history = []

classical_event = None
nexah_event = None


# =========================
# 2. Parameters
# =========================

WINDOW = 10
SWITCH_PEAK_THRESHOLD = 0.03
SCORE_PEAK_THRESHOLD = 3
DENSITY_TRIGGER = 3


# =========================
# 3. Simulation
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
    # NEXAH coherence proxy
    # =========================
    coherence = 1.0 - v_std

    voltage_history.append(v_mean)
    coherence_history.append(coherence)

    # Switch signal = derivative of voltage mean
    if len(voltage_history) > 2:
        sw = np.gradient(voltage_history)[-1]
    else:
        sw = 0.0
    switch_signal.append(sw)

    # Multi-band coherence
    b96 = 1 if coherence > 0.96 else 0
    b94 = 1 if coherence > 0.94 else 0
    b92 = 1 if coherence > 0.92 else 0
    b90 = 1 if coherence > 0.90 else 0

    band_96.append(b96)
    band_94.append(b94)
    band_92.append(b92)
    band_90.append(b90)

    # Coherence slope
    if len(coherence_history) > 1:
        dcoh = coherence_history[-1] - coherence_history[-2]
    else:
        dcoh = 0.0
    coherence_slope_history.append(dcoh)

    # Coherence acceleration
    if len(coherence_slope_history) > 1:
        ddcoh = coherence_slope_history[-1] - coherence_slope_history[-2]
    else:
        ddcoh = 0.0
    coherence_accel_history.append(ddcoh)

    # Switch clustering: local rolling activity
    if len(switch_signal) >= 5:
        cluster = np.mean(np.abs(switch_signal[-5:]))
    else:
        cluster = np.mean(np.abs(switch_signal))
    switch_cluster_history.append(cluster)

    # =========================
    # Instability score
    # =========================
    score = 0

    if b96 == 0:
        score += 1
    if b94 == 0:
        score += 1
    if b92 == 0:
        score += 1

    if dcoh < -0.002:
        score += 1
    if ddcoh < -0.001:
        score += 1

    if cluster > 0.01:
        score += 1

    instability_score_history.append(score)

    # =========================
    # Band break tracking
    # =========================
    if t > 0:
        band_break = 1 if (band_96[-2] == 1 and band_96[-1] == 0) else 0
    else:
        band_break = 0
    band_break_history.append(band_break)

    # =========================
    # Classical detection
    # =========================
    if classical_event is None and t > 5:
        if voltage_history[-2] >= 0.90 and v_mean < 0.90:
            classical_event = t

    # =========================
    # Impulse cluster detection
    # =========================
    if t >= WINDOW:
        w_switch = switch_signal[-WINDOW:]
        w_score = instability_score_history[-WINDOW:]
        w_break = band_break_history[-WINDOW:]
        w_slope = coherence_slope_history[-WINDOW:]

        switch_peak_count = int(np.sum(np.abs(w_switch) > SWITCH_PEAK_THRESHOLD))
        score_peak_count = int(np.sum(np.array(w_score) >= SCORE_PEAK_THRESHOLD))
        band_break_count = int(np.sum(w_break))
        negative_slope_count = int(np.sum(np.array(w_slope) < -0.0015))

        # Impulse density score
        density = (
            switch_peak_count
            + score_peak_count
            + band_break_count
        )

        # Optional structural support
        structural_support = negative_slope_count >= 1

        trigger = (
            density >= DENSITY_TRIGGER
            and band_break_count >= 1
            and structural_support
        )
    else:
        switch_peak_count = 0
        score_peak_count = 0
        density = 0
        trigger = False

    switch_peak_count_history.append(switch_peak_count)
    score_peak_count_history.append(score_peak_count)
    impulse_density_history.append(density)
    cluster_trigger_history.append(1 if trigger else 0)

    # =========================
    # NEXAH detection
    # =========================
    if nexah_event is None and t > WINDOW:
        if trigger:
            nexah_event = t


# =========================
# 4. Lead time
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
# 5. Plot
# =========================

t = np.arange(time_steps)

fig, ax = plt.subplots(8, 1, figsize=(14, 17), sharex=True)

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
if classical_event is not None:
    ax[1].axvline(classical_event, linestyle="--")
if nexah_event is not None:
    ax[1].axvline(nexah_event, linestyle=":")
ax[1].set_ylabel("Coherence")
ax[1].grid(True)

# Multi-band coherence
ax[2].plot(t, band_96, label=">0.96")
ax[2].plot(t, band_94, label=">0.94")
ax[2].plot(t, band_92, label=">0.92")
ax[2].plot(t, band_90, label=">0.90")
if classical_event is not None:
    ax[2].axvline(classical_event, linestyle="--")
if nexah_event is not None:
    ax[2].axvline(nexah_event, linestyle=":")
ax[2].set_ylabel("Bands")
ax[2].grid(True)
ax[2].legend(loc="best")

# Coherence slope + accel
ax[3].plot(t, coherence_slope_history, label="d(Coherence)")
ax[3].plot(t, coherence_accel_history, label="dd(Coherence)")
ax[3].axhline(-0.0015, linestyle="--", label="Slope support")
if classical_event is not None:
    ax[3].axvline(classical_event, linestyle="--")
if nexah_event is not None:
    ax[3].axvline(nexah_event, linestyle=":")
ax[3].set_ylabel("d / dd")
ax[3].grid(True)
ax[3].legend(loc="best")

# Switch + cluster
ax[4].plot(t, switch_signal, label="Switch signal")
ax[4].plot(t, switch_cluster_history, label="Switch cluster")
ax[4].axhline(0.01, linestyle="--", label="Cluster warn")
if classical_event is not None:
    ax[4].axvline(classical_event, linestyle="--")
if nexah_event is not None:
    ax[4].axvline(nexah_event, linestyle=":")
ax[4].set_ylabel("Switch")
ax[4].grid(True)
ax[4].legend(loc="best")

# Instability score
ax[5].plot(t, instability_score_history, label="Instability score")
ax[5].axhline(SCORE_PEAK_THRESHOLD, linestyle="--", label="Score peak")
if classical_event is not None:
    ax[5].axvline(classical_event, linestyle="--")
if nexah_event is not None:
    ax[5].axvline(nexah_event, linestyle=":")
ax[5].set_ylabel("Score")
ax[5].grid(True)
ax[5].legend(loc="best")

# Impulse density components
ax[6].plot(t, switch_peak_count_history, label="Switch peak count")
ax[6].plot(t, score_peak_count_history, label="Score peak count")
ax[6].plot(t, band_break_history, label="Band break")
ax[6].plot(t, impulse_density_history, label="Impulse density")
ax[6].axhline(DENSITY_TRIGGER, linestyle="--", label="Density trigger")
if classical_event is not None:
    ax[6].axvline(classical_event, linestyle="--")
if nexah_event is not None:
    ax[6].axvline(nexah_event, linestyle=":")
ax[6].set_ylabel("Counts")
ax[6].grid(True)
ax[6].legend(loc="best")

# Cluster trigger
ax[7].plot(t, cluster_trigger_history, label="Cluster trigger")
if classical_event is not None:
    ax[7].axvline(classical_event, linestyle="--", label="Classical")
if nexah_event is not None:
    ax[7].axvline(nexah_event, linestyle=":", label="NEXAH")
ax[7].set_ylabel("Trigger")
ax[7].set_xlabel("Time")
ax[7].grid(True)
ax[7].legend(loc="best")

title = "NEXAH IEEE 57 — Impulse Cluster Detector (v6)"
if lead_time is not None:
    title += f"\nLead Time = {lead_time} steps"

plt.suptitle(title)
plt.tight_layout(rect=[0, 0, 1, 0.97])


# =========================
# 6. Save
# =========================

save_dir = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
save_dir.mkdir(parents=True, exist_ok=True)

out_file = save_dir / "ieee57_pipeline_v6_impulse_cluster.png"
plt.savefig(out_file, dpi=200)
plt.close()

print(f"\nSaved: {out_file}")
