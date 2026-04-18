import numpy as np
import matplotlib.pyplot as plt

from nexah.field_layer.core.field import Field
from nexah.field_layer.core.metrics import FieldMetrics


# --- 1. Generate simple dynamical system (Lorenz-like) ---
def generate_lorenz(T=1000, dt=0.01):
    sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0

    x = np.zeros((T, 3))
    x[0] = [1.0, 1.0, 1.0]

    for t in range(T - 1):
        dx = sigma * (x[t, 1] - x[t, 0])
        dy = x[t, 0] * (rho - x[t, 2]) - x[t, 1]
        dz = x[t, 0] * x[t, 1] - beta * x[t, 2]

        x[t + 1] = x[t] + dt * np.array([dx, dy, dz])

    return x


# --- 2. Build FIELD ---
states = generate_lorenz()
field = Field(states)
metrics = FieldMetrics(field)

vectors = field.get_vector_field()
flow_strength = metrics.flow_strength()
curvature = metrics.curvature()
variance = metrics.fragmentation()


# --- 3. Visualization ---
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Trajectory (state space)
axs[0, 0].plot(states[:, 0], states[:, 1], linewidth=0.8)
axs[0, 0].set_title("State Trajectory (Lorenz projection)")
axs[0, 0].set_xlabel("x")
axs[0, 0].set_ylabel("y")

# Flow strength
axs[0, 1].plot(flow_strength)
axs[0, 1].set_title("Flow Strength ||dx/dt||")

# Curvature (acceleration proxy)
axs[1, 0].plot(curvature)
axs[1, 0].set_title("Acceleration (Curvature Proxy)")

# Variance (fragmentation proxy)
axs[1, 1].plot(variance)
axs[1, 1].set_title("State Variance (Dispersion Proxy)")

plt.tight_layout()
plt.show()
