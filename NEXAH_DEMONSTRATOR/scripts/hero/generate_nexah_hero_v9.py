import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================================
# SYSTEMS
# ============================================================

def lorenz(x, y, z, s=10, r=28, b=2.667):
    return s*(y-x), x*(r-z)-y, x*y - b*z

def halvorsen(x, y, z, a=1.4):
    return (
        -a*x - 4*y - 4*z - y*y,
        -a*y - 4*z - 4*x - z*z,
        -a*z - 4*x - 4*y - x*x
    )

def rossler(x, y, z, a=0.2, b=0.2, c=5.7):
    return -y - z, x + a*y, b + z*(x - c)

# ============================================================
# SIMULATION
# ============================================================

def simulate(system, steps=8000, dt=0.01):
    xs, ys, zs = np.zeros(steps), np.zeros(steps), np.zeros(steps)
    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

    for i in range(steps - 1):
        dx, dy, dz = system(xs[i], ys[i], zs[i])

        xs[i+1] = xs[i] + dx*dt
        ys[i+1] = ys[i] + dy*dt
        zs[i+1] = zs[i] + dz*dt

        if abs(xs[i+1]) > 50:
            xs[i+1] = xs[i]
        if abs(ys[i+1]) > 50:
            ys[i+1] = ys[i]
        if abs(zs[i+1]) > 50:
            zs[i+1] = zs[i]

    return xs, ys, zs

# ============================================================
# STRUCTURE EXTRACTION
# ============================================================

def extract_density(xs, ys):
    mask = np.isfinite(xs) & np.isfinite(ys)
    xs, ys = xs[mask], ys[mask]

    kde = gaussian_kde(np.vstack([xs, ys]))

    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()

    X, Y = np.mgrid[xmin:xmax:250j, ymin:ymax:250j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    Z = kde(positions).reshape(X.shape)

    return X, Y, Z

# ============================================================
# COHERENCE + LYAPUNOV (approx)
# ============================================================

def coherence(xs, ys):
    dx = np.gradient(xs)
    dy = np.gradient(ys)

    vel_norm = np.sqrt(dx**2 + dy**2) + 1e-8
    coherence = dx / vel_norm

    return coherence

def lyapunov_proxy(xs, ys):
    dx = np.gradient(xs)
    dy = np.gradient(ys)
    return np.log(np.sqrt(dx**2 + dy**2) + 1e-6)

# ============================================================
# KURAMOTO (mini version)
# ============================================================

def kuramoto(n=20, steps=2000, dt=0.05, K=2.0):
    theta = np.random.rand(n)*2*np.pi
    omega = np.random.randn(n)

    history = []

    for _ in range(steps):
        coupling = np.sum(np.sin(theta[:,None] - theta), axis=1)
        theta += (omega + K/n * coupling) * dt
        history.append(theta.copy())

    return np.array(history)

# ============================================================
# PLOTTING
# ============================================================

systems = [
    ("Lorenz", lorenz),
    ("Halvorsen", halvorsen),
    ("Rössler", rossler)
]

fig, axes = plt.subplots(3, 5, figsize=(20, 12))

for row, (name, system) in enumerate(systems):

    xs, ys, zs = simulate(system)
    X, Y, Z = extract_density(xs, ys)

    coh = coherence(xs, ys)
    lya = lyapunov_proxy(xs, ys)

    # --------------------------------------------------------
    # 1. RAW
    # --------------------------------------------------------
    axes[row,0].plot(xs, ys, lw=0.3)
    axes[row,0].set_title(f"{name}\nRaw")
    axes[row,0].axis('off')

    # --------------------------------------------------------
    # 2. DENSITY
    # --------------------------------------------------------
    axes[row,1].imshow(np.rot90(Z), cmap='viridis')
    axes[row,1].set_title("Density")
    axes[row,1].axis('off')

    # --------------------------------------------------------
    # 3. BASINS + GATES
    # --------------------------------------------------------
    axes[row,2].imshow(np.rot90(Z), cmap='coolwarm', alpha=0.7)
    axes[row,2].plot(xs, ys, color='white', lw=0.5, alpha=0.5)

    gate_mask = Z < np.percentile(Z, 20)
    axes[row,2].scatter(
        X[gate_mask], Y[gate_mask],
        color='cyan', s=2, alpha=0.3
    )

    axes[row,2].set_title("Basins + Gates")
    axes[row,2].axis('off')

    # --------------------------------------------------------
    # 4. COHERENCE + LYAPUNOV
    # --------------------------------------------------------
    axes[row,3].imshow(np.rot90(Z), cmap='plasma', alpha=0.8)
    axes[row,3].scatter(xs, ys, c=coh, s=0.5, cmap='coolwarm')
    axes[row,3].set_title("Coherence")
    axes[row,3].axis('off')

    # --------------------------------------------------------
    # 5. NEON TRANSITIONS
    # --------------------------------------------------------
    axes[row,4].imshow(np.rot90(Z), cmap='inferno')

    # Neon gate mask
    neon_mask = Z < np.percentile(Z, 15)

    axes[row,4].scatter(
        X[neon_mask], Y[neon_mask],
        color='#00FFFF', s=4, alpha=0.6
    )

    axes[row,4].plot(xs, ys, color='white', lw=0.6)

    axes[row,4].set_title("Neon Gates")
    axes[row,4].axis('off')

# ============================================================
# GLOBAL TITLE
# ============================================================

fig.suptitle(
    "NEXAH v9 — Cross-System Structure Extraction\n"
    "Dynamics → Field → Basins/Gates → Coherence → Neon Transition Structure",
    fontsize=16
)

plt.tight_layout()

plt.savefig(
    "RESEARCH/visuals/nexah_structure_v9.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()

# ============================================================
# OPTIONAL: Kuramoto Plot
# ============================================================

kuramoto_data = kuramoto()

plt.figure(figsize=(6,4))
plt.plot(np.sin(kuramoto_data))
plt.title("Kuramoto Synchronization")
plt.savefig("RESEARCH/visuals/kuramoto_sync.png", dpi=300)
plt.close()
