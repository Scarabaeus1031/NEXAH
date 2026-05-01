import numpy as np
import matplotlib.pyplot as plt

print("⚡ NEXAH — Mismatch → IOTA Law")

# =========================
# LOAD DATA
# =========================

data = np.load("RESEARCH/validation/causality/control_law_data.npz")

phi_grid = data["phi"]
s_star = data["s_star"]

# =========================
# PARAMETERS
# =========================

n_steps = 3000
dt = 0.01

target = np.array([15.0, 15.0])

# =========================
# LORENZ
# =========================

def lorenz(x, sigma=10.0, rho=28.0, beta=8/3):
    dx = sigma * (x[1] - x[0])
    dy = x[0] * (rho - x[2]) - x[1]
    dz = x[0] * x[1] - beta * x[2]
    return np.array([dx, dy, dz])

def get_s_star(phi):
    return np.interp(phi, phi_grid, s_star)

def instability(x):
    return np.linalg.norm(x[:2]) / 20.0

# =========================
# SIMULATION
# =========================

x = np.array([5.0, 5.0, 25.0])

mismatch_list = []
iota_list = []

for i in range(n_steps):
    t = i * dt
    phi = (t % (2*np.pi))

    s_opt = get_s_star(phi)
    s_actual = 0.5  # baseline

    mismatch = abs(s_actual - s_opt)
    inst = instability(x)

    # IOTA condition
    iota = inst > 1.2

    mismatch_list.append(mismatch)
    iota_list.append(iota)

    x = x + dt * lorenz(x)

mismatch_list = np.array(mismatch_list)
iota_list = np.array(iota_list)

# =========================
# BINNING
# =========================

bins = np.linspace(0, np.max(mismatch_list), 20)
prob = []

for i in range(len(bins)-1):
    mask = (mismatch_list >= bins[i]) & (mismatch_list < bins[i+1])
    
    if np.sum(mask) > 0:
        p = np.mean(iota_list[mask])
    else:
        p = 0
    
    prob.append(p)

bin_centers = 0.5 * (bins[:-1] + bins[1:])

# =========================
# PLOT
# =========================

plt.figure(figsize=(8, 5))
plt.plot(bin_centers, prob, 'o-')

plt.xlabel("Mismatch")
plt.ylabel("P(IOTA)")
plt.title("Mismatch → IOTA Probability")

plt.grid(True)
plt.tight_layout()

plt.savefig("RESEARCH/validation/causality/results/mismatch_iota_law.png", dpi=200)
plt.close()

print("✅ Saved: mismatch_iota_law.png")
