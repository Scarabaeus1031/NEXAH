import numpy as np

import matplotlib.pyplot as plt

from scipy.ndimage import gaussian_filter1d

print("⚡ NEXAH — Phase Gate Control v2")

# =========================

# LORENZ SYSTEM

# =========================

def lorenz_step(state, sigma=10, rho=28, beta=8/3):

    x, y, z = state

    dx = sigma * (y - x)

    dy = x * (rho - z) - y

    dz = x * y - beta * z

    return np.array([dx, dy, dz])

# =========================

# PARAMS

# =========================

dt = 0.01

steps = 3000

k = 0.20

threshold = 2.0

cooldown_steps = 25

# optional: only gate during strong negative phase velocity regimes

use_phase_velocity_filter = True

omega_trigger_limit = -4.0

# =========================

# BASELINE RUN — REFERENCE OMEGA

# =========================

state = np.array([1.0, 1.0, 1.0])

omega_series = []

phi_series = []

baseline_instability = []

prev_phi = None

for t in range(steps):

    dx = lorenz_step(state)

    state = state + dx * dt

    x, y, z = state

    phi = np.arctan2(y, x)

    phi_series.append(phi)

    baseline_instability.append(np.linalg.norm(dx))

    if prev_phi is None:

        omega = 0.0

    else:

        dphi = phi - prev_phi

        if dphi > np.pi:

            dphi -= 2 * np.pi

        elif dphi < -np.pi:

            dphi += 2 * np.pi

        omega = dphi / dt

    omega_series.append(omega)

    prev_phi = phi

omega_series = np.array(omega_series)

omega_smooth = gaussian_filter1d(omega_series, sigma=10)

baseline_instability = np.array(baseline_instability)

baseline_iota_threshold = np.percentile(baseline_instability, 95)

# =========================

# CONTROL RUN v2

# =========================

state = np.array([1.0, 1.0, 1.0])

trajectory = []

instability = []

mismatch_series = []

omega_control_series = []

gate_events = []

iota_events = []

control_active = []

prev_phi = None

prev_abs_mismatch = 0.0

last_gate_t = -10_000

for t in range(steps):

    dx = lorenz_step(state)

    x, y, z = state

    phi = np.arctan2(y, x)

    if prev_phi is None:

        omega = 0.0

    else:

        dphi = phi - prev_phi

        if dphi > np.pi:

            dphi -= 2 * np.pi

        elif dphi < -np.pi:

            dphi += 2 * np.pi

        omega = dphi / dt

    omega_expected = omega_smooth[t]

    mismatch = omega - omega_expected

    abs_mismatch = abs(mismatch)

    # =========================

    # GATE v2 CONDITIONS

    # =========================

    rising = abs_mismatch > prev_abs_mismatch

    strong_enough = abs_mismatch > threshold

    cooldown_ok = (t - last_gate_t) > cooldown_steps

    if use_phase_velocity_filter:

        phase_ok = omega < omega_trigger_limit

    else:

        phase_ok = True

    trigger = strong_enough and rising and cooldown_ok and phase_ok

    if trigger:

        # Correct only the phase mismatch direction.

        # Smaller, localized intervention.

        u = -k * mismatch

        dx[0] += u

        dx[1] += u

        gate_events.append(t)

        last_gate_t = t

        control_active.append(1)

    else:

        control_active.append(0)

    state = state + dx * dt

    trajectory.append(state.copy())

    inst = np.linalg.norm(dx)

    instability.append(inst)

    if inst > baseline_iota_threshold:

        iota_events.append(t)

    mismatch_series.append(abs_mismatch)

    omega_control_series.append(omega)

    prev_phi = phi

    prev_abs_mismatch = abs_mismatch

trajectory = np.array(trajectory)

instability = np.array(instability)

mismatch_series = np.array(mismatch_series)

omega_control_series = np.array(omega_control_series)

control_active = np.array(control_active)

# =========================

# SUMMARY

# =========================

print("")

