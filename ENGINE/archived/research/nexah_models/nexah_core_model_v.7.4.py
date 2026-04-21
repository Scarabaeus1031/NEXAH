import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# NEXAH v7.4 — Coupled Field System
# Triple Spiral / Water • Mercury • Ferrofluid
# ============================================================

# ------------------------------------------------------------
# GRID
# ------------------------------------------------------------
N = 90
x = np.linspace(-1.6, 1.6, N)
y = np.linspace(-1.6, 1.6, N)
X, Y = np.meshgrid(x, y)

# ------------------------------------------------------------
# BASE POTENTIAL
# ------------------------------------------------------------
def base_potential(x, y):
    r = np.sqrt(x*x + y*y) + 1e-9
    return np.log(r) + 0.22 * np.sin(2.5 * x) * np.cos(2.5 * y)

def grad_potential(x, y, eps=1e-4):
    dx = (base_potential(x + eps, y) - base_potential(x - eps, y)) / (2.0 * eps)
    dy = (base_potential(x, y + eps) - base_potential(x, y - eps)) / (2.0 * eps)
    return np.array([dx, dy], dtype=float)

def rot_field(x, y):
    r = np.sqrt(x*x + y*y) + 1e-9
    return np.array([-y / r, x / r], dtype=float)

# ------------------------------------------------------------
# THREE LAYERS
# ------------------------------------------------------------
def water_vector(x, y):
    """
    Soft / laminar / low-vorticity layer
    """
    g = grad_potential(x, y)
    r = rot_field(x, y)
    return -0.55 * g + 0.30 * r + np.array([0.06 * x, -0.04 * y])

def mercury_vector(x, y):
    """
    Dense / resonant / more inertial-looking layer
    """
    g = grad_potential(x, y)
    r = rot_field(x, y)
    resonance = np.array([
        0.18 * np.sin(3.5 * y),
        0.18 * np.cos(3.5 * x)
    ])
    return -0.75 * g + 0.55 * r + resonance

def ferro_vector(x, y):
    """
    Field-sensitive / stronger rotational structure
    """
    g = grad_potential(x, y)
    r = rot_field(x, y)

    # pseudo-magnetic directional bias
    mx = np.tanh(2.0 * x * y)
    my = np.tanh(x*x - y*y)
    m = np.array([mx, my], dtype=float)

    return -0.45 * g + 0.95 * r + 0.35 * m

# ------------------------------------------------------------
# COUPLED FIELD
# ------------------------------------------------------------
def coupled_vector(xw, yw, xm, ym, xf, yf,
                   c12=0.18, c23=0.22, c31=0.16):
    """
    Three mutually coupled layers:
    water ↔ mercury ↔ ferro
    """
    vw = water_vector(xw, yw)
    vm = mercury_vector(xm, ym)
    vf = ferro_vector(xf, yf)

    # pair couplings (difference-driven)
    cw = c12 * np.array([xm - xw, ym - yw]) + c31 * np.array([xf - xw, yf - yw])
    cm = c12 * np.array([xw - xm, yw - ym]) + c23 * np.array([xf - xm, yf - ym])
    cf = c23 * np.array([xm - xf, ym - yf]) + c31 * np.array([xw - xf, yw - yf])

    return vw + cw, vm + cm, vf + cf

# ------------------------------------------------------------
# ENERGY-LIKE METRICS
# ------------------------------------------------------------
def layer_energy(x, y, vec):
    speed = np.linalg.norm(vec)
    pot = base_potential(x, y)
    return 0.5 * speed * speed + 0.25 * pot * pot

