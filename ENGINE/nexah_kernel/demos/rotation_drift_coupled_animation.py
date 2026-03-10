import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


n = 5
radius = 5
iterations = 2500

fig, ax = plt.subplots(figsize=(7,7))

line, = ax.plot([],[],lw=1.2)

ax.set_xlim(-6,6)
ax.set_ylim(-6,6)
ax.set_aspect("equal")

ax.set_title("Coupled Rotation Drift System")


def generate(drift_deg):

    base = 2*np.pi/n
    drift = np.deg2rad(drift_deg)

    k = np.arange(iterations)

    theta = k*(base + drift)

    r = radius*(0.7 + 0.3*np.cos(k*0.02))

    x = r*np.cos(theta)
    y = r*np.sin(theta)

    return x,y


def update(frame):

    drift = frame*0.05

    x,y = generate(drift)

    line.set_data(x,y)

    return line,


ani = FuncAnimation(
    fig,
    update,
    frames=120,
    interval=40
)

plt.show()
