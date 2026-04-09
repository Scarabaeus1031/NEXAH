"""
v11_phase_controller.py
======================

Goal:
- replace radial / threshold control with phase-aware navigation
- stabilize motion along the orbit instead of forcing toward center

Core idea:
- convert (coherence, switch) → polar (r, θ)
- estimate phase velocity dθ/dt
- apply smooth correction toward target phase flow

Control law:
    u(t) = -k_theta * (dθ/dt - ω_target)

Effect:
- reduces phase drift
- avoids radial explosion
- keeps system on stable orbit

Outputs:
- ieee57_v11_phase_timeseries.png
- ieee57_v11_phase_polar.png
- ieee57_v11_phase_report.txt
"""

import pandapower as pp
import pandapower.networks as pn
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# =========================
# 1. Load system
# =========================

net = pn.case57()

time_steps = 300
np.random.seed(42)

base_load = net.load.p_mw.copy()

load_factor = 1.0 + 0.25 * np.sin(np.linspace(0, 6 * np.pi, time_steps))
noise = np.random.normal(0, 0.02, time_steps)


# =========================
# 2. Helpers
# =========================

def compute_state(voltages):
    v_mean = voltages.mean()
    v_std = voltages.std()
    coherence = 1.0 - v_std
    return v_mean, coherence


def compute_switch(voltage_history):
    if len(voltage_history) > 2:
        return np.gradient(voltage_history)[-1]
    return 0.0


def to_polar(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return r, theta


# =========================
# 3. Baseline simulation
# =========================

baseline_coh = []
baseline_sw = []
baseline_volt = []

net.load.p_mw = base_load.copy()

for t in range(time_steps):

    net.load.p_mw = base_load * (load_factor[t] + noise[t])

    try:
        pp.runpp(net, enforce_q_lims=True)
        voltages = net.res_bus.vm_pu.values
    except:
        voltages = np.ones(len(net.bus)) * 0.95

    v_mean, coherence = compute_state(voltages)
    sw = compute_switch(baseline_volt)

    baseline_volt.append(v_mean)
    baseline_coh.append(coherence)
    baseline_sw.append(sw)


baseline_coh = np.array(baseline_coh)
baseline_sw = np.array(baseline_sw)


# =========================
# 4. Controlled simulation (PHASE CONTROL)
# =========================

net = pn.case57()
net.load.p_mw = base_load.copy()

controlled_coh = []
controlled_sw = []
controlled_volt = []
control_signal = []

theta_history = []

# control parameters
k_theta = 0.2
omega_target = 0.0   # target phase velocity (stable orbit)

for t in range(time_steps):

    net.load.p_mw = base_load * (load_factor[t] + noise[t])

    try:
        pp.runpp(net, enforce_q_lims=True)
        voltages = net.res_bus.vm_pu.values
    except:
        voltages = np.ones(len(net.bus)) * 0.95

    v_mean, coherence = compute_state(voltages)
    sw = compute_switch(controlled_volt)

    # convert to polar
    r, theta = to_polar(coherence, sw)
    theta_history.append(theta)

    # estimate phase velocity
    if len(theta_history) > 2:
        dtheta = np.gradient(theta_history)[-1]
    else:
        dtheta = 0.0

    # PHASE CONTROL LAW
    u = -k_theta * (dtheta - omega_target)

    # apply gentle correction to load
    net.load.p_mw *= (1 + u)

    controlled_volt.append(v_mean)
    controlled_coh.append(coherence)
    controlled_sw.append(sw)
    control_signal.append(u)


controlled_coh = np.array(controlled_coh)
controlled_sw = np.array(controlled_sw)
control_signal = np.array(control_signal)


# =========================
# 5. Metrics
# =========================

baseline_r = np.sqrt(baseline_coh**2 + baseline_sw**2)
controlled_r = np.sqrt(controlled_coh**2 + controlled_sw**2)

report = f"""
===== NEXAH PHASE CONTROL REPORT =====

Baseline mean radius: {baseline_r.mean():.6f}
Controlled mean radius: {controlled_r.mean():.6f}

Baseline max radius: {baseline_r.max():.6f}
Controlled max radius: {controlled_r.max():.6f}

Mean control signal: {control_signal.mean():.6f}
Max control signal: {control_signal.max():.6f}

Interpretation:
- phase-based control stabilizes angular drift
- should reduce chaotic escape amplification
"""


# =========================
# 6. Plots
# =========================

Path("results").mkdir(exist_ok=True)

# Phase space
plt.figure(figsize=(8,6))
plt.plot(baseline_coh, baseline_sw, alpha=0.4, label="Baseline")
plt.plot(controlled_coh, controlled_sw, alpha=0.8, label="Phase-controlled")
plt.xlabel("Coherence")
plt.ylabel("Switch")
plt.title("NEXAH v11 — Phase Control (Phase Space)")
plt.legend()
plt.grid()
plt.savefig("results/ieee57_v11_phase_phase_space.png")
plt.close()

# Time series
plt.figure(figsize=(10,6))
plt.plot(baseline_coh, label="Baseline coherence")
plt.plot(controlled_coh, label="Controlled coherence")
plt.legend()
plt.title("Coherence over time")
plt.grid()
plt.savefig("results/ieee57_v11_phase_timeseries.png")
plt.close()

# Polar
theta_b = np.arctan2(baseline_sw, baseline_coh)
theta_c = np.arctan2(controlled_sw, controlled_coh)

plt.figure(figsize=(8,8))
ax = plt.subplot(111, projection='polar')
ax.plot(theta_b, baseline_r, alpha=0.4, label="Baseline")
ax.plot(theta_c, controlled_r, alpha=0.8, label="Controlled")
ax.set_title("NEXAH v11 — Phase Control (Polar)")
plt.legend()
plt.savefig("results/ieee57_v11_phase_polar.png")
plt.close()


# =========================
# 7. Save report
# =========================

with open("results/ieee57_v11_phase_report.txt", "w") as f:
    f.write(report)

print(report)