def pair_distance(a, b):
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# ------------------------------------------------------------
# SIMULATION
# ------------------------------------------------------------
def simulate_coupled_system(
    w0=(-1.10, 0.00),
    m0=(0.00, 1.10),
    f0=(1.10, 0.00),
    steps=900,
    dt=0.018,
    max_radius=2.6
):
    xw, yw = map(float, w0)
    xm, ym = map(float, m0)
    xf, yf = map(float, f0)

    water_traj = []
    mercury_traj = []
    ferro_traj = []

    Ew = []
    Em = []
    Ef = []
    coupling_hist = []

    for _ in range(steps):
        vw, vm, vf = coupled_vector(xw, yw, xm, ym, xf, yf)

        # step limiting for robustness
        for vec in (vw, vm, vf):
            nrm = np.linalg.norm(vec)
            if nrm > 3.0:
                vec *= 3.0 / (nrm + 1e-9)

        xw += dt * vw[0]
        yw += dt * vw[1]

        xm += dt * vm[0]
        ym += dt * vm[1]

        xf += dt * vf[0]
        yf += dt * vf[1]

        water_traj.append((xw, yw))
        mercury_traj.append((xm, ym))
        ferro_traj.append((xf, yf))

        Ew.append(layer_energy(xw, yw, vw))
        Em.append(layer_energy(xm, ym, vm))
        Ef.append(layer_energy(xf, yf, vf))

        dwm = pair_distance((xw, yw), (xm, ym))
        dmf = pair_distance((xm, ym), (xf, yf))
        dfw = pair_distance((xf, yf), (xw, yw))
        coupling_hist.append((dwm, dmf, dfw))

        if (
            np.sqrt(xw*xw + yw*yw) > max_radius or
            np.sqrt(xm*xm + ym*ym) > max_radius or
            np.sqrt(xf*xf + yf*yf) > max_radius
        ):
            break

    return (
        np.array(water_traj, dtype=float),
        np.array(mercury_traj, dtype=float),
        np.array(ferro_traj, dtype=float),
        np.array(Ew, dtype=float),
        np.array(Em, dtype=float),
        np.array(Ef, dtype=float),
        np.array(coupling_hist, dtype=float),
    )

# ------------------------------------------------------------
# MAPS
# ------------------------------------------------------------
def compute_maps():
    water_speed = np.zeros_like(X)
    mercury_speed = np.zeros_like(X)
    ferro_speed = np.zeros_like(X)
    combined_density = np.zeros_like(X)

    for i in range(N):
        for j in range(N):
            xi = X[i, j]
            yi = Y[i, j]

            vw = water_vector(xi, yi)
            vm = mercury_vector(xi, yi)
            vf = ferro_vector(xi, yi)

            water_speed[i, j] = np.linalg.norm(vw)
            mercury_speed[i, j] = np.linalg.norm(vm)
            ferro_speed[i, j] = np.linalg.norm(vf)
            combined_density[i, j] = (
                0.8 * water_speed[i, j] +
                1.0 * mercury_speed[i, j] +
                1.2 * ferro_speed[i, j]
            )

    return water_speed, mercury_speed, ferro_speed, combined_density

# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------
water_map, mercury_map, ferro_map, density_map = compute_maps()

(
    water_traj,
    mercury_traj,
    ferro_traj,
    Ew,
    Em,
    Ef,
    coupling_hist
) = simulate_coupled_system()

# ------------------------------------------------------------
# PLOT 1 — MAPS
# ------------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

im0 = axs[0, 0].imshow(
    water_map, origin="lower", extent=[x.min(), x.max(), y.min(), y.max()], cmap="Blues"
)
axs[0, 0].set_title("Water Layer Speed")
plt.colorbar(im0, ax=axs[0, 0])

im1 = axs[0, 1].imshow(
    mercury_map, origin="lower", extent=[x.min(), x.max(), y.min(), y.max()], cmap="Reds"
)
axs[0, 1].set_title("Mercury Layer Speed")
plt.colorbar(im1, ax=axs[0, 1])

im2 = axs[1, 0].imshow(
    ferro_map, origin="lower", extent=[x.min(), x.max(), y.min(), y.max()], cmap="Greens"
)
axs[1, 0].set_title("Ferrofluid Layer Speed")
plt.colorbar(im2, ax=axs[1, 0])

im3 = axs[1, 1].imshow(
    density_map, origin="lower", extent=[x.min(), x.max(), y.min(), y.max()], cmap="magma"
)
axs[1, 1].set_title("Combined Coupled Density")
plt.colorbar(im3, ax=axs[1, 1])

