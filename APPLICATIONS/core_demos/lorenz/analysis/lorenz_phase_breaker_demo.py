"""
NEXAH — Lorenz Phase Breaker Demo

Goal:
Show how instability creates:
- regime transitions
- risk spikes
- need for navigation

Compares:
1. Stable system
2. Unstable system (phase breaker active)
"""

import numpy as np
import matplotlib.pyplot as plt

plt.style.use("dark_background")


# ==================================================
# 1. LORENZ SYSTEM
# ==================================================

sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

def lorenz(x):
    dx = sigma * (x[1] - x[0])
    dy = x[0] * (rho - x[2]) - x[1]
    dz = x[0] * x[1] - beta * x[2]
    return np.array([dx, dy, dz])


# ==================================================
# 2. COHERENCE / RISK
# ==================================================

def compute_coherence(x, dx_obs):
    dx_field = lorenz(x)
    num = np.dot(dx_obs, dx_field)
    denom = np.linalg.norm(dx_obs) * np.linalg.norm(dx_field) + 1e-8
    return num / denom

def compute_risk(x, dx_obs):
    return 1 - compute_coherence(x, dx_obs)


# ==================================================
# 3. PHASE BREAKER (🔥 KEY PART)
# ==================================================

def phase_breaker(step, x):
    """
    Inject instability:
    - periodic forcing
    - asymmetric push
    """

    # sinusoidal forcing (external energy)
    forcing = np.array([
        np.sin(0.01 * step),
        np.cos(0.015 * step),
        0.5 * np.sin(0.02 * step)
    ])

    # asymmetry (break symmetry of attractor)
    asymmetry = np.array([
        0.2 * x[0],
        -0.1 * x[1],
        0.05 * x[2]
    ])

    return forcing + asymmetry


# ==================================================
# 4. SIMULATION
# ==================================================

def run_simulation(noise_strength=2.0, breaker=False):

    dt = 0.01
    steps = 4000

    x = np.array([1.0, 1.0, 1.0])

    traj = []
    coherence = []
    risk = []

    for step in range(steps):

        dx = lorenz(x)

        noise = noise_strength * np.random.randn(3)
        dx_obs = dx + noise

        # 🔥 APPLY PHASE BREAKER
        if breaker:
            dx_obs += phase_breaker(step, x)

        c = compute_coherence(x, dx_obs)
        r = 1 - c

        x = x + dt * dx_obs

        traj.append(x.copy())
        coherence.append(c)
        risk.append(r)

    return np.array(traj), np.array(coherence), np.array(risk)


# ==================================================
# 5. RUN BOTH MODES
# ==================================================

print("\n🧠 Running Phase Breaker Demo...\n")

traj_stable, coh_stable, risk_stable = run_simulation(
    noise_strength=2.0,
    breaker=False
)

traj_unstable, coh_unstable, risk_unstable = run_simulation(
    noise_strength=5.0,
    breaker=True
)


# ==================================================
# 6. VISUALIZATION
# ==================================================

fig = plt.figure(figsize=(14, 10))


# -------------------------------
# A. STABLE TRAJECTORY
# -------------------------------
ax1 = fig.add_subplot(221, projection='3d')

ax1.plot(
    traj_stable[:, 0],
    traj_stable[:, 1],
    traj_stable[:, 2],
    color="cyan",
    linewidth=0.5
)

ax1.set_title("Stable System")


# -------------------------------
# B. UNSTABLE TRAJECTORY
# -------------------------------
ax2 = fig.add_subplot(222, projection='3d')

ax2.plot(
    traj_unstable[:, 0],
    traj_unstable[:, 1],
    traj_unstable[:, 2],
    color="red",
    linewidth=0.5
)

ax2.set_title("Phase Breaker Active")


# -------------------------------
# C. COHERENCE
# -------------------------------
ax3 = fig.add_subplot(223)

ax3.plot(coh_stable, label="Stable", color="cyan")
ax3.plot(coh_unstable, label="Unstable", color="red")

ax3.set_title("Coherence Comparison")
ax3.legend()


# -------------------------------
# D. RISK
# -------------------------------
ax4 = fig.add_subplot(224)

ax4.plot(risk_stable, label="Stable", color="cyan")
ax4.plot(risk_unstable, label="Unstable", color="red")

ax4.set_title("Risk Comparison")
ax4.legend()


plt.tight_layout()

output_path = "APPLICATIONS/outputs/lorenz_phase_breaker.png"
plt.savefig(output_path, dpi=150)

print("Saved:", output_path)

plt.show()


# ==================================================
# 7. OUTPUT
# ==================================================

print("\n--- STABLE SYSTEM ---")
print("Mean coherence:", np.mean(coh_stable))
print("Mean risk:", np.mean(risk_stable))

print("\n--- UNSTABLE SYSTEM ---")
print("Mean coherence:", np.mean(coh_unstable))
print("Mean risk:", np.mean(risk_unstable))


print("""
🧭 Interpretation:

Stable:
- high coherence
- low risk
- predictable structure

Unstable (Phase Breaker):
- coherence drops
- risk spikes
- transitions appear

----------------------------------------

🧠 Key Insight:

WITHOUT instability:
→ no transitions
→ no navigation

WITH instability:
→ structure becomes dynamic
→ navigation becomes meaningful
""")
