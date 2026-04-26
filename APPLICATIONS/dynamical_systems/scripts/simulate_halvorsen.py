import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Halvorsen system definition
# -----------------------------

def halvorsen(state, a=1.4):
    x, y, z = state
    
    dx = -a * x - 4*y - 4*z - y**2
    dy = -a * y - 4*z - 4*x - z**2
    dz = -a * z - 4*x - 4*y - x**2
    
    return np.array([dx, dy, dz])


# -----------------------------
# RK4 integrator
# -----------------------------

def rk4_step(f, state, dt):
    k1 = f(state)
    k2 = f(state + 0.5 * dt * k1)
    k3 = f(state + 0.5 * dt * k2)
    k4 = f(state + dt * k3)
    
    return state + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)


# -----------------------------
# Simulation
# -----------------------------

def simulate(n_steps=50000, dt=0.01):
    state = np.array([1.0, 0.0, 0.0])
    
    trajectory = np.zeros((n_steps, 3))
    
    for i in range(n_steps):
        state = rk4_step(halvorsen, state, dt)
        trajectory[i] = state
    
    return trajectory


# -----------------------------
# Plot
# -----------------------------

def plot_3d(traj):
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(projection='3d')
    
    ax.plot(traj[:,0], traj[:,1], traj[:,2], lw=0.3)
    
    ax.set_title("Halvorsen Attractor")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    plt.tight_layout()
    plt.show()


# -----------------------------
# Run
# -----------------------------

if __name__ == "__main__":
    traj = simulate()
    plot_3d(traj)
