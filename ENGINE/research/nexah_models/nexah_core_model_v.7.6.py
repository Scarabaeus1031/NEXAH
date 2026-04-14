# ============================================================
# NEXAH v7.6 — Torus + Lorenz + C + State Switching
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------
steps = 5000
dt = 0.01

# control parameter C
C = 1.15

# double-well / switching dynamics
alpha = 1.2
beta = 1.0
gamma = 0.55
delta = 0.35

# torus embedding
R = 2.3
r = 0.85

# phase transport
omega_base = 0.9
omega_mod = 0.35


# ------------------------------------------------------------
# 3+1 STATE MACHINE
# ------------------------------------------------------------
def nexah_state(c, dc):
    """
    3+1 logic from local control state
    """
    if c > 0.85:
        return "engage"   # 0001
    elif c > 0.35:
        return "lock"     # 0010
    elif c > -0.25:
        return "release"  # 0100
    else:
        return "nexit"    # 1000


def state_index(name):
    table = {
        "engage": 0,
        "lock": 1,
        "release": 2,
        "nexit": 3
    }
    return table[name]


# ------------------------------------------------------------
# CORE DYNAMICS
# ------------------------------------------------------------
def nexah_vector_field(c, dc, C):
    """
    Double-well + switching + weak rotation
    c  = main control variable
    dc = drift / velocity
    C  = bifurcation / forcing parameter

    Structure:
    - double well in c
    - damping / anti-damping depending on zone
    - weak rotational cross-coupling
    """

    state = nexah_state(c, dc)

    # potential derivative:
    # U(c) = 1/4 c^4 - (C/2) c^2
    # dU/dc = c^3 - C*c
    force_potential = -(c**3 - C * c)

    # weak shear / coupling
    shear = gamma * dc

    # state-dependent damping / drive
    if state == "engage":
        damping = 1.8 * dc
        boost = 0.15

    elif state == "lock":
        damping = 2.6 * dc
        boost = 0.00

    elif state == "release":
        damping = 0.9 * dc
        boost = -0.10

    else:  # nexit
        damping = 0.35 * dc
        boost = -0.18

    d2c = alpha * force_potential - damping + shear + boost

    return d2c, state


# ------------------------------------------------------------
# SIMULATION
# ------------------------------------------------------------
def simulate_v76(c0=0.15, dc0=0.0, theta0=0.0, phi0=0.0):
    """
    c, dc: local Lorenz-like switching coordinates
    theta, phi: torus phases
    """

    c = c0
    dc = dc0
    theta = theta0
    phi = phi0

    c_traj = []
    dc_traj = []
    theta_traj = []
    phi_traj = []
    x_traj = []
    y_traj = []
    z_traj = []
    states = []
    energy = []
    switches = []

    prev_state = nexah_state(c, dc)

    for t in range(steps):
        d2c, state = nexah_vector_field(c, dc, C)

        # integrate switching dynamics
        dc += d2c * dt
        c += dc * dt

        # clamp softly to avoid blow-up
        c = np.clip(c, -2.5, 2.5)
        dc = np.clip(dc, -6.0, 6.0)

        # torus transport frequency depends on c and dc
        omega_theta = omega_base + omega_mod * np.tanh(c)
        omega_phi = 1.35 * omega_base + 0.25 * np.tanh(dc)

        theta += omega_theta * dt
        phi += omega_phi * dt

        # torus radius breathing from control variable
        local_r = r * (1.0 + 0.18 * np.tanh(c))

        # torus embedding
        x = (R + local_r * np.cos(phi)) * np.cos(theta)
        y = (R + local_r * np.cos(phi)) * np.sin(theta)
        z = local_r * np.sin(phi) + delta * c

        # energy-like observable
        E = 0.5 * dc**2 + 0.25 * c**4 - 0.5 * C * c**2

        c_traj.append(c)
        dc_traj.append(dc)
        theta_traj.append(theta)
        phi_traj.append(phi)
        x_traj.append(x)
        y_traj.append(y)
        z_traj.append(z)
        states.append(state)
        energy.append(E)

        if state != prev_state:
            switches.append(t)

        prev_state = state

    return {
        "c": np.array(c_traj),
        "dc": np.array(dc_traj),
        "theta": np.array(theta_traj),
        "phi": np.array(phi_traj),
        "x": np.array(x_traj),
        "y": np.array(y_traj),
        "z": np.array(z_traj),
        "states": states,
        "energy": np.array(energy),
        "switches": np.array(switches, dtype=int)
    }


