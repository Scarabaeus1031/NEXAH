import numpy as np
import matplotlib.pyplot as plt


# ==============================
# FIELD STATE MACHINE (3+1)
# ==============================

def nexah_mode(v, dv):

    if v > 0.95:
        return "engage"   # 0001
    elif v > 0.85:
        return "lock"     # 0010
    elif v > 0.7:
        return "release"  # 0100
    else:
        return "nexit"    # 1000


# ==============================
# ENERGY + MULTI-ATTRACTOR FIELD
# ==============================

def nexah_field(v, dv):

    mode = nexah_mode(v, dv)

    # ---- multi attractor wells ----
    wells = [
        (0.9, 6.0),
        (0.75, 4.0),
        (0.6, 2.5)
    ]

    force = 0.0
    for center, strength in wells:
        force += -strength * (v - center)

    # ---- mode-based modulation ----
    if mode == "engage":
        damping = 1.0 * dv
        force *= 0.5

    elif mode == "lock":
        damping = 3.0 * dv
        force *= 1.2

    elif mode == "release":
        damping = 1.5 * dv
        force *= 0.8

    elif mode == "nexit":
        damping = 0.5 * dv
        force *= 0.3

    return force - damping


# ==============================
# SIMULATION
# ==============================

def simulate_nexah(v0=1.0, steps=120, dt=1.0):

    v = v0
    dv = 0.0

    traj = []
    dv_traj = []
    modes = []

    for _ in range(steps):

        force = nexah_field(v, dv)

        dv += force * dt
        v += dv * dt

        traj.append(v)
        dv_traj.append(dv)
        modes.append(nexah_mode(v, dv))

    return np.array(traj), np.array(dv_traj), modes


# ==============================
# ENERGY
# ==============================

def compute_energy(v, dv):
    return 0.5 * dv**2 + (v - 0.9)**2


# ==============================
# VISUALIZATION
# ==============================

def plot_all():

    cases = {
        "collapse": 1.0,
        "slow_collapse": 0.98,
        "partial_collapse": 1.02,
        "multi_step": 1.01
    }

    for name, v0 in cases.items():

        v, dv, modes = simulate_nexah(v0)

        t = np.arange(len(v))
        E = compute_energy(v, dv)

        fig, axs = plt.subplots(1, 3, figsize=(15, 4))

        # ---- Trajectory ----
        axs[0].plot(t, v, label="field-driven")
        axs[0].axhline(0.7, linestyle="--", label="threshold")

        axs[0].set_title(f"{name} — Trajectory")
        axs[0].legend()

        # ---- Phase space ----
        axs[1].plot(v, dv)
        axs[1].axvline(0.0)
        axs[1].axhline(0.0)
        axs[1].set_title("Phase Space")

        # ---- Energy ----
        axs[2].plot(t, E)
        axs[2].set_title("Energy")

        plt.tight_layout()
        plt.show()


# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    plot_all()
