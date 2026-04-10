"""
v14.7_orbit_capture_and_gate_lock_controller.py
===============================================

Upgrade:
--------
- Enhanced orbital flow (DAO)
- Radial-dependent flow gain
- Broken symmetry (phase drift)
- Lowered gate threshold (reachable)

Goal:
-----
Orbit capture → real orbital motion → first gate interaction
"""

import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp
from pathlib import Path


# ============================================================
# Paths
# ============================================================

OUTDIR = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
OUTDIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Global settings
# ============================================================

TIME_STEPS = 300
SEED = 42

CENTER_X = 0.942913
CENTER_Y = 0.000076

R_CORE_MAX = 0.018
R_CAPTURE_TARGET = 0.032
R_CAPTURE_MIN = 0.020
R_BAND_MIN = 0.026
R_BAND_MAX = 0.040
R_ENVELOPE_MAX = 0.055

R_TARGET = 0.0325
R_BAND_HALF = 0.0075

THETA_REF = -np.pi / 2
OMEGA_REF = 0.0

NCS_LOCKS = np.deg2rad([97.0, 277.0, 292.0])
SNAP_TOL = np.deg2rad(8.0)

# === v14.7 FLOW ===
K_FLOW = 0.08
FLOW_PHASE = np.pi / 2 + 0.3

K_LIFT = 0.080
K_R_CAPTURE = 0.060
K_R_HOLD = 0.050
K_R_RETURN = 0.070

K_THETA_CAPTURE = 0.010
K_THETA_HOLD = 0.025
K_OMEGA = 0.020

K_SWITCH_DAMP = 0.100
K_COH_BOOST = 0.050

K_SNAP = 0.060
K_PULSE = 0.040

U_MAX = 0.10


# ============================================================
# Utils
# ============================================================

def wrap_angle(theta):
    return (theta + np.pi) % (2*np.pi) - np.pi


def state_to_polar(x, y):
    dx = x - CENTER_X
    dy = y - CENTER_Y
    return np.hypot(dx, dy), np.arctan2(dy, dx)


def min_angle_to_locks(theta):
    return min(abs(wrap_angle(theta - l)) for l in NCS_LOCKS)


def nearest_lock(theta):
    return min(NCS_LOCKS, key=lambda l: abs(wrap_angle(theta - l)))


def pulse_weight(theta):
    return np.exp(-18.0 * min_angle_to_locks(theta))


def compute_gate_score(r, theta, omega):
    radial = max(0.0, 1.0 - abs(r - R_TARGET) / R_BAND_HALF)
    phase = max(0.0, 1.0 - min_angle_to_locks(theta) / SNAP_TOL)
    omega_term = max(0.0, 1.0 - abs(omega - OMEGA_REF) / 0.06)
    return 0.4*radial + 0.4*phase + 0.2*omega_term


# ============================================================
# Mode selection
# ============================================================

def choose_mode(r, prev_mode, gate_score):

    if prev_mode == "gate_lock":
        if R_BAND_MIN <= r <= R_BAND_MAX and gate_score > 0.60:
            return "gate_lock"
        return "band_hold"

    if prev_mode == "band_hold":
        if R_BAND_MIN <= r <= R_BAND_MAX and gate_score > 0.60:
            return "gate_lock"
        if r < R_CAPTURE_MIN:
            return "capture"
        return "band_hold"

    if r < R_CORE_MAX:
        return "core_escape"
    if r < R_BAND_MIN:
        return "capture"
    if r <= R_BAND_MAX:
        return "band_hold"
    if r > R_ENVELOPE_MAX:
        return "outer_return"

    return "band_hold"


# ============================================================
# Simulation
# ============================================================

