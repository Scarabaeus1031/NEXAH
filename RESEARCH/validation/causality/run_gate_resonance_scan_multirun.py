import numpy as np
import matplotlib.pyplot as plt

print("⚡ NEXAH — Gate Resonance Scan (Multi-Run)")

# =========================
# PARAMETERS
# =========================

n_steps = 2000
dt = 0.01
runs = 20

strength_values = np.linspace(0.0, 1.5, 15)
phase_values = np.linspace(0.0, 2 * np.pi, 30)

target = np.array([15.0, 15.0])
target_radius = 3.0

# =========================
# LORENZ SYSTEM
# =========================

def lorenz(x, sigma=10.0, rho=28.0, beta=8/3):
    dx = sigma * (x[1] - x[0])
    dy = x[0] * (rho - x[2]) - x[1]
    dz = x[0] * x[1] - beta * x[2]
    return np.array([dx, dy, dz])

# =========================
# GATE FUNCTION (IMPROVED)
# =========================

def apply_gate(x, t, strength, phase):
    # smoother, larger region
    if np.linalg.norm(x[:2]) < 20:
        modulation = np.sin(t + phase)
        direction = target - x[:2]
        direction = direction / (np.linalg.norm(direction) + 1e-8)

        x[0] += strength * modulation * direction[0]
        x[1] += strength * modulation * direction[1]

    return x

# =========================
# SIMULATION
# =========================

def simulate(strength, phase):
    hits = 0
    total_steps = 0

    for _ in range(runs):
        x = np.array([
            np.random.uniform(-15, 15),
            np.random.uniform(-15, 15),
            np.random.uniform(5, 35)
        ])

        for i in range(n_steps):
            t = i * dt

            x = x + dt * lorenz(x)
            x = apply_gate(x, t, strength, phase)

            total_steps += 1

            if np.linalg.norm(x[:2] - target) < target_radius:
                hits += 1

    return hits / total_steps

# =========================
# SCAN
# =========================

heatmap = np.zeros((len(strength_values), len(phase_values)))

for i, s in enumerate(strength_values):
    for j, p in enumerate(phase_values):
        hit_rate = simulate(s, p)
        heatmap[i, j] = hit_rate

        print(f"s={s:.2f}, phase={p:.2f} → hit={hit_rate:.4f}")

# =========================
# PLOT
# =========================

plt.figure(figsize=(10, 6))
plt.imshow(
    heatmap,
    aspect='auto',
    origin='lower',
    extent=[0, 2*np.pi, strength_values[0], strength_values[-1]]
)
plt.colorbar(label="hit rate")
plt.xlabel("phase")
plt.ylabel("gate strength")
plt.title("Gate Resonance Scan (Multi-Run)")
plt.tight_layout()

plt.savefig("RESEARCH/validation/causality/gate_resonance_scan_multirun.png")
print("✅ Saved: gate_resonance_scan_multirun.png")

plt.show()
