# unified_flow_torus_map.py

import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7,7))

# --- Basis: Kreis (Phase space) ---
theta = np.linspace(0, 2*np.pi, 500)
ax.plot(np.cos(theta), np.sin(theta), linewidth=1)

# --- Pentagon (5) ---
pent_angles = np.linspace(0, 2*np.pi, 6)[:-1]
pent_x = np.cos(pent_angles)
pent_y = np.sin(pent_angles)
ax.plot(np.append(pent_x, pent_x[0]),
        np.append(pent_y, pent_y[0]),
        linewidth=2)

# --- Hexagon (6) ---
hex_angles = np.linspace(0, 2*np.pi, 7)[:-1] + np.pi/6
hex_x = 0.8*np.cos(hex_angles)
hex_y = 0.8*np.sin(hex_angles)
ax.plot(np.append(hex_x, hex_x[0]),
        np.append(hex_y, hex_y[0]),
        linewidth=1)

# --- Triangle (3-cycle) ---
tri_angles = [0, 2*np.pi/3, 4*np.pi/3]
tri_x = 0.5*np.cos(tri_angles)
tri_y = 0.5*np.sin(tri_angles)
ax.plot(np.append(tri_x, tri_x[0]),
        np.append(tri_y, tri_y[0]),
        linewidth=2)

# --- Flow (Spiral / Drift + Rotation) ---
t = np.linspace(0, 4*np.pi, 500)  # 720°
r = np.linspace(0.2, 1.0, 500)

x = r * np.cos(t)
y = r * np.sin(t)

ax.plot(x, y, linewidth=1)

# --- Center ---
ax.scatter([0], [0], s=50)

# --- Styling ---
ax.set_aspect('equal')
ax.set_xlim(-1.2,1.2)
ax.set_ylim(-1.2,1.2)
ax.set_title("UNIFIED FLOW TORUS MAP")

plt.show()