def simulate():
    np.random.seed(SEED)

    net = pp.networks.case57()
    base_p = net.load["p_mw"].copy()

    voltage_mean = []
    coherence = []
    switch = []
    theta = []
    radius = []
    mode_hist = []

    last_theta = None
    last_mode = "core_escape"
    last_coh = CENTER_X
    last_sw = CENTER_Y

    for t in range(TIME_STEPS):

        r_est, th_est = state_to_polar(last_coh, last_sw)
        omg_est = 0 if last_theta is None else wrap_angle(th_est - last_theta)

        gate_score = compute_gate_score(r_est, th_est, omg_est)
        mode = choose_mode(r_est, last_mode, gate_score)

        u = 0.0

        u_switch = -K_SWITCH_DAMP * last_sw
        u_coh = K_COH_BOOST * (CENTER_X - last_coh)
        u_omega = -K_OMEGA * omg_est

        if mode == "core_escape":
            u += K_LIFT * (R_CAPTURE_TARGET - r_est)

        elif mode == "capture":
            theta_err = wrap_angle(THETA_REF - th_est)
            u += K_R_CAPTURE * (R_TARGET - r_est)
            u += K_THETA_CAPTURE * theta_err

        elif mode == "band_hold":

            u += K_R_HOLD * (R_TARGET - r_est)

            # === v14.7 FLOW ===
            theta_error = wrap_angle(th_est - THETA_REF)
            flow_gain = 1.0 + 2.0 * r_est / R_TARGET

            u_theta_align = -1.2 * K_THETA_HOLD * theta_error
            u_theta_flow = K_FLOW * np.sin(theta_error + FLOW_PHASE) * flow_gain

            u += u_theta_align + u_theta_flow
            # ==================

            u += u_omega

        elif mode == "gate_lock":

            u += K_R_HOLD * (R_TARGET - r_est)

            # === v14.7 FLOW ===
            theta_error = wrap_angle(th_est - THETA_REF)
            flow_gain = 1.0 + 2.5 * r_est / R_TARGET

            u_theta_align = -1.2 * K_THETA_HOLD * theta_error
            u_theta_flow = K_FLOW * np.sin(theta_error + FLOW_PHASE) * flow_gain

            u += u_theta_align + u_theta_flow
            # ==================

            # pulse + snap
            ang_w = pulse_weight(th_est)
            pulse = K_PULSE * ang_w

            nearest = nearest_lock(th_est)
            snap = K_SNAP * wrap_angle(nearest - th_est)

            u += pulse + snap

        elif mode == "outer_return":
            u += -K_R_RETURN * (r_est - R_TARGET)

        u = np.clip(u, -U_MAX, U_MAX)

        scale = 1.0 - u
        net.load["p_mw"] = base_p * scale

        try:
            pp.runpp(net)
            voltages = net.res_bus.vm_pu.values
        except:
            voltages = np.ones(len(net.bus)) * 0.95

        v_mean = np.mean(voltages)
        v_std = np.std(voltages)
        coh = 1 - v_std

        sw = 0 if len(voltage_mean) < 2 else np.gradient(voltage_mean)[-1]

        r, th = state_to_polar(coh, sw)

        voltage_mean.append(v_mean)
        coherence.append(coh)
        switch.append(sw)
        radius.append(r)
        theta.append(th)
        mode_hist.append(mode)

        last_theta = th
        last_coh = coh
        last_sw = sw
        last_mode = mode

    return theta, radius, mode_hist


# ============================================================
# Run
# ============================================================

theta, radius, mode = simulate()


# ============================================================
# Polar plot
# ============================================================

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="polar")

ax.scatter(theta, radius, s=20)

theta_grid = np.linspace(-np.pi, np.pi, 400)
ax.plot(theta_grid, np.full_like(theta_grid, R_BAND_MIN), "--")
ax.plot(theta_grid, np.full_like(theta_grid, R_BAND_MAX), "--")

for lock in NCS_LOCKS:
    ax.plot([lock, lock], [0, R_ENVELOPE_MAX], alpha=0.3)

ax.set_title("NEXAH v14.7 — Orbital Flow + Gate Prep")

plt.savefig(OUTDIR / "v14_7_polar.png", dpi=150)
plt.close()

print("✅ v14.7 complete")