print("📊 Phase Gate Control v2")

print(f"Gate events:  {len(gate_events)}")

print(f"IOTA events:  {len(iota_events)}")

print(f"Threshold:    {threshold}")

print(f"Cooldown:     {cooldown_steps}")

print(f"k:            {k}")

print(f"omega filter: {use_phase_velocity_filter}, omega < {omega_trigger_limit}")

# =========================

# PLOT 1 — TRAJECTORY

# =========================

plt.figure(figsize=(7, 7))

plt.plot(trajectory[:, 0], trajectory[:, 1], linewidth=2)

plt.title("Phase Gate Control v2 Trajectory")

plt.xlabel("x")

plt.ylabel("y")

plt.grid(True)

plt.tight_layout()

plt.savefig(

    "RESEARCH/validation/causality/results/phase_gate_v2_trajectory.png",

    dpi=200

)

plt.close()

# =========================

# PLOT 2 — INSTABILITY + GATES

# =========================

plt.figure(figsize=(14, 5))

plt.plot(instability, label="instability")

for t in gate_events:

    plt.axvline(t, color="red", alpha=0.25)

plt.axhline(

    baseline_iota_threshold,

    linestyle="--",

    alpha=0.6,

    label="baseline IOTA threshold"

)

plt.title("Phase Gate Control v2 — Instability")

plt.xlabel("time")

plt.ylabel("instability")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(

    "RESEARCH/validation/causality/results/phase_gate_v2_instability.png",

    dpi=200

)

plt.close()

# =========================

# PLOT 3 — CONTROL ACTIVATION

# =========================

plt.figure(figsize=(14, 3))

plt.plot(control_active, linewidth=1.5)

plt.title("Phase Gate Control v2 — Activation")

plt.xlabel("time")

plt.ylabel("active (1/0)")

plt.grid(True)

plt.tight_layout()

plt.savefig(

    "RESEARCH/validation/causality/results/phase_gate_v2_activation.png",

    dpi=200

)

plt.close()

# =========================

# PLOT 4 — MISMATCH + GATES

# =========================

plt.figure(figsize=(14, 5))

plt.plot(mismatch_series, label="|phase mismatch|")

for t in gate_events:

    plt.axvline(t, color="red", alpha=0.25)

plt.axhline(

    threshold,

    linestyle="--",

    alpha=0.6,

    label="gate threshold"

)

plt.title("Phase Gate Control v2 — Mismatch")

plt.xlabel("time")

plt.ylabel("|ω - expected ω|")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(

    "RESEARCH/validation/causality/results/phase_gate_v2_mismatch.png",

    dpi=200

)

plt.close()

# =========================

# SAVE SUMMARY

# =========================

summary_path = "RESEARCH/validation/causality/results/phase_gate_v2_summary.txt"

with open(summary_path, "w") as f:

    f.write("NEXAH — Phase Gate Control v2\n\n")

    f.write(f"Gate events: {len(gate_events)}\n")

    f.write(f"IOTA events: {len(iota_events)}\n")

    f.write(f"Threshold: {threshold}\n")

    f.write(f"Cooldown steps: {cooldown_steps}\n")

    f.write(f"Control strength k: {k}\n")

    f.write(f"Use phase velocity filter: {use_phase_velocity_filter}\n")

    f.write(f"Omega trigger limit: {omega_trigger_limit}\n\n")

    f.write("Interpretation:\n")

    f.write("Gate control is now selective.\n")

    f.write("It activates only when mismatch is large, rising, outside cooldown, and optionally in a critical omega regime.\n")

    f.write("This reduces blinking and tests whether phase-gated intervention can target transition precursors.\n")

print("✅ Saved: phase_gate_v2_trajectory.png")

print("✅ Saved: phase_gate_v2_instability.png")

print("✅ Saved: phase_gate_v2_activation.png")

print("✅ Saved: phase_gate_v2_mismatch.png")

print("✅ Saved: phase_gate_v2_summary.txt")
