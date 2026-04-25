# NEXAH_CORE/scripts/ieee_gate_detection_v28_yugo_flow_iota_coupling.py
#
# v28: YUGO Flow + IOTA Coupling
#
# Goal:
#   IOTA = rare structural break / escape event
#   YUGO = local flow direction around TAO / DAO / IOTA regions
#
# This script:
#   1. generates the same controlled transition signal
#   2. computes phase-space coordinates theta, r
#   3. computes dr/dtheta
#   4. classifies THETA / TAO / DAO / IOTA states
#   5. computes YUGO flow vectors
#   6. visualizes:
#        - state map with YUGO arrows
#        - YUGO direction angle over time
#        - IOTA-centered local flow windows

import os
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

np.random.seed(42)

N = 1000
TRANSITION_POINT = 600

OUTPUT_DIR = "NEXAH_CORE/outputs/ieee_gates"
os.makedirs(OUTPUT_DIR, exist_ok=True)

OUT_STATE_FLOW = os.path.join(OUTPUT_DIR, "v28_yugo_state_flow.png")
OUT_ANGLE_TIME = os.path.join(OUTPUT_DIR, "v28_yugo_angle_time.png")
OUT_IOTA_WINDOWS = os.path.join(OUTPUT_DIR, "v28_iota_local_windows.png")

SPIKE_THRESHOLD = 10.0
SWITCH_LOW = 0.3
SWITCH_HIGH = 0.7

WINDOW_SWITCH = 20
ARROW_STEP = 12
LOCAL_PAD = 20

STATE_THETA = 0
STATE_TAO = 1
STATE_DAO = 2
STATE_IOTA = 3

STATE_NAMES = {
    STATE_THETA: "THETA",
    STATE_TAO: "TAO",
    STATE_DAO: "DAO",
    STATE_IOTA: "IOTA",
}

STATE_COLORS = {
    STATE_THETA: "tab:blue",
    STATE_TAO: "tab:orange",
    STATE_DAO: "tab:green",
    STATE_IOTA: "red",
}


# --------------------------------------------------
# SIGNAL
# --------------------------------------------------

t = np.arange(N)

signal = np.sin(0.2 * t)
noise = np.random.normal(0, 0.8, size=N)
signal[TRANSITION_POINT:] = np.sin(0.2 * t[TRANSITION_POINT:]) + noise[TRANSITION_POINT:]


# --------------------------------------------------
# PHASE SPACE
# --------------------------------------------------

theta = np.unwrap(np.angle(signal + 1j * np.roll(signal, 1)))
r = np.abs(signal)

dtheta = np.gradient(theta)
dr = np.gradient(r)

eps = 1e-8
dr_dtheta = np.divide(dr, dtheta + eps)

# YUGO vector = normalized local flow in phase-space
flow_norm = np.sqrt(dtheta**2 + dr**2) + eps
yugo_theta = dtheta / flow_norm
yugo_r = dr / flow_norm
yugo_angle = np.arctan2(yugo_r, yugo_theta)


# --------------------------------------------------
# SWITCHING DENSITY
# --------------------------------------------------

switching = np.abs(np.diff(np.sign(dr_dtheta), prepend=0))
switching_density = np.convolve(
    switching,
    np.ones(WINDOW_SWITCH) / WINDOW_SWITCH,
    mode="same"
)


# --------------------------------------------------
# STATE CLASSIFICATION
# --------------------------------------------------

states = np.zeros(N, dtype=int)

for i in range(N):
    if abs(dr_dtheta[i]) > SPIKE_THRESHOLD:
        states[i] = STATE_IOTA
    elif switching_density[i] > SWITCH_HIGH:
        states[i] = STATE_DAO
    elif switching_density[i] > SWITCH_LOW:
        states[i] = STATE_TAO
    else:
        states[i] = STATE_THETA

iota_idx = np.where(states == STATE_IOTA)[0]


# --------------------------------------------------
# PLOT 1 — STATE MAP + YUGO FLOW
# --------------------------------------------------

plt.figure(figsize=(12, 7))

for state in [STATE_THETA, STATE_TAO, STATE_DAO, STATE_IOTA]:
    mask = states == state
    plt.scatter(
        theta[mask],
        r[mask],
        s=12 if state != STATE_IOTA else 36,
        alpha=0.65 if state != STATE_IOTA else 0.95,
        color=STATE_COLORS[state],
        label=STATE_NAMES[state],
    )