for ax in axs.ravel():
    ax.set_xlabel("x")
    ax.set_ylabel("y")

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# PLOT 2 — TRAJECTORIES
# ------------------------------------------------------------
plt.figure(figsize=(8, 8))
plt.imshow(
    density_map,
    origin="lower",
    extent=[x.min(), x.max(), y.min(), y.max()],
    cmap="Greys",
    alpha=0.25
)

if len(water_traj) > 0:
    plt.plot(water_traj[:, 0], water_traj[:, 1], color="blue", lw=2, label="Wasser (6D analog)")
    plt.scatter(water_traj[0, 0], water_traj[0, 1], color="blue", s=40)

if len(mercury_traj) > 0:
    plt.plot(mercury_traj[:, 0], mercury_traj[:, 1], color="red", lw=2, label="Quecksilber (7D analog)")
    plt.scatter(mercury_traj[0, 0], mercury_traj[0, 1], color="red", s=40)

if len(ferro_traj) > 0:
    plt.plot(ferro_traj[:, 0], ferro_traj[:, 1], color="green", lw=2, label="Magnetfluid (8D analog)")
    plt.scatter(ferro_traj[0, 0], ferro_traj[0, 1], color="green", s=40)

plt.title("NEXAH v7.4 — Coupled Triple Spiral")
plt.xlabel("x")
plt.ylabel("y")
plt.xlim(x.min(), x.max())
plt.ylim(y.min(), y.max())
plt.grid(True, alpha=0.2)
plt.legend()
plt.show()

# ------------------------------------------------------------
# PLOT 3 — ENERGY TIMELINES
# ------------------------------------------------------------
plt.figure(figsize=(12, 5))
plt.plot(Ew, color="blue", label="Water energy")
plt.plot(Em, color="red", label="Mercury energy")
plt.plot(Ef, color="green", label="Ferro energy")
plt.title("Layer Energy over Time")
plt.xlabel("time step")
plt.ylabel("energy-like quantity")
plt.grid(True, alpha=0.25)
plt.legend()
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# PLOT 4 — COUPLING DISTANCES
# ------------------------------------------------------------
if len(coupling_hist) > 0:
    plt.figure(figsize=(12, 5))
    plt.plot(coupling_hist[:, 0], label="dist(Water, Mercury)")
    plt.plot(coupling_hist[:, 1], label="dist(Mercury, Ferro)")
    plt.plot(coupling_hist[:, 2], label="dist(Ferro, Water)")
    plt.title("Pair Coupling Distances")
    plt.xlabel("time step")
    plt.ylabel("distance")
    plt.grid(True, alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.show()

# ------------------------------------------------------------
# PLOT 5 — OVERLAY SHAPE ONLY
# ------------------------------------------------------------
plt.figure(figsize=(7, 7))
if len(water_traj) > 0:
    plt.plot(water_traj[:, 0], water_traj[:, 1], color="blue", lw=1.8, alpha=0.9)
if len(mercury_traj) > 0:
    plt.plot(mercury_traj[:, 0], mercury_traj[:, 1], color="red", lw=1.8, alpha=0.9)
if len(ferro_traj) > 0:
    plt.plot(ferro_traj[:, 0], ferro_traj[:, 1], color="green", lw=1.8, alpha=0.9)

plt.title("Dreifache Spiralüberlagerung: Wasser – Quecksilber – Magnetfluid")
plt.xlabel("x")
plt.ylabel("y")
plt.axis("equal")
plt.grid(True, alpha=0.25)
plt.legend(["Wasser", "Quecksilber", "Magnetfluid"])
plt.show()

# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------
print("\n=== NEXAH v7.4 Summary ===")
print("trajectory lengths:",
      len(water_traj), len(mercury_traj), len(ferro_traj))

if len(Ew) > 0:
    print("Water energy min/max:", float(np.min(Ew)), float(np.max(Ew)))
if len(Em) > 0:
    print("Mercury energy min/max:", float(np.min(Em)), float(np.max(Em)))
if len(Ef) > 0:
    print("Ferro energy min/max:", float(np.min(Ef)), float(np.max(Ef)))

if len(coupling_hist) > 0:
    print("Mean pair distances:",
          np.mean(coupling_hist[:, 0]),
          np.mean(coupling_hist[:, 1]),
          np.mean(coupling_hist[:, 2]))
