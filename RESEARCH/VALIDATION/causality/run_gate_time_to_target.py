import numpy as np
import matplotlib.pyplot as plt

# ============================
# Lorenz system
# ============================

def lorenz(x, y, z, s=10, r=28, b=8/3):
    dx = s*(y - x)
    dy = x*(r - z) - y
    dz = x*y - b*z
    return dx, dy, dz

# ============================
# Simulation with optional gate
# ============================

def simulate(steps=5000, dt=0.01, gate_region=None, target=None, strength=0.5):
    xs = np.zeros(steps)
    ys = np.zeros(steps)
    zs = np.zeros(steps)

    xs[0], ys[0], zs[0] = (0.0, 1.0, 1.05)

    for i in range(steps - 1):
        dx, dy, dz = lorenz(xs[i], ys[i], zs[i])

        # Gate intervention
        if gate_region is not None:
            x, y = xs[i], ys[i]
            x_min, x_max, y_min, y_max = gate_region

            if x_min < x < x_max and y_min < y < y_max:
                if target is not None:
                    tx, ty = target
                    dx += strength * (tx - x)
                    dy += strength * (ty - y)

        xs[i+1] = xs[i] + dx * dt
        ys[i+1] = ys[i] + dy * dt
        zs[i+1] = zs[i] + dz * dt

    return np.stack([xs, ys, zs], axis=1)

# ============================
# Time-to-target computation
# ============================

def compute_time_to_target(data, target, radius=2.5):
    x, y = data[:,0], data[:,1]
    tx, ty = target

    dist = np.sqrt((x - tx)**2 + (y - ty)**2)

    hit_indices = np.where(dist < radius)[0]

    if len(hit_indices) == 0:
        return None  # never reached

    return hit_indices[0]  # first hit time

# ============================
# Multi-run experiment
# ============================

def run_time_to_target(n_runs=20):

    print("⚡ NEXAH — Gate Time-to-Target Test")

    target = (15, 15)
    gate_region = (-5, 5, -5, 5)

    baseline_times = []
    controlled_times = []

    for _ in range(n_runs):

        data_base = simulate()
        data_ctrl = simulate(
            gate_region=gate_region,
            target=target,
            strength=0.5
        )

        t_base = compute_time_to_target(data_base, target)
        t_ctrl = compute_time_to_target(data_ctrl, target)

        if t_base is not None:
            baseline_times.append(t_base)

        if t_ctrl is not None:
            controlled_times.append(t_ctrl)

    baseline_times = np.array(baseline_times)
    controlled_times = np.array(controlled_times)

    print("\n=== TIME TO TARGET ===")
    print(f"Baseline mean:   {np.mean(baseline_times):.2f}")
    print(f"Controlled mean: {np.mean(controlled_times):.2f}")

    improvement = np.mean(baseline_times) - np.mean(controlled_times)
    print(f"Speed-up:        {improvement:.2f} steps")

    # ============================
    # Plot
    # ============================

    plt.figure(figsize=(8,5))

    plt.hist(baseline_times, bins=15, alpha=0.6, label="baseline")
    plt.hist(controlled_times, bins=15, alpha=0.6, label="controlled")

    plt.xlabel("time to first target hit")
    plt.ylabel("count")
    plt.legend()
    plt.title("Time-to-Target Distribution")

    plt.savefig("RESEARCH/validation/causality/results/time_to_target.png")
    plt.close()

    print("✅ Saved: time_to_target.png")

# ============================
# Run
# ============================

if __name__ == "__main__":
    run_time_to_target()
