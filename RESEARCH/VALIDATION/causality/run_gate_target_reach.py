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

        # --- Gate intervention ---
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
# Target reach metric
# ============================

def compute_target_hits(data, target, radius=2.5):
    x, y = data[:,0], data[:,1]
    tx, ty = target

    dist = np.sqrt((x - tx)**2 + (y - ty)**2)
    hits = dist < radius

    hit_count = np.sum(hits)
    hit_ratio = hit_count / len(data)

    return hit_count, hit_ratio, hits

# ============================
# Main experiment
# ============================

def run_target_reach():

    print("⚡ NEXAH — Gate Target Reach Test")

    # config
    target = (15, 15)
    gate_region = (-5, 5, -5, 5)

    # baseline
    data_base = simulate()

    # controlled
    data_ctrl = simulate(
        gate_region=gate_region,
        target=target,
        strength=0.5
    )

    # metrics
    base_hits, base_ratio, base_mask = compute_target_hits(data_base, target)
    ctrl_hits, ctrl_ratio, ctrl_mask = compute_target_hits(data_ctrl, target)

    print("\n=== TARGET REACH ===")
    print(f"Baseline hits:   {base_hits} ({base_ratio:.4f})")
    print(f"Controlled hits: {ctrl_hits} ({ctrl_ratio:.4f})")

    improvement = ctrl_ratio - base_ratio
    print(f"Improvement:     {improvement:.4f}")

    # ============================
    # Plot
    # ============================

    plt.figure(figsize=(10,5))

    # baseline
    plt.subplot(1,2,1)
    plt.plot(data_base[:,0], data_base[:,1], alpha=0.5)
    plt.scatter(target[0], target[1], c='red', s=80)
    plt.title(f"Baseline\nhits={base_hits}")

    # controlled
    plt.subplot(1,2,2)
    plt.plot(data_ctrl[:,0], data_ctrl[:,1], alpha=0.5)
    plt.scatter(target[0], target[1], c='red', s=80)
    plt.title(f"Controlled\nhits={ctrl_hits}")

    plt.savefig("RESEARCH/validation/causality/results/target_reach.png")
    plt.close()

    print("✅ Saved: target_reach.png")

# ============================
# Run
# ============================

if __name__ == "__main__":
    run_target_reach()
