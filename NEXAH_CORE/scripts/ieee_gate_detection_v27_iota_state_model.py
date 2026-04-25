import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# CONFIG
# -----------------------------

N = 1000
TRANSITION_POINT = 600

OUTPUT_PATH = "NEXAH_CORE/outputs/ieee_gates"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# thresholds (kannst du später tunen)
SPIKE_THRESHOLD = 10
SWITCH_LOW = 0.3
SWITCH_HIGH = 0.7

# -----------------------------
# SIGNAL GENERATION (wie vorher)
# -----------------------------

t = np.arange(N)

# stabiler Bereich
signal = np.sin(0.2 * t)

# chaotischer Bereich nach Transition
noise = np.random.normal(0, 0.8, size=N)
signal[TRANSITION_POINT:] = np.sin(0.2 * t[TRANSITION_POINT:]) + noise[TRANSITION_POINT:]

# -----------------------------
# PHASE SPACE
# -----------------------------

theta = np.unwrap(np.angle(signal + 1j * np.roll(signal, 1)))
r = np.abs(signal)

# -----------------------------
# DERIVATIVE
# -----------------------------

dtheta = np.gradient(theta)
dr = np.gradient(r)

dr_dtheta = np.divide(dr, dtheta, out=np.zeros_like(dr), where=dtheta != 0)

# -----------------------------
# SWITCHING DENSITY (simple)
# -----------------------------

switching = np.abs(np.diff(np.sign(dr_dtheta), prepend=0))
window = 20
switching_density = np.convolve(switching, np.ones(window)/window, mode='same')

# -----------------------------
# STATE MODEL (V27 CORE)
# -----------------------------

STATE_THETA = 0
STATE_TAO   = 1
STATE_DAO   = 2
STATE_IOTA  = 3

states = np.zeros(N)

for i in range(N):

    if abs(dr_dtheta[i]) > SPIKE_THRESHOLD:
        states[i] = STATE_IOTA

    elif switching_density[i] > SWITCH_HIGH:
        states[i] = STATE_DAO

    elif switching_density[i] > SWITCH_LOW:
        states[i] = STATE_TAO

    else:
        states[i] = STATE_THETA

# -----------------------------
# COLORS
# -----------------------------

colors = {
    STATE_THETA: "blue",
    STATE_TAO: "orange",
    STATE_DAO: "green",
    STATE_IOTA: "red"
}

color_array = [colors[s] for s in states]

# -----------------------------
# PLOT 1 — PHASE SPACE STATE MAP
# -----------------------------

plt.figure(figsize=(10, 6))
plt.scatter(theta, r, c=color_array, s=8, alpha=0.7)
plt.axvline(theta[TRANSITION_POINT], linestyle='--', color='black', label='true transition')
plt.xlabel("θ (phase)")
plt.ylabel("r")
plt.title("V27 — Phase Space State Map (THETA / TAO / DAO / IOTA)")
plt.legend()

plt.savefig(f"{OUTPUT_PATH}/v27_phase_state_map.png", dpi=200)
plt.close()

# -----------------------------
# PLOT 2 — STATE OVER TIME
# -----------------------------

plt.figure(figsize=(10, 4))
plt.plot(states, linewidth=1)
plt.axvline(TRANSITION_POINT, linestyle='--', color='black', label='true transition')
plt.yticks([0,1,2,3], ["THETA", "TAO", "DAO", "IOTA"])
plt.title("V27 — State Evolution Over Time")
plt.xlabel("time")
plt.ylabel("state")
plt.legend()

plt.savefig(f"{OUTPUT_PATH}/v27_state_time.png", dpi=200)
plt.close()

# -----------------------------
# PLOT 3 — IOTA ONLY (ESCAPE)
# -----------------------------

mask_iota = states == STATE_IOTA

plt.figure(figsize=(10, 6))
plt.scatter(theta, dr_dtheta, s=8, alpha=0.2, color="grey", label="all")
plt.scatter(theta[mask_iota], dr_dtheta[mask_iota], color="red", s=20, label="IOTA")
plt.axvline(theta[TRANSITION_POINT], linestyle='--', color='black')
plt.xlabel("θ")
plt.ylabel("dr/dθ")
plt.title("V27 — IOTA Escape Events")
plt.legend()

plt.savefig(f"{OUTPUT_PATH}/v27_iota_events.png", dpi=200)
plt.close()

# -----------------------------
# OUTPUT SUMMARY
# -----------------------------

print("\n--- V27 RESULTS ---")
print(f"Total points: {N}")
print(f"IOTA events: {np.sum(states == STATE_IOTA)}")
print(f"DAO points: {np.sum(states == STATE_DAO)}")
print(f"TAO points: {np.sum(states == STATE_TAO)}")
print(f"THETA points: {np.sum(states == STATE_THETA)}")

print(f"\nSaved to: {OUTPUT_PATH}/v27_*.png")
