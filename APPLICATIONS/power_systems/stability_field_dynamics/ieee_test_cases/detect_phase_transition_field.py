import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("v34_physical_coupling.csv")

df["theta"] = 2 * np.pi * df["t"] / 24.0

# 2D Feld
theta_bins = 36
c_bins = 20

theta_grid = np.linspace(0, 2*np.pi, theta_bins)
c_grid = np.linspace(df["C"].min(), df["C"].max(), c_bins)

heatmap = np.zeros((theta_bins-1, c_bins-1))

for i in range(theta_bins-1):
    for j in range(c_bins-1):
        mask = (
            (df["theta"] >= theta_grid[i]) & (df["theta"] < theta_grid[i+1]) &
            (df["C"] >= c_grid[j]) & (df["C"] < c_grid[j+1])
        )
        subset = df[mask]
        if len(subset) > 0:
            heatmap[i, j] = subset["loops"].mean()

plt.imshow(heatmap.T, aspect='auto', origin='lower',
           extent=[0, 2*np.pi, c_grid[0], c_grid[-1]])

plt.colorbar(label="loops")
plt.xlabel("theta (rad)")
plt.ylabel("C")
plt.title("Phase Transition Field")

plt.show()
