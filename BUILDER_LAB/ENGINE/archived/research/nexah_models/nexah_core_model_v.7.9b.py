import numpy as np
import matplotlib.pyplot as plt

# =============================
# Lorenz parameters
# =============================
sigma = 10
rho = 28
beta = 8 / 3

dt = 0.01
steps = 12000

# =============================
# NEXAH regions
# =============================
def classify_region(x, y):
    r = np.sqrt(x**2 + y**2)
    if r < 4:
        return "eye"
    elif x < 0:
        return "moon"
    else:
        return "deris"

# =============================
# Mode controller
# =============================
class ModeController:
    def __init__(self):
        self.mode = "stabilize"
        self.timer = 0

    def update(self, counts):
        self.timer += 1

        # normalize
        total = sum(counts.values())
        ratios = {k: v / total for k, v in counts.items()}

        # --- switching logic ---
        if self.mode == "stabilize":
            if ratios["moon"] > 0.55:
                self.mode = "expand"
                self.timer = 0

        elif self.mode == "expand":
            if ratios["deris"] > 0.55:
                self.mode = "pass"
                self.timer = 0

        elif self.mode == "pass":
            if self.timer > 500:
                self.mode = "stabilize"
                self.timer = 0

        return self.mode

# =============================
# Control force (mode-based)
# =============================
def control_force(x, y, mode):
    fx, fy = 0.0, 0.0

    if mode == "stabilize":
        # pull toward moon (left)
        fx -= 0.5 * np.sign(x)
        fy -= 0.1 * y

    elif mode == "expand":
        # push outward
        fx += 0.8 * np.sign(x)
        fy += 0.2 * np.sign(y)

    elif mode == "pass":
        # pull toward center (eye)
        fx -= 0.6 * x
        fy -= 0.6 * y

    return fx, fy

# =============================
# Simulation
# =============================
x, y, z = 1.0, 1.0, 1.0

xs, ys, zs = [], [], []
regions = []
modes = []

controller = ModeController()

counts = {"eye": 1, "moon": 1, "deris": 1}

for i in range(steps):

    # classify
    region = classify_region(x, y)
    counts[region] += 1

    # update mode
    mode = controller.update(counts)

    # control
    fx, fy = control_force(x, y, mode)

    # Lorenz dynamics + control
    dx = sigma * (y - x) + fx
    dy = x * (rho - z) - y + fy
    dz = x * y - beta * z

    x += dx * dt
    y += dy * dt
    z += dz * dt

    xs.append(x)
    ys.append(y)
    zs.append(z)
    regions.append(region)
    modes.append(mode)

# =============================
# Summary
# =============================
print("\n=== NEXAH v7.9 Summary ===")
total = sum(counts.values())
for k in counts:
    print(f"{k}: {counts[k]} ({counts[k]/total:.3f})")

# =============================
# Plot
# =============================
colors = {
    "eye": "green",
    "moon": "blue",
    "deris": "red"
}

plt.figure(figsize=(8, 6))
for i in range(len(xs)):
    plt.scatter(xs[i], ys[i], color=colors[regions[i]], s=1)

plt.title("NEXAH v7.9 — Mode-Switch Navigation")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid()
plt.show()

# =============================
# Mode timeline
# =============================
mode_map = {"stabilize": 0, "expand": 1, "pass": 2}
mode_vals = [mode_map[m] for m in modes]

plt.figure(figsize=(10, 3))
plt.plot(mode_vals, linewidth=0.8)
plt.yticks([0,1,2], ["stabilize", "expand", "pass"])
plt.title("Mode Timeline")
plt.grid()
plt.show()
