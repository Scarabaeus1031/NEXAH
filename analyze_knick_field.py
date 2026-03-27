import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("v34_physical_coupling.csv")

df["theta"] = 2 * np.pi * df["t"] / 24.0

if "dt" in df.columns:
    df["dt_norm"] = (df["dt"] - df["dt"].min()) / (df["dt"].max() - df["dt"].min())

gh = df[df["phase"] == "GH"]

plt.figure(figsize=(8, 8))
ax = plt.subplot(111, projection='polar')

ax.scatter(df["theta"], df["C"], s=20, alpha=0.2)
ax.scatter(gh["theta"], gh["C"], s=40, color="orange")

ax.set_title("Knick Field (C vs θ)")
plt.show()

plt.figure(figsize=(10, 4))
plt.scatter(df["theta"], df["loops"], alpha=0.3)
plt.scatter(gh["theta"], gh["loops"], color="red")

plt.xlabel("theta (rad)")
plt.ylabel("loops")
plt.title("Loops vs Angle (GH)")
plt.show()

if "dt" in df.columns:
    plt.figure(figsize=(10, 4))
    plt.scatter(df["theta"], df["dt"], alpha=0.3)
    plt.scatter(gh["theta"], gh["dt"], color="blue")

    plt.xlabel("theta (rad)")
    plt.ylabel("dt")
    plt.title("Time Dynamics vs Angle")
    plt.show()
