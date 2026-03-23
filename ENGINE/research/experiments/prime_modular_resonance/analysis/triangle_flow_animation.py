import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Base triangle (centered)
triangle = np.array([
    [0.0, 0.4],
    [-0.35, -0.2],
    [0.35, -0.2],
    [0.0, 0.4]
])

fig, ax = plt.subplots()
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_aspect('equal')

line, = ax.plot([], [], lw=2, color='red')

# rotation + drift
def transform(t):
    angle = t * 0.05  # rotation speed
    R = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle),  np.cos(angle)]
    ])
    
    drift = np.array([
        0.2 * np.sin(t * 0.03),
        0.2 * np.cos(t * 0.02)
    ])
    
    return (triangle @ R.T) + drift

def update(frame):
    pts = transform(frame)
    line.set_data(pts[:,0], pts[:,1])
    return line,

ani = FuncAnimation(fig, update, frames=400, interval=30)
plt.title("Triangle Flow (Generator Layer)")
plt.show()
