# nexah_core_model_v8_5.py

import numpy as np
import matplotlib.pyplot as plt

# ==============================
# 1. LORENZ SYSTEM
# ==============================

def lorenz(x, y, z, sigma=10, rho=28, beta=8/3):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz

def simulate_lorenz(n_steps=20000, dt=0.01):
    xs = np.zeros(n_steps)
    ys = np.zeros(n_steps)
    zs = np.zeros(n_steps)

    xs[0], ys[0], zs[0] = 0.1, 0.0, 0.0

    for i in range(n_steps - 1):
        dx, dy, dz = lorenz(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx * dt
        ys[i+1] = ys[i] + dy * dt
        zs[i+1] = zs[i] + dz * dt

    return xs, ys, zs

# ==============================
# 2. RGB CLASSIFICATION
# ==============================

def classify_rgb(x, y, z):
    if x < -5:
        return "blue"
    elif x > 5:
        return "red"
    else:
        return "green"

# ==============================
# 3. GREY CHANNEL DETECTION
# ==============================

def detect_grey_channel(x, y):
    # Nähe zur Diagonale (dein "Myzel Channel")
    d = np.abs(y - x * 0.7)
    return d < 1.0

# ==============================
# 4. ANGULAR ANALYSIS (CORE v8.5)
# ==============================

def compute_angles(x, y):
    theta = np.arctan2(y, x)
    theta = (theta + 2*np.pi) % (2*np.pi)
    theta_deg = np.degrees(theta)
    return theta, theta_deg

def angular_velocity(theta):
    dtheta = np.diff(theta)
    return dtheta

# ==============================
# 5. MAIN
# ==============================

def main():

    print("\n=== NEXAH v8.5 — Angular Resonance Analysis ===\n")

    # --- simulate ---
    x, y, z = simulate_lorenz()

    # --- classify ---
    labels = np.array([classify_rgb(x[i], y[i], z[i]) for i in range(len(x))])

    # --- grey channel ---
    grey_mask = detect_grey_channel(x, y)

    # --- angles ---
    theta, theta_deg = compute_angles(x, y)
    dtheta = angular_velocity(theta)

    # ==============================
    # 6. VISUAL 1 — FULL FIELD
    # ==============================

    plt.figure(figsize=(8,6))

    colors = {
        "blue": "blue",
        "green": "orange",
        "red": "green"
    }

    for key in colors:
        mask = labels == key
        plt.scatter(x[mask], y[mask], s=2, color=colors[key], label=key)

    plt.scatter(x[grey_mask], y[grey_mask], s=5, color="black", label="grey")

    plt.title("NEXAH v8.5 — Field + Grey Channel")
    plt.legend()
    plt.show()

    # ==============================
    # 7. VISUAL 2 — ANGLE HISTOGRAM
    # ==============================

    plt.figure(figsize=(10,4))

    plt.hist(theta_deg, bins=180)
    plt.title("Angular Distribution (Full Field)")
    plt.xlabel("Degrees")
    plt.ylabel("Count")

    # mark special angles
    for a in [137, 139, 276]:
        plt.axvline(a, linestyle="--")

    plt.show()

    # ==============================
    # 8. VISUAL 3 — GREY CHANNEL ANGLES
    # ==============================

    plt.figure(figsize=(10,4))

    plt.hist(theta_deg[grey_mask], bins=180)
    plt.title("Angular Distribution (Grey Channel)")
    plt.xlabel("Degrees")

    for a in [137, 139, 276]:
        plt.axvline(a, linestyle="--")

    plt.show()

    # ==============================
    # 9. VISUAL 4 — ANGULAR VELOCITY
    # ==============================

    plt.figure(figsize=(10,4))
    plt.plot(dtheta)
    plt.title("Angular Velocity dθ")
    plt.show()

    # ==============================
    # 10. VISUAL 5 — THETA OVER TIME
    # ==============================

    plt.figure(figsize=(10,4))
    plt.plot(theta_deg)
    plt.title("θ over time")
    plt.show()

    # ==============================
    # 11. SUMMARY
    # ==============================

    total = len(labels)
    counts = {k: np.sum(labels == k) for k in ["blue", "green", "red"]}
    grey_count = np.sum(grey_mask)

    print("=== Summary ===")
    for k, v in counts.items():
        print(f"{k}: {v} ({v/total:.3f})")
    print(f"grey: {grey_count} ({grey_count/total:.3f})")

# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    main()
