import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# ============================
# Lorenz System
# ============================

def lorenz(x, y, z, s=10, r=28, b=2.667):
    dx = s * (y - x)
    dy = x * (r - z) - y
    dz = x * y - b * z
    return dx, dy, dz

def simulate_lorenz(steps=5000, dt=0.01):
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
# Target definition
# ============================

TARGET = np.array([15.0, 15.0, 25.0])
RADIUS = 3.0

def is_in_target(x):
    return np.linalg.norm(x - TARGET) < RADIUS

# ============================
# Gate Intervention (scaled)
# ============================

def apply_gate(x, strength):
    direction = TARGET - x
    direction = direction / (np.linalg.norm(direction) + 1e-8)
    return x + strength * direction

# ============================
# Run test
# ============================

def run_test(strengths, steps=3000):

    results = []

    for s in strengths:

        data = simulate_lorenz(steps=steps)
        hits = 0
        first_hit_times = []

        for i in range(len(data)):
            x = data[i]

            # Gate only in central region
            if -5 < x[0] < 5 and -5 < x[1] < 5:
                x = apply_gate(x, s)

            if is_in_target(x):
                hits += 1
                first_hit_times.append(i)

        hit_rate = hits / len(data)

        mean_time = np.mean(first_hit_times) if first_hit_times else np.nan

        results.append((s, hit_rate, mean_time))

        print(f"strength={s:.3f} → hit_rate={hit_rate:.4f}, mean_time={mean_time}")

    return results

# ============================
# Plot
# ============================

def plot_results(results):

    strengths = [r[0] for r in results]
    hit_rates = [r[1] for r in results]
    times = [r[2] for r in results]

    plt.figure(figsize=(10,4))

    plt.subplot(1,2,1)
    plt.plot(strengths, hit_rates, marker="o")
    plt.title("Hit Rate vs Gate Strength")
    plt.xlabel("strength")
    plt.ylabel("hit rate")

    plt.subplot(1,2,2)
    plt.plot(strengths, times, marker="o")
    plt.title("Time-to-Target vs Gate Strength")
    plt.xlabel("strength")
    plt.ylabel("mean steps")

    plt.tight_layout()
    plt.savefig("RESEARCH/validation/causality/gate_minimal_intervention.png")
    plt.close()

# ============================
# Main
# ============================

if __name__ == "__main__":

    print("⚡ NEXAH — Minimal Gate Intervention Test")

    strengths = np.linspace(0.0, 1.0, 10)

    results = run_test(strengths)

    plot_results(results)

    print("✅ Saved: gate_minimal_intervention.png")