# ------------------------------------------------------------
# VISUALIZATION
# ------------------------------------------------------------
def plot_results(data):
    t = np.arange(len(data["c"])) * dt

    state_colors = {
        "engage": "blue",
        "lock": "orange",
        "release": "green",
        "nexit": "red"
    }

    numeric_states = np.array([state_index(s) for s in data["states"]])

    # --------------------------------------------------------
    # Figure 1: c / dc / energy / states
    # --------------------------------------------------------
    fig, axs = plt.subplots(2, 2, figsize=(14, 9))

    axs[0, 0].plot(t, data["c"], color="navy", label="c")
    axs[0, 0].plot(t, data["dc"], color="crimson", alpha=0.8, label="dc")
    for s in data["switches"]:
        axs[0, 0].axvline(s * dt, color="gray", alpha=0.15)
    axs[0, 0].set_title("Control variable c(t) and drift dc(t)")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    axs[0, 1].plot(data["c"], data["dc"], color="black", linewidth=1.0)
    axs[0, 1].axvline(0, color="gray", linewidth=0.8)
    axs[0, 1].axhline(0, color="gray", linewidth=0.8)
    axs[0, 1].set_title("Phase Portrait (c vs dc)")
    axs[0, 1].set_xlabel("c")
    axs[0, 1].set_ylabel("dc")
    axs[0, 1].grid(True)

    axs[1, 0].plot(t, data["energy"], color="purple")
    for s in data["switches"]:
        axs[1, 0].axvline(s * dt, color="gray", alpha=0.15)
    axs[1, 0].set_title("Energy-like observable")
    axs[1, 0].grid(True)

    axs[1, 1].step(t, numeric_states, where="post", color="darkgreen")
    axs[1, 1].set_yticks([0, 1, 2, 3])
    axs[1, 1].set_yticklabels(["engage", "lock", "release", "nexit"])
    axs[1, 1].set_title("State Timeline (3+1)")
    axs[1, 1].grid(True)

    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Figure 2: torus 3D
    # --------------------------------------------------------
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    # draw segments by state color
    for i in range(len(data["x"]) - 1):
        s = data["states"][i]
        ax.plot(
            data["x"][i:i+2],
            data["y"][i:i+2],
            data["z"][i:i+2],
            color=state_colors[s],
            linewidth=1.2
        )

    # mark switch points
    if len(data["switches"]) > 0:
        sw = data["switches"]
        ax.scatter(
            data["x"][sw],
            data["y"][sw],
            data["z"][sw],
            color="black",
            s=25,
            label="switches"
        )

    ax.set_title("NEXAH v7.6 — Torus + Lorenz + C + State Switching")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Figure 3: top view
    # --------------------------------------------------------
    plt.figure(figsize=(8, 8))
    for state_name, color in state_colors.items():
        idx = [i for i, s in enumerate(data["states"]) if s == state_name]
        plt.scatter(
            data["x"][idx],
            data["y"][idx],
            s=4,
            color=color,
            label=state_name,
            alpha=0.7
        )

    if len(data["switches"]) > 0:
        sw = data["switches"]
        plt.scatter(
            data["x"][sw],
            data["y"][sw],
            color="black",
            s=18,
            label="switches"
        )

    plt.axhline(0, color="gray", linewidth=0.8)
    plt.axvline(0, color="gray", linewidth=0.8)
    plt.title("Top View — State-colored torus navigation")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.axis("equal")
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------
def print_summary(data):
    unique, counts = np.unique(data["states"], return_counts=True)
    count_map = dict(zip(unique, counts))

    print("\n=== NEXAH v7.6 Summary ===")
    print("C =", C)
    print("c min/max:", np.min(data["c"]), np.max(data["c"]))
    print("dc min/max:", np.min(data["dc"]), np.max(data["dc"]))
    print("energy min/max:", np.min(data["energy"]), np.max(data["energy"]))
    print("switch count:", len(data["switches"]))
    print("\nState counts:")
    for key in ["engage", "lock", "release", "nexit"]:
        print(f"{key}: {count_map.get(key, 0)}")


# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------
if __name__ == "__main__":
    data = simulate_v76(
        c0=0.15,
        dc0=0.0,
        theta0=0.0,
        phi0=0.0
    )
    print_summary(data)
    plot_results(data)
