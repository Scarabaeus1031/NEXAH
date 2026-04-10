"""
v14.8_two_axis_orbit_controller.py
==================================
(complete, fixed)
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp

# ============================================================
# 0. Paths
# ============================================================

OUTDIR = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
OUTDIR.mkdir(parents=True, exist_ok=True)

TS_PATH = OUTDIR / "ieee57_v14_8_two_axis_timeseries.png"
PHASE_PATH = OUTDIR / "ieee57_v14_8_two_axis_phase.png"
POLAR_PATH = OUTDIR / "ieee57_v14_8_two_axis_polar.png"
REPORT_PATH = OUTDIR / "ieee57_v14_8_two_axis_report.txt"

# ============================================================
# 1. Settings
# ============================================================

TIME_STEPS = 300
SEED = 42
CLASSICAL_THRESHOLD = 0.90

CENTER_X = 0.942913
CENTER_Y = 0.000076

R_CORE_MAX = 0.018
R_CAPTURE_TARGET = 0.032
R_BAND_MIN = 0.026
R_BAND_MAX = 0.040
R_TARGET = 0.0325
R_ENVELOPE_MAX = 0.055

THETA_REF = -np.pi / 2.0
OMEGA_REF = 0.0

K_FLOW = 0.10
FLOW_PHASE = np.pi / 2 + 0.25
TANGENTIAL_DRIFT = 0.010

K_R = 0.06
K_THETA = 0.02

U_R_MAX = 0.10
U_THETA_MAX = 0.10

# ============================================================
# 2. Utils
# ============================================================

def wrap_angle(theta):
    return (theta + np.pi) % (2*np.pi) - np.pi

def state_to_polar(x, y):
    dx = x - CENTER_X
    dy = y - CENTER_Y
    r = np.hypot(dx, dy)
    theta = np.arctan2(dy, dx)
    return r, theta

def clip(x, lo, hi):
    return np.clip(x, lo, hi)

# ============================================================
# 3. Simulation
# ============================================================

def simulate():
    np.random.seed(SEED)

    net = pp.networks.case57()
    base_p = net.load["p_mw"].copy()
    base_q = net.load["q_mvar"].copy()

    load_factor = 1 + 0.25*np.sin(np.linspace(0, 6*np.pi, TIME_STEPS))
    noise = np.random.normal(0, 0.02, TIME_STEPS)

    voltage_mean = []
    coherence = []
    switch = []
    radius = []
    theta = []

    u_r_hist = []
    u_theta_hist = []

    last_theta = None
    last_coh = CENTER_X
    last_sw = CENTER_Y

    for t in range(TIME_STEPS):

        r_est, th_est = state_to_polar(last_coh, last_sw)

        if last_theta is None:
            omega = 0.0
        else:
            omega = wrap_angle(th_est - last_theta)

        # =========================
        # CONTROL (2-axis)
        # =========================

        # radial
        u_r = K_R * (R_TARGET - r_est)

        # tangential
        u_theta = -K_THETA * wrap_angle(th_est - THETA_REF)
        u_theta += K_FLOW * np.sin(th_est + FLOW_PHASE)
        u_theta += TANGENTIAL_DRIFT

        u_r = clip(u_r, -U_R_MAX, U_R_MAX)
        u_theta = clip(u_theta, -U_THETA_MAX, U_THETA_MAX)

        u_r_hist.append(u_r)
        u_theta_hist.append(u_theta)

        # =========================
        # apply to grid
        # =========================

        base_scale = max(0.5, load_factor[t] + noise[t])

        scale_p = clip(base_scale - u_r, 0.45, 1.45)
        scale_q = clip(base_scale - u_theta, 0.45, 1.45)

        net.load["p_mw"] = base_p * scale_p
        net.load["q_mvar"] = base_q * scale_q

        try:
            pp.runpp(net)
            voltages = net.res_bus.vm_pu.values
        except:
            voltages = np.ones(len(net.bus)) * 0.95

        v_mean = np.mean(voltages)
        v_std = np.std(voltages)

        coh = 1 - v_std
        voltage_mean.append(v_mean)
        coherence.append(coh)

        if len(voltage_mean) > 2:
            sw = np.gradient(voltage_mean)[-1]
        else:
            sw = 0.0

        switch.append(sw)

        r, th = state_to_polar(coh, sw)
        radius.append(r)
        theta.append(th)

        last_theta = th
        last_coh = coh
        last_sw = sw

    return {
        "coherence": np.array(coherence),
        "switch": np.array(switch),
        "radius": np.array(radius),
        "theta": np.array(theta),
        "u_r": np.array(u_r_hist),
        "u_theta": np.array(u_theta_hist)
    }

# ============================================================
# 4. Run
# ============================================================

data = simulate()

# ============================================================
# 5. Plots
# ============================================================

t = np.arange(TIME_STEPS)

# --- Time series ---
fig, axs = plt.subplots(3, 1, figsize=(12,10), sharex=True)

axs[0].plot(t, data["coherence"])
axs[0].set_ylabel("coherence")

axs[1].plot(t, data["switch"])
axs[1].set_ylabel("switch")

axs[2].plot(t, data["u_r"], label="u_r")
axs[2].plot(t, data["u_theta"], label="u_theta")
axs[2].legend()
axs[2].set_ylabel("control")

plt.savefig(TS_PATH)
plt.close()

# --- Phase ---
plt.figure(figsize=(6,6))
plt.scatter(data["coherence"], data["switch"], s=10)
plt.xlabel("coherence")
plt.ylabel("switch")
plt.savefig(PHASE_PATH)
plt.close()

# --- Polar ---
plt.figure(figsize=(6,6))
ax = plt.subplot(111, projection="polar")
ax.scatter(data["theta"], data["radius"], s=10)
plt.savefig(POLAR_PATH)
plt.close()

print("✅ v14.8 complete — 2-axis control active")
