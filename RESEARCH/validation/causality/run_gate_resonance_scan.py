import numpy as np
import matplotlib.pyplot as plt

# ============================
# Lorenz System
# ============================

def lorenz(x, y, z, s=10, r=28, b=2.667):
    dx = s * (y - x)
    dy = x * (r - z) - y
    dz = x * y - b * z
    return dx, dy, dz

def simulate_lorenz(steps=4000, dt=0.01):
    xs = np.zeros(steps)
    ys = np.zeros(steps)
    zs = np.zeros(steps)

    xs[0], ys[0], zs[0] = (0.0, 1.0, 1.05)

    for i in range(steps - 1):
        dx, dy, dz = lorenz(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx * dt
        ys[i+1] = ys[i] + dy * dt
        zs[i+1] = zs[i] + dz * dt

    return np.stack([xs, ys, zs], axis=1)

# ============================
# Target
# ============================

TARGET = np.array([15.0, 15.0, 25.0])
RADIUS = 3.0

def is_in_target(x):
    return np.linalg.norm(x - TARGET) < RADIUS

# ============================
# Gate (resonance version)
# ============================

def apply_gate(x, strength, phase):
    direction = TARGET - x
    norm = np.linalg.norm(direction) + 1e-8
    direction = direction / norm

    # 🔥 sinus modulation → das ist der wichtige Teil
    modulation = np.sin(phase)

    return x + strength * modulation * direction

# ============================
# Resonance scan
# ============================

def run_resonance_scan(strengths, phases):

    results = []

    for s in strengths:
        for p in phases:

            data = simulate_lorenz()

            hits = 0

            for i in range(len(data)):
                x = data[i]

                # größere Gate-Zone (wichtig!)
                if -10 < x[0] < 10 and -10 < x[1] < 10:
                    x = apply_gate(x, s, p + i * 0.05)  # phase evolves

                if is_in_target(x):
                    hits += 1

            hit_rate = hits / len(data)

            results.append((s, p, hit_rate))

            print(f"s={s:.2f}, phase={p:.2f} → hit={hit_rate:.4f}")

    return results

# ============================
# Plot
# ============================

def plot_heatmap(results, strengths, phases):

    heat = np.zeros((len(strengths), len(phases)))

    for s, p, h in results:
        i = np.where(strengths == s)[0][0]
        j = np.where(phases == p)[0][0]
        heat[i, j] = h

    plt.figure(figsize=(8,6))
    plt.imshow(heat, aspect='auto', origin='lower', cmap='inferno')

    plt.colorbar(label="hit rate")
    plt.xlabel("phase index")
    plt.ylabel("strength index")
    plt.title("Gate Resonance Scan")

    plt.savefig("RESEARCH/validation/causality/gate_resonance_scan.png")
    plt.close()

# ============================
# Main
# ============================

if __name__ == "__main__":

    print("⚡ NEXAH — Gate Resonance Scan")

    strengths = np.linspace(0.0, 2.0, 20)
    phases = np.linspace(0.0, 2*np.pi, 30)

    results = run_resonance_scan(strengths, phases)

    plot_heatmap(results, strengths, phases)

    print("✅ Saved: gate_resonance_scan.png")
