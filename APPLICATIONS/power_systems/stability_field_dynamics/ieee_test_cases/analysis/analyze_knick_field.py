import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === LOAD DATA ===
df = pd.read_csv("v34_physical_coupling.csv")

# Falls du später V35 nutzt:
# df = pd.read_csv("v35_time_dynamics.csv")

# === TIME → ANGLE MAPPING ===
df["theta"] = 2 * np.pi * df["t"] / 24.0

# === OPTIONAL: NORMALIZE DT ===
if "dt" in df.columns:
    df["dt_norm"] = (df["dt"] - df["dt"].min()) / (df["dt"].max() - df["dt"].min())

# === FILTER GH PHASE ===
gh = df[df["phase"] == "GH"]

# === PLOT 1: POLAR (C FIELD) ===
plt.figure(figsize=(8, 8))
ax = plt.subplot(111, projection='polar')

ax.scatter(df["theta"], df["C"], s=20, alpha=0.2, label="All")
ax.scatter(gh["theta"], gh["C"], s=40, color="orange", label="GH")

ax.set_title("Knick Field (C vs θ)")
ax.legend()

plt.show()

# === PLOT 2: LOOPS vs ANGLE ===
plt.figure(figsize=(10, 4))
plt.scatter(df["theta"], df["loops"], alpha=0.3, label="All")
plt.scatter(gh["theta"], gh["loops"], color="red", label="GH")

plt.xlabel("theta (rad)")
plt.ylabel("loops")
plt.title("Loops vs Angle (GH highlighted)")
plt.legend()
plt.show()

# === PLOT 3: DT vs ANGLE (KEY FOR V35) ===
if "dt" in df.columns:
    plt.figure(figsize=(10, 4))
    plt.scatter(df["theta"], df["dt"], alpha=0.3, label="All")
    plt.scatter(gh["theta"], gh["dt"], color="blue", label="GH")

    plt.xlabel("theta (rad)")
    plt.ylabel("dt")
    plt.title("Time Dynamics vs Angle (Knick timing)")
    plt.legend()
    plt.show()

# === OPTIONAL: LOAD SPLIT ===
for load in sorted(df["load"].unique()):
    subset = df[df["load"] == load]
    gh_subset = subset[subset["phase"] == "GH"]

    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, projection='polar')

    ax.scatter(subset["theta"], subset["C"], alpha=0.2)
    ax.scatter(gh_subset["theta"], gh_subset["C"], color="orange")

    ax.set_title(f"Load {load} – GH Corridor")
    plt.show()