# show arrows only in non-stable states to avoid clutter
flow_mask = states != STATE_THETA
flow_indices = np.where(flow_mask)[0][::ARROW_STEP]

plt.quiver(
    theta[flow_indices],
    r[flow_indices],
    yugo_theta[flow_indices],
    yugo_r[flow_indices],
    angles="xy",
    scale_units="xy",
    scale=8,
    width=0.003,
    alpha=0.75,
    color="black",
    label="YUGO flow",
)

plt.axvline(theta[TRANSITION_POINT], linestyle="--", color="black", linewidth=1.5, label="true transition")

plt.xlabel("theta (unwrapped phase)")
plt.ylabel("r")
plt.title("V28 — YUGO Flow Coupled to THETA / TAO / DAO / IOTA States")
plt.legend(loc="upper left")
plt.grid(True, alpha=0.35)
plt.tight_layout()
plt.savefig(OUT_STATE_FLOW, dpi=180)
plt.close()


# --------------------------------------------------
# PLOT 2 — YUGO ANGLE OVER TIME
# --------------------------------------------------

plt.figure(figsize=(12, 5))

plt.plot(t, yugo_angle, color="purple", linewidth=1.2, label="YUGO angle")

plt.scatter(
    iota_idx,
    yugo_angle[iota_idx],
    color="red",
    s=45,
    label="IOTA events",
    zorder=5,
)

plt.axvline(TRANSITION_POINT, linestyle="--", color="black", linewidth=1.5, label="true transition")

plt.xlabel("time")
plt.ylabel("YUGO angle = atan2(dr, dtheta)")
plt.title("V28 — YUGO Direction Angle over Time")
plt.legend()
plt.grid(True, alpha=0.35)
plt.tight_layout()
plt.savefig(OUT_ANGLE_TIME, dpi=180)
plt.close()


# --------------------------------------------------
# PLOT 3 — LOCAL WINDOWS AROUND IOTA EVENTS
# --------------------------------------------------

plt.figure(figsize=(12, 7))

plt.scatter(theta, r, s=8, alpha=0.12, color="gray", label="all states")

for j, idx in enumerate(iota_idx):
    start = max(0, idx - LOCAL_PAD)
    end = min(N, idx + LOCAL_PAD + 1)

    plt.plot(
        theta[start:end],
        r[start:end],
        linewidth=2,
        alpha=0.8,
        label="IOTA local window" if j == 0 else None,
    )

    plt.scatter(
        theta[idx],
        r[idx],
        color="red",
        s=70,
        edgecolor="black",
        linewidth=0.8,
        zorder=6,
    )

    # local direction at IOTA
    plt.quiver(
        theta[idx],
        r[idx],
        yugo_theta[idx],
        yugo_r[idx],
        angles="xy",
        scale_units="xy",
        scale=5,
        width=0.006,
        color="black",
        zorder=7,
    )

plt.axvline(theta[TRANSITION_POINT], linestyle="--", color="black", linewidth=1.5, label="true transition")

plt.xlabel("theta (unwrapped phase)")
plt.ylabel("r")
plt.title("V28 — IOTA Local Windows with YUGO Direction")
plt.legend(loc="upper left")
plt.grid(True, alpha=0.35)
plt.tight_layout()
plt.savefig(OUT_IOTA_WINDOWS, dpi=180)
plt.close()


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print("\n--- V28 RESULTS ---")
print(f"Total points: {N}")
print(f"True transition index: {TRANSITION_POINT}")
print(f"True transition theta: {theta[TRANSITION_POINT]:.3f}")

for state in [STATE_THETA, STATE_TAO, STATE_DAO, STATE_IOTA]:
    print(f"{STATE_NAMES[state]} points: {np.sum(states == state)}")

print("\nIOTA event indices:")
print(iota_idx.tolist())

if len(iota_idx) > 0:
    print("\nIOTA event details:")
    for idx in iota_idx:
        print(
            f"  t={idx:4d} | theta={theta[idx]:8.3f} | r={r[idx]:6.3f} | "
            f"dr/dtheta={dr_dtheta[idx]:9.3f} | yugo_angle={yugo_angle[idx]:7.3f}"
        )

print("\nSaved:")
print(OUT_STATE_FLOW)
print(OUT_ANGLE_TIME)
print(OUT_IOTA_WINDOWS)
